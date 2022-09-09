"""
Script for loading statistics.
"""

import argparse
from array import typecodes
from distutils.log import error
import requests
from helpers.boxscore import BoxscoreHelper
from helpers.player import PlayerHelper
from pyquery import PyQuery as pq
from urllib.parse import urljoin

import logging

logging.basicConfig(level=logging.INFO)

API_BASE_URL = 'http://k3-main:30082'


def get_schedules(year:int, week:int, type_code:str) -> list|None:
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

def get_stat_page(game_id:str) -> str|None:
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

def process_stats(stats:list) -> int:
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

def load_passing_stats(document:pq, schedule_id:int) -> None:
    """
    Compiles the Passing Stats to load to the API.

    Args:
        document (pq): Document
    """
    
    stat_section = document('#gamepackage-passing')    
    stat_document = pq(stat_section)    
    away_wrapper = stat_document('div.gamepackage-away-wrap')
    home_wrapper = stat_document('div.gamepackage-home-wrap')
    
    helper = BoxscoreHelper(API_BASE_URL)
    
    away_stats = helper.build_passing_statistics(schedule_id,away_wrapper)
    home_stats = helper.build_passing_statistics(schedule_id, home_wrapper)
    
    logging.info('LOADING PASSING STATS TO API')
    process_stats(away_stats)
    process_stats(home_stats)
    logging.info('FINISHED LOADING PASSING STATS')    
    

def load_rushing_stats(document:pq, schedule_id:int) -> None:
    """
    Compiles the Rushing stats for Home and Away

    Args:
        document (pq): PyQuery Document
        schedule_id (int): Schedule Id
    """
    
    stat_section = document('#gamepackage-rushing')    
    stat_document = pq(stat_section)    
    away_wrapper = stat_document('div.gamepackage-away-wrap')
    home_wrapper = stat_document('div.gamepackage-home-wrap')
    
    helper = BoxscoreHelper(API_BASE_URL)    
    away_stats = helper.build_rushing_statistics(schedule_id, away_wrapper)
    home_stats = helper.build_rushing_statistics(schedule_id, home_wrapper)
    
    
    logging.info('LOADING RUSHING STATS TO API')
    process_stats(away_stats)
    process_stats(home_stats)
    logging.info('RUSHING STATS LOADED')

        
def load_receiving_stats(document:pq, schedule_id:int) -> None:
    """
    Compiles all of the Receiving stats for the Home and Away teams/

    Args:
        document (pq): PyQuery document
        schedule_id (int): Schedule Id
    """
    
    stat_section = document('#gamepackage-receiving')    
    stat_document = pq(stat_section)    
    away_wrapper = stat_document('div.gamepackage-away-wrap')
    home_wrapper = stat_document('div.gamepackage-home-wrap')
    
    helper = BoxscoreHelper(API_BASE_URL)    
    away_stats = helper.build_receiving_statistics(schedule_id, away_wrapper)
    home_stats = helper.build_receiving_statistics(schedule_id, home_wrapper)
    
    
    logging.info('LOADING RECEIVING STATS TO API')
    process_stats(away_stats)
    process_stats(home_stats)
    logging.info('FINISHED LOADING RECEIVING STATS TO API')

def load_fumble_stats(document:pq, schedule_id:int) -> None:
    """
    Compiles all of the fumble stats for the Home and Away teams/

    Args:
        document (pq): PyQuery document
        schedule_id (int): Schedule Id

    """
    
    stat_section = document('#gamepackage-fumbles')    
    stat_document = pq(stat_section)    
    away_wrapper = stat_document('div.gamepackage-away-wrap')
    home_wrapper = stat_document('div.gamepackage-home-wrap')
    
    helper = BoxscoreHelper(API_BASE_URL)    
    away_stats = helper.build_fumble_statistics(schedule_id, away_wrapper)
    home_stats = helper.build_fumble_statistics(schedule_id, home_wrapper)
    
    
    logging.info('LOADING FUMBLE STATS TO API')
    process_stats(away_stats)
    process_stats(home_stats)
    logging.info('FINISHED FUMBLE RECEIVING STATS TO API')

def load_interception_stats(document:pq, schedule_id:int) -> None:
    """
    Compiles all of the Interception stats for the Home and Away teams/

    Args:
        document (pq): PyQuery document
        schedule_id (int): Schedule Id
    """
    
    stat_section = document('#gamepackage-interceptions')    
    stat_document = pq(stat_section)    
    away_wrapper = stat_document('div.gamepackage-away-wrap')
    home_wrapper = stat_document('div.gamepackage-home-wrap')
    
    helper = BoxscoreHelper(API_BASE_URL)    
    away_stats = helper.build_interception_statistics(schedule_id, away_wrapper)
    home_stats = helper.build_interception_statistics(schedule_id, home_wrapper)
    
    
    logging.info('LOADING INERCEPTIONS STATS TO API')
    process_stats(away_stats)
    process_stats(home_stats)
    logging.info('FINISHED LOADING INTERCEPTIONS STATS TO API')

def load_defensive_stats(document:pq, schedule_id:int) -> None:
    """
    Compiles all of the Defensive stats for the Home and Away teams/

    Args:
        document (pq): PyQuery document
        schedule_id (int): Schedule Id
    """
    
    stat_section = document('#gamepackage-defensive')    
    stat_document = pq(stat_section)    
    away_wrapper = stat_document('div.gamepackage-away-wrap')
    home_wrapper = stat_document('div.gamepackage-home-wrap')
    
    helper = BoxscoreHelper(API_BASE_URL)    
    away_stats = helper.build_defensive_statistics(schedule_id, away_wrapper)
    home_stats = helper.build_defensive_statistics(schedule_id, home_wrapper)
    
    
    logging.info('LOADING DEFENSE STATS TO API')
    process_stats(away_stats)
    process_stats(home_stats)
    logging.info('FINISHED LOADING DEFENSE STATS TO API')
    
def load_kick_return_stats(document:pq, schedule_id:int) -> None:
    """
    Compiles all of the Kick Returns stats for the Home and Away teams/

    Args:
        document (pq): PyQuery document
        schedule_id (int): Schedule Id
    """
    
    stat_section = document('#gamepackage-kickReturns')    
    stat_document = pq(stat_section)    
    away_wrapper = stat_document('div.gamepackage-away-wrap')
    home_wrapper = stat_document('div.gamepackage-home-wrap')
    
    helper = BoxscoreHelper(API_BASE_URL)    
    away_stats = helper.build_kick_return_statistics(schedule_id, away_wrapper)
    home_stats = helper.build_kick_return_statistics(schedule_id, home_wrapper)
    
    
    logging.info('LOADING KICK RETURN STATS TO API')
    process_stats(away_stats)
    process_stats(home_stats)
    logging.info('FINISHED LOADING KICK RETURN STATS TO API')
    
def load_punt_return_stats(document:pq, schedule_id:int) -> None:
    """
    Compiles all of the Punt Return stats for the Home and Away teams

    Args:
        document (pq): PyQuery document
        schedule_id (int): Schedule Id
    """
    
    stat_section = document('#gamepackage-puntReturns')    
    stat_document = pq(stat_section)    
    away_wrapper = stat_document('div.gamepackage-away-wrap')
    home_wrapper = stat_document('div.gamepackage-home-wrap')
    
    helper = BoxscoreHelper(API_BASE_URL)    
    away_stats = helper.build_punt_return_statistics(schedule_id, away_wrapper)
    home_stats = helper.build_punt_return_statistics(schedule_id, home_wrapper)
    
    
    logging.info('LOADING PUNT RETURN STATS TO API')
    process_stats(away_stats)
    process_stats(home_stats)
    logging.info('FINISHED LOADING PUNT RETURN STATS TO API')

def load_kicking_stats(document:pq, schedule_id:int) -> None:
    """
    Compiles all of the Kicking stats for the Home and Away teams/

    Args:
        document (pq): PyQuery document
        schedule_id (int): Schedule Id
    """
    
    stat_section = document('#gamepackage-kicking')    
    stat_document = pq(stat_section)    
    away_wrapper = stat_document('div.gamepackage-away-wrap')
    home_wrapper = stat_document('div.gamepackage-home-wrap')
    
    helper = BoxscoreHelper(API_BASE_URL)    
    away_stats = helper.build_kicking_statistics(schedule_id, away_wrapper)
    home_stats = helper.build_kicking_statistics(schedule_id, home_wrapper)
    
    
    logging.info('LOADING KICKING STATS TO API')
    process_stats(away_stats)
    process_stats(home_stats)
    logging.info('FINISHED LOADING KICKING STATS TO API')
    
def load_punting_stats(document:pq, schedule_id:int) -> None:
    """
    Compiles all of the Receiving stats for the Home and Away teams/

    Args:
        document (pq): PyQuery document
        schedule_id (int): Schedule Id
    """
    
    stat_section = document('#gamepackage-punting')    
    stat_document = pq(stat_section)    
    away_wrapper = stat_document('div.gamepackage-away-wrap')
    home_wrapper = stat_document('div.gamepackage-home-wrap')
    
    helper = BoxscoreHelper(API_BASE_URL)    
    away_stats = helper.build_punting_statistics(schedule_id, away_wrapper)
    home_stats = helper.build_punting_statistics(schedule_id, home_wrapper)
    
    
    logging.info('LOADING PUNTING STATS TO API')
    process_stats(away_stats)
    process_stats(home_stats)
    logging.info('FINISHED LOADING PUNTING STATS TO API')

def main(args:dict) -> None:
    """
    Main Function

    Args:
        args (dict): Argument Dictionary.
    """
    
    logging.info('GETTING SCHEDULES')
    
    schedules = get_schedules(int(args.get('year')), int(args.get('week')), str(args.get('type')))
    
    for schedule in schedules:
        if schedule.get('HomeGame', False) is True:
            logging.info(f"PULLING STATS FOR GAMEID: {schedule.get('gameId')}")
        
            stat_page_html = get_stat_page(schedule.get('gameId'))
            if stat_page_html:
                document = pq(stat_page_html)                
                schedule_id = int(schedule.get('id'))
                
                # COMPILE AND LOAD STATS
                load_passing_stats(document, schedule_id)
                load_rushing_stats(document, schedule_id)
                load_receiving_stats(document, schedule_id)
                load_defensive_stats(document, schedule_id)
                load_fumble_stats(document, schedule_id)
                load_interception_stats(document, schedule_id)
                load_kick_return_stats(document, schedule_id)
                load_kicking_stats(document, schedule_id)
                load_punt_return_stats(document, schedule_id)
                load_punting_stats(document, schedule_id)
                logging.info(f"FINISHED PULLING STATS FOR GAMEID: {schedule.get('gameId')}")
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