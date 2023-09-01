"""
Script for Scraping NFL Stats from the Web.
"""

import requests
from pyquery import PyQuery as pq
import logging
import os
from fake_useragent import UserAgent

logging.basicConfig(level=logging.INFO)

URL = "https://www.espn.com/college-football/boxscore/_/gameId/401282789"

headers = {
    'User-Agent': str(UserAgent.chrome)
}

response = requests.get(URL, headers=headers)

if not os.path.exists('./output'):
    os.makedirs('./output')

logging.info(response.status_code)

with open('./output/cfb_schedule.html', 'w', encoding='utf-8') as output_text:
    output_text.write(response.text)
