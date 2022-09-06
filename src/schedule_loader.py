"""
Script to Load Schedule Entries to the Database.
"""

from helpers.schedule import ScheduleHelper
import requests
import argparse
import logging
from urllib.parse import urljoin
import os

API_URL = urljoin(os.environ.get('BASE_URL'),'/api/schedule')

logging.basicConfig(level=logging.INFO)

def main(args:dict) -> None:
    """
    Main Function for pulling Schedule Entries from the system

    Args:
        args (dict): Arguments
    """
    
    schedule_url = 'https://www.espn.com/nfl/schedule/_/week/' + str(args.get('week')) + '/year/' + str(args.get('year')) + '/seasontype/' + str(args.get('type'))
    
    logging.info('RETRIEVING SCHEDULE..')
    response = requests.get(schedule_url)
    
    if response.status_code == 200:
        logging.info('BUILDING SCHEDULE ENTRIES')
        helper = ScheduleHelper(response.text)
        entries = helper.get_schedule_entries(int(args.get('week')), int(args.get('year')), str(args.get('type')))
        logging.info('WRITING TO WEB SERVICE')
        if entries:
            for entry in entries:
                
                schedule_response = requests.post(API_URL, json=entry)
                if schedule_response.status_code != 200:
                    logging.warning(f"SCHEDULE MAY HAVE FAILED TO POST: {entry.get('gameId')} : {schedule_response.status_code}")
        
    logging.info('DONE')
        


if __name__ == '__main__':
    argparser = argparse.ArgumentParser(description='Script Arguments')
    argparser.add_argument('-y', '--year', type=int, help='Year Value')
    argparser.add_argument('-w', '--week', type=int, help='Week Value')
    argparser.add_argument('-t', '--type', type=str, help='Schedule Type (1,2,3)')
    
    args = argparser.parse_args()
    
    main({
        'week': args.week,
        'year': args.year,
        'type': args.type
    })
    
