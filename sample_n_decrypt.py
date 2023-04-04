"""
Sample and Decrypt Json Files before Infering the Schema
"""
import sys
import json
import random
import os
import tqdm
from src.json_tool import json_tool


def run(src_path, target_path, sample_size):
    files = os.listdir(src_path)
    sampled_files = random.sample(files, sample_size)
    if not os.path.exists(target_path):
        os.mkdir(target_path)
    for file in tqdm.tqdm(sampled_files):
        json_obj = json_tool.load(f"{src_path}/{file}")
        with open(f"{target_path}/{file}", "w", encoding="utf-8") as f:
            json.dump(json_obj, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    run(sys.argv[1], sys.argv[2], int(sys.argv[3]))
