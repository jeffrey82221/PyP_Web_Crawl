# PyP_Web_Crawl

Crawling the Dependency Web of PyPi Packages 

# Goal: 

- [ ] link prediction (whether dependency would emerge between two package)
- [ ] node prediction (whether a package would continue to upgrade in the near future)

# Plan:

- [X] Refactor: extract the json loading and saving core 
- [X] Add decryption and encryption to the json loading and saving core
- [X] Add a sample and decrypt module to be use in `check_schema.yml`
- [X] Refactor: rename `check_schema.yml` to `check_latest_schema.yml`
- [X] Add a release online sampling module and build another `check_release_schema.yml` workflow
- [X] Add monthly run workflow for `update_release_time.py`.
- [-] Fix: JSkiner - pyo3_runtime.PanicException: There should not be Union in Union
- [X] Connect all ETL together at etl.yml (do it everyday monday noon. update package_name -> update latest -> update release time). 
- [X] Using auto PR instead of branch merging 
- [X] Connect check schema together at check.yml (do it everyday midnight.) 
- [-] Using fast checkout with workspace in the same workspace. 
- [ ] Generate Edge.csv & Node.csv of every month. 
