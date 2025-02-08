"""
Script for loading matchup statistics.
"""

import argparse
import logging
from urllib.parse import urljoin
import requests
from pyquery import PyQuery
from sqlalchemy import create_engine, URL
from sqlalchemy.orm import sessionmaker

from football_data.models import Team, StatisticCode, StatisticCategory, Statistic, Schedule, \
    TypeCode
from football_data.repositories import TeamRepository, StatisticRepository, StatisticCodeRepository, \
    StatisticCategoryRepository, ScheduleRepository, TypeCodeRepository

from helpers.box_score import BoxscoreHelper
from helpers.team import MatchupHelper

logging.basicConfig(level=logging.INFO)

API_BASE_URL = 'http://k3-main:30082'


def build_maker(server: str, database: str, user: str, password: str) -> sessionmaker:
    """
    Creates a Session Maker for the Stats DB.
    Args:
        server: Server
        database: Database
        user: User
        password: Password

    Returns: Session Maker
    """

    url = URL.create('postgresql', username=user, password=password, host=server, database=database)
    engine = create_engine(url)
    Team.metadata.create_all(bind=engine)
    Statistic.metadata.create_all(bind=engine)
    Schedule.metadata.create_all(bind=engine)
    StatisticCategory.metadata.create_all(bind=engine)
    StatisticCode.metadata.create_all(bind=engine)
    TypeCode.metadata.create_all(bind=engine)
    return sessionmaker(bind=engine, expire_on_commit=False)


def get_schedules(maker: sessionmaker, year: int, week: int, type_code: str) -> list[Schedule]:
    """
    Retrieves a listing of Schedule items from the API.

    Args:
        maker (sessionmaker): Session Maer
        year (int): year value
        week (int): week value
        type_code (str): type code

    Returns:
        list: list of Schedules
    """

    repo = ScheduleRepository(maker)
    schedules = repo.get_schedules(year=year, week=week)

    type_repo = TypeCodeRepository(maker)
    type_code = type_repo.get_type_code(code=type_code)

    return list(filter(lambda x: x.type_id == type_code.id, schedules))


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


def main(arguments: dict) -> None:
    """
    Main Function

    Args:
        arguments (dict): Argument Dictionary.
    """

    logging.info('GETTING SCHEDULES')
    db_user = arguments.get('user_name', '')
    db_password = arguments.get('password', '')
    db_server = arguments.get('server', '')
    database = arguments.get('database', '')
    year_value = int(arguments.get('year', 0))
    week_number = int(arguments.get('week', 0))
    type_code = arguments.get('type', '')

    maker = build_maker(db_server, database, db_user, db_password)

    schedules = get_schedules(maker, year_value, week_number, type_code)
    stat_helper = BoxscoreHelper(API_BASE_URL)

    for schedule in schedules:
        if schedule.is_home is True:
            logging.info('PULLING MATCHUP STATS FOR GAMEID: %s', schedule.game_id)
            stat_page_html = get_matchup_page(schedule.game_id)
            if stat_page_html:
                # COMPILE AND LOAD STATS
                matchup_helper = MatchupHelper(stat_page_html, API_BASE_URL)
                logging.info('LOADING MATCHUP STATS FOR GAME: %s', schedule.game_id)
                stats = matchup_helper.build_team_stats(schedule.team_id, schedule.opponent_id,
                                                        schedule.game_id)
                if stats:
                    logging.info('SENDING STATS TO API')
                    stat_helper.add_statistic(stats)
                    logging.info('FINISHED SENDING STATS TO API')
                else:
                    logging.warning('NO STATS FOUND FOR GAME: %s', schedule.game_id)
                logging.info('FINISHED LOADING STATS FOR GAME ID: %s', schedule.game_id)
    logging.info('DONE')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-y', '--year', type=int, help='Year Value')
    parser.add_argument('-w', '--week', type=int, help='Week Value')
    parser.add_argument('-t', '--type', type=str, help='Schedule Type (1,2,3)')
    parser.add_argument('-s', '--server', type=str, help='DB Server')
    parser.add_argument('-d', '--database', type=str, help='Database Name')
    parser.add_argument('-u', '--user', type=str, help='Username')
    parser.add_argument('-p', '--password', type=str, help='Password')

    args = parser.parse_args()

    main({
        'week': args.week,
        'year': args.year,
        'type': args.type,
        'user_name': args.user,
        'password': args.password,
        'server': args.server,
        'database': args.database
    })
