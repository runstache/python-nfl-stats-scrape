"""
Script for Scraping NFL Stats from the Web.
"""

import requests
from pyquery import PyQuery as pq
import logging
import os

logging.basicConfig(level=logging.INFO)

URL = "https://www.espn.com/nfl/boxscore/_/gameId/400951741"

response = requests.get(URL)

if not os.path.exists('./output'):
    os.mkdirs('./output')

with open('./output/boxscore.html', 'w', encoding='utf-8') as output_text:
    output_text.write(response.text)
