FROM python:3.13.0b1-slim

RUN apt-get update && apt-get -y install cron bash vim

# create empty crontab file
RUN touch /etc/cron.d/crontab

WORKDIR /app

# copy the python script to the image
COPY data_collector.py /app/data_collector.py

# copy the requirements file to the image
COPY ./requirements.txt /app/requirements.txt

# copy entrypoint shell script
COPY start.sh /app/start.sh

# create dat DIR
RUN mkdir /app/data

# install the dependencies and packages in the requirements file
RUN pip install -r requirements.txt

# set permissions
RUN chmod 0644 /etc/cron.d/crontab
RUN chmod +x /app/start.sh

# run the shell script
ENTRYPOINT ["/bin/bash","-c","source /app/start.sh"]
