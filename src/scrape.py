"""
Script for Scraping NFL Stats from the Web.
"""

import requests
from pyquery import PyQuery as pq
import logging
import os

logging.basicConfig(level=logging.INFO)

URL = "https://www.espn.com/nfl/matchup?gameId=401437654"

response = requests.get(URL)

if not os.path.exists('./output'):
    os.makedirs('./output')

with open('./output/teams.html', 'w', encoding='utf-8') as output_text:
    output_text.write(response.text)
