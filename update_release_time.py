"""
Sort the package release by upload date 
and continue to update the resulting table

TODO:
- [X] Load (package, release, updatetime) from data/latest
    - [X] Ignore release that does not fit a,b,c
    - [X] Updatetime -> max update date
- [X] Sort by datetime 
- [X] Save result of each month to parquet starting from 2005-01-01
"""
import os
import json
from datetime import datetime, timedelta
import tqdm
import pandas as pd
import glob
from src.ignore import ignore_filter
from src.json_tool import json_tool


class TimeFilter:
    """
    Filter out data not in time range
    """

    def __init__(self, start_time: datetime, end_time: datetime):
        self._start_time = start_time
        self._end_time = end_time

    def connect(self, input_tuples):
        for data in input_tuples:
            if data[-1] >= self._start_time and data[-1] < self._end_time:
                yield data


def convert_to_datetime(t):
    try:
        return datetime.strptime(t, "%Y-%m-%dT%H:%M:%S.%fZ")
    except:
        return datetime.strptime(t, "%Y-%m-%dT%H:%M:%SZ")


class MonthlyReleaseLoader:
    def __init__(
        self,
        etl_date: datetime,
        src_path="data/latest",
        target_path="data/release_time",
    ):
        self._src_path = src_path
        self._target_path = target_path
        self._start_time = MonthlyReleaseLoader._get_month_first_day(etl_date)
        self._end_time = MonthlyReleaseLoader._get_next_month(self._start_time)
        self._time_filter = TimeFilter(self._start_time, self._end_time)

    @staticmethod
    def _get_month_first_day(etl_date):
        first_day = datetime(etl_date.year, etl_date.month, 1)
        return first_day

    @staticmethod
    def _get_next_month(start_time):
        end_time = start_time + timedelta(days=32)
        return end_time.replace(day=1)

    def run(self):
        file_names = sorted(os.listdir(self._src_path))
        file_names = tqdm.tqdm(file_names, desc=self.target_parquet)
        paths = map(lambda fn: f"{self._src_path}/{fn}", file_names)
        releases = MonthlyReleaseLoader.extract_content_pipe(paths)
        releases = self._time_filter.connect(releases)
        dataframe = pd.DataFrame.from_records(
            releases, columns=["package", "version", "upload_time"]
        )
        if len(dataframe):
            dataframe.sort_values("upload_time", inplace=True)
            print("Number of selected releases:", len(dataframe))
            dataframe.to_parquet(self.target_parquet)
            print(self.target_parquet, "saved")
        else:
            dataframe.to_parquet(self.target_parquet.replace(".parquet", ".empty"))
            print(self.target_parquet.replace(".parquet", ".empty"), "saved")

    @property
    def target_parquet(self):
        month_str = "{:02d}".format(self._start_time.month)
        return f"{self._target_path}/{self._start_time.year}-{month_str}.parquet"

    @property
    def parquet_exists(self):
        return os.path.exists(self.target_parquet) or os.path.exists(
            self.target_parquet.replace(".parquet", ".empty")
        )

    @staticmethod
    def extract_content_pipe(paths):
        for path in paths:
            result = json_tool.load(path)
            for version, release_content in result["releases"].items():
                if ignore_filter._pattern.match(version) and release_content:
                    times = [
                        content["upload_time_iso_8601"] for content in release_content
                    ]
                    dates = [convert_to_datetime(t) for t in times]
                    try:
                        yield (result["info"]["name"], version, max(dates))
                    except BaseException as e:
                        print(f"error in {version}:\n", release_content)
                        raise e


def get_all_etl_date():
    threshold_date = MonthlyReleaseLoader._get_month_first_day(datetime.now())
    date = datetime(2005, 3, 1)
    while date < threshold_date:
        yield date
        date = MonthlyReleaseLoader._get_next_month(date)


def read_parquet():
    parquet_files = glob.glob("data/release_time/*.parquet")
    df = pd.concat([pd.read_parquet(file) for file in parquet_files])
    return df


if __name__ == "__main__":
    print("Number of releases in parquets before etl:", len(read_parquet()))
    for etl_date in get_all_etl_date():
        loader = MonthlyReleaseLoader(etl_date)
        if loader.parquet_exists:
            print(loader.target_parquet, "exists:", loader.parquet_exists)
        else:
            loader.run()
            print("Number of releases in parquets after etl:", len(read_parquet()))
