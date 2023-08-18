# Pex Data Collector

This project provides a way to extract call detail records on a daily basis from Pexip Infinity using the Management History API, storing the records as CSV files. Packaged as a Docker container, it's designed to provide the same functionality which is covered in the Pexip documentation, using the published PowerShell script (https://docs.pexip.com/api_manage/extract_analyse.htm#script).

The output of this container:

- Writes that day's history to two CSV files. The files are named in the format: `<date_time>_pexHistoryConf.csv` and `<date_time>_pexHistoryPart.csv`.
- Aggregates the running history data into two files. These files are named `pexHistoryConf.csv` and `pexHistoryPart.csv`.
- Application level logs written to `data_collector.log`.
- All files are output to a data folder.
