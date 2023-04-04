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
- [ ] Add a release online sampling module and build another `check_release_schema.yml` workflow
- [ ] Add monthly run workflow for `update_release_time.py`.
- [ ] Generate Edge.csv & Node.csv of every month. 