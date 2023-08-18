from datetime import datetime, timedelta
import requests
import urllib3
import csv
import os
import logging

# set log format
logging.basicConfig(format='%(asctime)s %(levelname)s:%(name)s:%(message)s',filename='/app/data/data_collector.log',filemode = 'a')

logger = logging.getLogger('collector')

logger.setLevel(logging.DEBUG)

# suppresses warning when verify (in requests) is false
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


# function to make API call to MGR
def get_api(url,username,password):
    #
    try:
        logger.debug('Attempting API call')

        response = requests.request("GET", url, auth=(username, password), verify=False)

        # grab the json objects
        data_json = response.json()['objects']
        # grab the total_count in meta data
        count = response.json()['meta']['total_count']
               
        return data_json, count, response.status_code

    except:
        logger.error('There was a problem eith the API call!')

        return "ERROR! There is a problem with this request."

# function to write CSV's
def write_csv(mgr_call,mgr_user,mgr_password,type):
    int_file =''

    # determine filenames based on passed type
    if type == "conf":
        int_file = "_pexHistoryConf.csv"
        agg_file = "pexHistoryConf.csv"
    else:
        int_file = "_pexHistoryPart.csv"
        agg_file = "pexHistoryPart.csv"

    logger.debug('Calling get_api function for '+ type +' data')

    resp_json = get_api(mgr_call,mgr_user,mgr_password)
    x_json = resp_json[0]

    # create interval CSV
    logger.debug('Attempting to write interval data to CSV')

    x_filename = now.strftime("%Y-%m-%d_%H-%M-%S") + int_file

    data_file = open('/app/data/'+x_filename, 'w', newline='')
    csv_writer = csv.writer(data_file)

    count = 0
    for data in x_json:
        if count == 0:
            header = data.keys()
            csv_writer.writerow(header)
            count += 1
        csv_writer.writerow(data.values())

    data_file.close()

    # append to aggregated CSV
    logger.debug('Attempting to write aggregated data to CSV')

    x_filename = agg_file

    data_file = open('/app/data/'+x_filename, 'a', newline='')
    csv_writer = csv.writer(data_file)

    # don't want headers in this data
    for data in x_json:
        csv_writer.writerow(data.values())

    data_file.close()


if __name__ == '__main__':
    
    
    logger.info('Running data_collector.py')

    # Management Node Details
    # Can set env variables in the terminal with $env:DEFAULT_MGR_ADDRESS = '<value>', $env:DEFAULT_MGR_SECRET = '<value>' etc.
    mgr_host = os.getenv('DEFAULT_MGR_ADDRESS')
    mgr_user = os.getenv('DEFAULT_MGR_USERNAME', 'admin')
    mgr_password = os.getenv('DEFAULT_MGR_SECRET')
    conf_limit = os.getenv('DEFAULT_CONF_LIMIT','5000')
    part_limit = os.getenv('DEFAULT_PART_LIMIT','10000')
    
    logger.debug('ENV DEFAULT_MGR_ADDRESS =' + mgr_host)
    logger.debug('ENV DEFAULT_MGR_USERNAME =' + mgr_user)
    logger.debug('ENV DEFAULT_CONF_LIMIT =' + conf_limit)
    logger.debug('ENV DEFAULT_PART_LIMIT =' + part_limit)

    # Get the current time and date
    now = datetime.now()
    # Convert the current time to a sortable format (suits the Management Node) e.g. 2019-04-08T00:00:00
    current_datetime = now.strftime("%Y-%m-%dT%H:%M:%S")
    # Number of days ago to start the report from (1 day)
    start_date = now - timedelta(days=1)
    # Convert the start time to a sortable format (suits the Management Node):
    start_date = start_date.strftime("%Y-%m-%dT%H:%M:%S")

    logging.debug('Current Date/Time =' + current_datetime + ', Start Date/Time = ' + start_date)


    mgr_part = "https://" + mgr_host + "/api/admin/history/v1/participant/" + "?limit=" + part_limit + "&end_time__gte=" + start_date + "&end_time__lt=" + current_datetime
    logger.info('Participant API request URL = ' + mgr_part)
    mgr_conf = "https://" + mgr_host + "/api/admin/history/v1/conference/" + "?limit=" + conf_limit + "&end_time__gte=" + start_date + "&end_time__lt=" + current_datetime
    logger.info('Conference API request URL = ' + mgr_conf)

    # make the request and write CSV
    logger.debug('Calling write_csv function for conference data')
    write_csv(mgr_conf,mgr_user,mgr_password,"conf")
    logger.debug('Calling write_csv function for participant data')
    write_csv(mgr_part,mgr_user,mgr_password,"part")