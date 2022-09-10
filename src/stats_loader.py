"""
Script for loading statistics.
"""

import argparse
import logging
from typing import Callable
from urllib.parse import urljoin

import requests
from pyquery import PyQuery as pq

from helpers.boxscore import BoxscoreHelper
from helpers.player import PlayerHelper

logging.basicConfig(level=logging.INFO)

API_BASE_URL = 'http://k3-main:30082'

HOME_WRAPPER = 'div.gamepackage-home-wrap'
AWAY_WRAPPER = 'div.gamepackage-away-wrap'


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


def get_stat_page(game_id: str) -> str | None:
    """
    Retrieves the Stat page from the Web

    Args:
        game_id (str): Game Id to retrieve

    Returns:
        str: Boxscore page html
    """

    url = 'https://www.espn.com/nfl/boxscore/_/gameId/' + str(game_id)
    response = requests.get(url)

    if response.status_code == 200:
        return response.text
    return None


def process_stats(stats: list) -> int:
    """
    Processes list of stats into the API.

    Args:
        stats (list): Stats to load

    Returns:
        int: errors
    """
    helper = BoxscoreHelper(API_BASE_URL)
    for stat in stats:
        # Add the player
        player_helper = PlayerHelper(stat.get('playerUrl'), API_BASE_URL)
        player = player_helper.build_player()
        if player:
            player_helper.add_player_information(player)
    # Submit the Stats
    helper.add_statistic(stats)


def load_stats(document: pq, stat_sections: tuple, game_id: int, team_id: int, method: Callable) -> list:
    """
    Loads the Stats Section from the Stats Section Locator, game, team and helper function to use.

    Args:
        document (pq): PyQuery Document
        stat_sections (tuple): Stats Section Locator (Identifier, Wrapper)
        game_id (int): Game Id
        team_id (int): Team Id
        method (function): Helper Method
    """

    stat_section = document(stat_sections[0])
    stat_document = pq(stat_section)

    wrapper = stat_document(stat_sections[1])

    stats = method(team_id, game_id, wrapper)
    return stats


def main(args: dict) -> None:
    """
    Main Function

    Args:
        args (dict): Argument Dictionary.
    """

    logging.info('GETTING SCHEDULES')

    schedules = get_schedules(int(args.get('year')), int(
        args.get('week')), str(args.get('type')))
    helper = BoxscoreHelper(API_BASE_URL)
    for schedule in schedules:
        if schedule.get('HomeGame', False) is True:
            game_id = schedule.get('gameId')
            logging.info(f"PULLING STATS FOR GAMEID: {game_id}")

            stat_page_html = get_stat_page(schedule.get('gameId'))
            if stat_page_html:
                document = pq(stat_page_html)
                team_id = int(schedule.get('teamId'))
                opponent_id = int(schedule.get('opponentId'))

                stats_categories = [
                    ('#gamepackage-punting',
                     helper.build_punting_statistics, 'PUNTING'),
                    ('#gamepackage-kicking',
                     helper.build_kicking_statistics, 'KICKING'),
                    ('#gamepackage-puntReturns',
                     helper.build_punt_return_statistics, 'PUNT RETURN'),
                    ('#gamepackage-kickReturns',
                     helper.build_kick_return_statistics, 'KICK RETURN'),
                    ('#gamepackage-defensive',
                     helper.build_defensive_statistics, 'DEFENSICE'),
                    ('#gamepackage-interceptions',
                     helper.build_interception_statistics, 'INTERCEPTION'),
                    ('#gamepackage-fumbles', helper.build_fumble_statistics, 'FUMBLE'),
                    ('#gamepackage-receiving',
                     helper.build_receiving_statistics, 'RECEIVING'),
                    ('#gamepackage-rushing',
                     helper.build_rushing_statistics, 'RUSHING'),
                    ('#gamepackage-passing', helper.build_passing_statistics, 'PASSING')
                ]

                # COMPILE AND LOAD THE STATS
                for category in stats_categories:
                    logging.info(f"LOADING {category[2]} STATS TO API")
                    process_stats(load_stats(
                        document, (category[0], HOME_WRAPPER), game_id, team_id, category[1]))
                    process_stats(load_stats(
                        document, (category[0], AWAY_WRAPPER), game_id, opponent_id, category[1]))
                    logging.info(
                        f"FINISHED LOADING {category[2]} STATS TO API")
                logging.info(
                    f"FINISHED PULLING STATS FOR GAMEID: {schedule.get('gameId')}")
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
