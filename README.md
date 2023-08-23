# Pex Data Collector

This project provides a way to extract call detail records on a daily basis from Pexip Infinity using the Management History API, storing the records as CSV files. Packaged as a Docker container, it's designed to provide the same functionality which is covered in the Pexip documentation, using the published PowerShell script (https://docs.pexip.com/api_manage/extract_analyse.htm#script).

The output of this container:

- Writes that day's history to two CSV files. The files are named in the format: `<date_time>_pexHistoryConf.csv` and `<date_time>_pexHistoryPart.csv`.
- Aggregates the running history data into two files. These files are named `pexHistoryConf.csv` and `pexHistoryPart.csv`.
- Application level logs written to `data_collector.log`.
- All files are output to a data folder.

## Build and Run the Container
Create the image from the Dockerfile using the docker build command:

```docker build . -t aledmorris/pex_data_collector```

Before running the container, there are some pre-requisites to be aware of:

- A volume must be mounted, mapping a local folder to ```/app/data/``` in the container. This folder is where the extracted data and log is stored.
- Minimum of three environment variables need to be used (noted below) to represent the Management Node FQDN, Management Node Password, and Cron expression. Failure to specify these will result in the data collection failing.

### Envrionment variables
The environment variables are described below:

- ```DEFAULT_MGR_ADDRESS```: The FQDN or IP of the Management Node you are gathering data from.
- ```DEFAULT_MGR_USERNAME```: (Optional) The username to authenticate to the Management Node, defaults to ```admin```.
- ```DEFAULT_MGR_SECRET```: The password to authenticate to the Management Node.
- ```DEFAULT_CONF_LIMIT```: (Optional) maximum number of conference records to retrieve, defaults to ```5000```. If you find that this value is too low then this can be increased.
- ```DEFAULT_PART_LIMIT```: (Optional) maximum number of participant records to retrieve, defaults to ```10000```. If you find that this value is too low then this can be increased.
- ```DATA_CRON_TIME```: Cron expression to control when the data is collected. It should be set to once a day. Use an online cron expression generator if unsure (e.g. https://www.atatus.com/tools/cron)

An example ```.env``` file can be found in the repository. The env file can be used or you can manually set the environment variables in the CLI prior to running the Docker run command.

### Run the container
Once the image is built, you can run the container using one of the following example commands. These commands run in the foreground and you will see the output from the container, which can be useful for troubleshooting. The container can be run in detached mode (in the background) by using the ```-d``` flag.

#### Variables Inline
- ```docker run -e DEFAULT_MGR_ADDRESS='mgr.example.com' -e DEFAULT_MGR_SECRET='SuperSecretPasswordLOL!' -e DATA_CRON_TIME='0 0 * * *' -v ./data:/app/data aledmorris/pex_data_collector:latest```

#### Variables in .env file
- ```docker run --env-file .env -v ./data:/app/data aledmorris/pex_data_collector:latest```

## Disclaimer
Please be aware of the following.

- The container is **not** production ready, it is purely a proof of concept to demonstrate a number of different elements, namely: Pexip Infinity Management API, Ptyhon, Docker, Dockerfile, and using Cron within a Docker container to run a script on a shedule.
- This container is not secure and you should use it at your own risk.
    - API requests to the Management Node use HTTPS, but TLS is unverified.
    - As the password is passed to the container, it can be viewed in plaintext when connecting to the container shell.
    - Storing your password in the ```.env``` file (i.e. in plain text) is probably not a good idea.