#!/bin/bash


# add env variables to the crontab file
printf "DEFAULT_MGR_ADDRESS=$DEFAULT_MGR_ADDRESS\n" >> /etc/cron.d/crontab
printf "DEFAULT_MGR_SECRET=$DEFAULT_MGR_SECRET\n" >> /etc/cron.d/crontab

if [ $DEFAULT_MGR_USERNAME != '' ]
then
  printf "DEFAULT_MGR_USERNAME=$DEFAULT_MGR_USERNAME\n" >> /etc/cron.d/crontab
fi
if [ $DEFAULT_CONF_LIMIT != '' ]
then
  printf "DEFAULT_CONF_LIMIT=$DEFAULT_CONF_LIMIT\n" >> /etc/cron.d/crontab
fi
if [ $DEFAULT_PART_LIMIT != '' ]
then
  printf "DEFAULT_PART_LIMIT=$DEFAULT_PART_LIMIT\n" >> /etc/cron.d/crontab
fi


echo -e '>> Writing ENV to cron.'

# append entry to crontab file
printf "$DATA_CRON_TIME /usr/local/bin/python /app/data_collector.py > /proc/1/fd/1 2>/proc/1/fd/2\n# END CRON JOB" >> /etc/cron.d/crontab
echo -e '>> Writing cron config..'


# running Cron
/usr/bin/crontab /etc/cron.d/crontab

echo -e '>> Running cron...'

echo -e 'Application logs can be found in 'data_collector.log', located in the data folder.'

cron -f