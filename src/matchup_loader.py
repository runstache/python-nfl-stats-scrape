"""
Script for loading matchup statistics.
"""

import argparse
import logging
from typing import Callable
from urllib.parse import urljoin

import requests
from pyquery import PyQuery as pq

from helpers.boxscore import BoxscoreHelper
from helpers.team import MatchupHelper

logging.basicConfig(level=logging.INFO)

API_BASE_URL = 'http://k3-main:30082'



def get_schedules(year: int, week: int, type_code: str) -> list | None:
    """
    Retrieves a listing of Schedule items from the API.

    Args:
        year (int): year value
        week (int): week value
        type_code (str): type code

    Returns:
        list: list of Schedules
    """
    params = {
        'week': week,
        'year': year,
        'typeCode': type_code
    }
    url = urljoin(API_BASE_URL, '/api/schedules')
    success = False
    max_attempts = 5
    count = 0

    while not success and count <= max_attempts:
        try:
            response = requests.get(url, params=params, timeout=60)
            if (response.status_code == 200):
                success = True
                return response.json()
            else:
                success = False
                count = count + 1
        except TimeoutError:
            success = False
            count = count + 1
    return None


def get_matchup_page(game_id: str) -> str | None:
    """
    Retrieves the Stat page from the Web

    Args:
        game_id (str): Game Id to retrieve

    Returns:
        str: Boxscore page html
    """

    url = 'https://www.espn.com/nfl/matchup/_/gameId/' + str(game_id)
    response = requests.get(url)

    if response.status_code == 200:
        return response.text
    return None

def main(args: dict) -> None:
    """
    Main Function

    Args:
        args (dict): Argument Dictionary.
    """

    logging.info('GETTING SCHEDULES')

    schedules = get_schedules(int(args.get('year')), int(
        args.get('week')), str(args.get('type')))
    stat_helper = BoxscoreHelper(API_BASE_URL)
    
    for schedule in schedules:
        if schedule.get('HomeGame', False) is True:
            game_id = schedule.get('gameId')
            logging.info(f"PULLING MATCHUP STATS FOR GAMEID: {game_id}")

            stat_page_html = get_matchup_page(schedule.get('gameId'))
            if stat_page_html:
                team_id = int(schedule.get('teamId'))
                opponent_id = int(schedule.get('opponentId'))

                # COMPILE AND LOAD STATS
                matchup_helper = MatchupHelper(stat_page_html, API_BASE_URL)
                
                logging.info(f"LOADING MATCHUP STATS FOR GAME: {game_id}")
                stats = matchup_helper.build_team_stats(team_id, opponent_id, game_id)
                if stats:
                    logging.info('SENDING STATS TO API')
                    stat_helper.add_statistic(stats)
                    logging.info('FINISHED SENDING STATS TO API')
                else:
                    logging.warning(f"NO STATS FOUND FOR GAME: {game_id}")
                logging.info(f"FINISHED LOADING STATS FOR GAME ID: {game_id}")
    logging.info('DONE')


if __name__ == '__main__':
    argparser = argparse.ArgumentParser(description='Script Arguments')
    argparser.add_argument('-y', '--year', type=int, help='Year Value')
    argparser.add_argument('-w', '--week', type=int, help='Week Value')
    argparser.add_argument('-t', '--type', type=str,
                           help='Schedule Type (1,2,3)')

    args = argparser.parse_args()

    main({
        'week': args.week,
        'year': args.year,
        'type': args.type
    })
