#!/bin/bash

# display env vars for sanity checking
# WARNING! Uncommenting these will output the MGR node password to the terminal
#echo -e "\nDocker ENV vars\n--------------------------------------\n"
#echo -e "MGR = $DEFAULT_MGR_ADDRESS\n"
#echo -e "PASS = $DEFAULT_MGR_SECRET\n"
#echo -e "CRON timer = $DATA_CRON_TIME\n"
#echo -e "\n--------------------------------------\n"

# add env variables to the crontab file
printf "DEFAULT_MGR_ADDRESS=$DEFAULT_MGR_ADDRESS\n" >> /etc/cron.d/crontab
printf "DEFAULT_MGR_SECRET=$DEFAULT_MGR_SECRET\n" >> /etc/cron.d/crontab

echo -e '>> Writing ENV to cron.'

# append entry to crontab file
printf "$DATA_CRON_TIME /usr/local/bin/python /app/data_collector.py > /proc/1/fd/1 2>/proc/1/fd/2\n# END CRON JOB" >> /etc/cron.d/crontab
echo -e '>> Writing cron config..'


# display contents of crontab for sanity check
# WARNING! Uncommenting these will output the MGR node password to the terminal
#echo -e "\nConfigured crontab\n--------------------------------------\n"
#cat /etc/cron.d/crontab
#echo -e "\n--------------------------------------\n"

# running Cron
/usr/bin/crontab /etc/cron.d/crontab

echo -e '>> Running cron...'

echo -e 'Application logs can be found in 'data_collector.log', located in the data folder.'

cron -f