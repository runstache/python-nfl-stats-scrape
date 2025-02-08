"""
Script for Scraping NFL Stats from the Web.
"""

import logging
from selenium import webdriver
import json
import requests
from fake_useragent import UserAgent

logging.basicConfig(level=logging.INFO)

boxscore_url = "https://www.espn.com/nfl/boxscore/_/gameId/401437650"
schedule_url = 'https://www.espn.com/nfl/schedule/_/week/1/year/2022/seasontype/2'
matchup_url = 'https://www.espn.com/nfl/matchup/_/gameId/401437650'
player_url = 'https://www.espn.com/nfl/player/_/id/3918298/josh-allen'

options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--ignore-certificate-errors')

browser = webdriver.Chrome(options=options)
browser.get(boxscore_url)
boxscore_result:dict = browser.execute_script('return window.__espnfitt__')
browser.get(schedule_url)
schedule_result:dict = browser.execute_script('return window.__espnfitt__')
browser.get(matchup_url)
matchup_result = browser.execute_script('return window.__espnfitt__')
browser.get(player_url)
player_result = browser.execute_script('return window.__espnfitt__')
browser.quit()
with open('output/boxscore.json', 'w', encoding='utf-8') as output_file:
    output_file.write(json.dumps(boxscore_result))

with open('output/schedule.json', 'w', encoding='utf-8') as sched_outpout:
    sched_outpout.write(json.dumps(schedule_result))

with open('output/matchup.json', 'w', encoding='utf-8') as match_out:
    match_out.write(json.dumps(matchup_result))

with open('output/player.json', 'w', encoding='utf-8') as player_out:
    player_out.write(json.dumps(player_result))


headers = {
    'User-Agent': UserAgent().chrome
}
response = requests.get(player_url, headers=headers)

with open('./output/player.html', 'w', encoding='utf-8') as match_out_html:
    match_out_html.write(response.text)


