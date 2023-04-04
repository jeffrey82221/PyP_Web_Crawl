"""
- [X] Download release json given package name and release name 
- [X] Get release names of a package from data/latest/<package_name>
- [X] Create releases/package_name folder automatically if it does not exists 
- [-] Identify missing release in releases/package_name folder 
- [X] Adding ignoring rule (
        1. [X] ignore version start with 0. 
        2. [X] ignore version name not all digits (e,g, 1.2.3b / 1.2.3.dev123))
        3. [X] ignore version name with no '.' mark in it.
        4. [X] ignore version with first number having more than 4 digit (12313245.1232.4)
        5. [X] ignore version start with v
"""
import json
import glob
import requests
import re
import os
from src.ignore import ignore_filter
from src.json_tool import json_tool


def download_json(pkg_name, version):
    url = f"https://pypi.org/pypi/{pkg_name}/{version}/json"
    result = requests.get(url).json()
    return result


def get_release_versions(pkg_name):
    json_path = glob.glob(f"data/latest/{pkg_name}.rc*.json")
    if json_path:
        result = json_tool.load(json_path[0])
        return list(result["releases"].keys())
    else:
        return []


def save_json(pkg_name, release, json_obj):
    save_path = f"data/releases/{pkg_name}/{release}.json"
    json_tool.dump(save_path, json_obj)


def update(pkg_name):
    releases = list(get_release_versions(pkg_name))
    print("all releases:", releases)
    releases = ignore_filter.connect(releases)
    releases = filter(
        lambda ver: not os.path.exists(f"data/releases/{pkg_name}/{ver}.json"), releases
    )
    releases = list(releases)
    print("filtered releases:", releases)
    if releases:
        jsons = map(
            lambda release: (pkg_name, release, download_json(pkg_name, release)),
            releases,
        )
        folder = f"data/releases/{pkg_name}"
        if not os.path.exists(folder):
            os.mkdir(folder)
            print(folder, "created")
        saved_json = map(lambda x: save_json(*x), jsons)
        _ = list(saved_json)
