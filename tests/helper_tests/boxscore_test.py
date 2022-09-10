"""
Tests for the Boxscore helper.
"""

from src.helpers.boxscore import BoxscoreHelper
from pyquery import PyQuery as pq
from assertpy import assert_that

TEST_FILE = './tests/test_files/boxscore.html'
BASE_URL = 'http://localhost'
TEAM_ID = 1
GAME_ID = 12345

def load_test_file() -> str:
    """
    Loads the Test file

    Returns:
        str: Test File Html
    """
    
    with open(TEST_FILE, 'r', encoding='utf-8') as test_file:
        return test_file.read()
    
def test_passing_stats():
    """
    Tests retrieving the passing stats.
    """
    
    document = pq(load_test_file())    
    stat_section = document('#gamepackage-passing')    
    stat_document = pq(stat_section)    
    stat_wrapper = stat_document('div.gamepackage-away-wrap')
    
    helper = BoxscoreHelper(BASE_URL)
    
    stats = helper.build_passing_statistics(TEAM_ID, GAME_ID, stat_wrapper)
    
    assert_that(stats).is_not_empty()
    
    assert_that(stats)\
        .contains({
            'statisticCode': 'PC',
            'playerUrl': 'https://www.espn.com/nfl/player/_/id/2577189/brett-hundley',
            'value': 14,
            'gameId': GAME_ID,
            'teamId': TEAM_ID,
            'categoryCode': 'O'
        })\
            .contains({
            'statisticCode': 'PA',
            'playerUrl': 'https://www.espn.com/nfl/player/_/id/2577189/brett-hundley',
            'value': 24,
            'gameId': GAME_ID,
            'teamId': TEAM_ID,
            'categoryCode': 'O'
        })\
        .contains({
            'statisticCode': 'PYDS',
            'playerUrl': 'https://www.espn.com/nfl/player/_/id/2577189/brett-hundley',
            'value': 172,
            'gameId': GAME_ID,
            'teamId': TEAM_ID,
            'categoryCode': 'O'
        })\
        .contains({
            'statisticCode': 'PSAVG',
            'playerUrl': 'https://www.espn.com/nfl/player/_/id/2577189/brett-hundley',
            'value': 7.2,
            'gameId': GAME_ID,
            'teamId': TEAM_ID,
            'categoryCode': 'O'
        })\
        .contains({
            'statisticCode': 'PTD',
            'playerUrl': 'https://www.espn.com/nfl/player/_/id/2577189/brett-hundley',
            'value': 1,
            'gameId': GAME_ID,
            'teamId': TEAM_ID,
            'categoryCode': 'O'
        })\
        .contains({
            'statisticCode': 'PINT',
            'playerUrl': 'https://www.espn.com/nfl/player/_/id/2577189/brett-hundley',
            'value': 2,
            'gameId': GAME_ID,
            'teamId': TEAM_ID,
            'categoryCode': 'O'
        })\
        .contains({
            'statisticCode': 'QBR',
            'playerUrl': 'https://www.espn.com/nfl/player/_/id/2577189/brett-hundley',
            'value': 3.8,
            'gameId': GAME_ID,
            'teamId': TEAM_ID,
            'categoryCode': 'O'
        })\
        .contains({
            'statisticCode': 'RTG',
            'playerUrl': 'https://www.espn.com/nfl/player/_/id/2577189/brett-hundley',
            'value': 59.7,
            'gameId': GAME_ID,
            'teamId': TEAM_ID,
            'categoryCode': 'O'
        })
    
    
    
def test_rushing_stats():
    """
    Tests Retrieving the Rushing Stats.
    """
    document = pq(load_test_file())    
    stat_section = document('#gamepackage-rushing')    
    rstat_document = pq(stat_section)    
    stat_wrapper = rstat_document('div.gamepackage-away-wrap')
    
    helper = BoxscoreHelper(BASE_URL)
    
    stats = helper.build_rushing_statistics(TEAM_ID, GAME_ID, stat_wrapper)
    
    assert_that(stats).is_not_empty()
    
    assert_that(stats)\
        .contains({
            'statisticCode': 'RCAR',
            'playerUrl': 'https://www.espn.com/nfl/player/_/id/2980453/jamaal-williams',
            'value': 22,
            'gameId': GAME_ID,
            'teamId': TEAM_ID,
            'categoryCode': 'O'
        })\
            .contains({
            'statisticCode': 'RYDS',
            'playerUrl': 'https://www.espn.com/nfl/player/_/id/2980453/jamaal-williams',
            'value': 82,
            'gameId': GAME_ID,
            'teamId': TEAM_ID,
            'categoryCode': 'O'
        })\
        .contains({
            'statisticCode': 'RAVG',
            'playerUrl': 'https://www.espn.com/nfl/player/_/id/2980453/jamaal-williams',
            'value': 3.7,
            'gameId': GAME_ID,
            'teamId': TEAM_ID,
            'categoryCode': 'O'
        })\
        .contains({
            'statisticCode': 'RTD',
            'playerUrl': 'https://www.espn.com/nfl/player/_/id/2980453/jamaal-williams',
            'value': 0,
            'gameId': GAME_ID,
            'teamId': TEAM_ID,
            'categoryCode': 'O'
        })\
        .contains({
            'statisticCode': 'RLONG',
            'playerUrl': 'https://www.espn.com/nfl/player/_/id/2980453/jamaal-williams',
            'value': 14,
            'gameId': GAME_ID,
            'teamId': TEAM_ID,
            'categoryCode': 'O'
        })

def test_receiving_stats():
    """
    Tests retrieving the receiving stats.
    """
    
    document = pq(load_test_file())    
    stat_section = document('#gamepackage-receiving')    
    stat_document = pq(stat_section)    
    stat_wrapper = stat_document('div.gamepackage-away-wrap')
    
    helper = BoxscoreHelper(BASE_URL)
    
    stats = helper.build_receiving_statistics(TEAM_ID, GAME_ID, stat_wrapper)
    
    assert_that(stats).is_not_empty()
    
    assert_that(stats)\
        .contains({
            'statisticCode': 'REC',
            'playerUrl': 'https://www.espn.com/nfl/player/_/id/2573343/trevor-davis',
            'value': 3,
            'gameId': GAME_ID,
            'teamId': TEAM_ID,
            'categoryCode': 'O'
        })\
            .contains({
            'statisticCode': 'CYDS',
            'playerUrl': 'https://www.espn.com/nfl/player/_/id/2573343/trevor-davis',
            'value': 56,
            'gameId': GAME_ID,
            'teamId': TEAM_ID,
            'categoryCode': 'O'
        })\
        .contains({
            'statisticCode': 'CAVG',
            'playerUrl': 'https://www.espn.com/nfl/player/_/id/2573343/trevor-davis',
            'value': 18.7,
            'gameId': GAME_ID,
            'teamId': TEAM_ID,
            'categoryCode': 'O'
        })\
        .contains({
            'statisticCode': 'CTD',
            'playerUrl': 'https://www.espn.com/nfl/player/_/id/2573343/trevor-davis',
            'value': 0,
            'gameId': GAME_ID,
            'teamId': TEAM_ID,
            'categoryCode': 'O'
        })\
        .contains({
            'statisticCode': 'CLONG',
            'playerUrl': 'https://www.espn.com/nfl/player/_/id/2573343/trevor-davis',
            'value': 29,
            'gameId': GAME_ID,
            'teamId': TEAM_ID,
            'categoryCode': 'O'
        })\
        .contains({
            'statisticCode': 'TGTS',
            'playerUrl': 'https://www.espn.com/nfl/player/_/id/2573343/trevor-davis',
            'value': 3,
            'gameId': GAME_ID,
            'teamId': TEAM_ID,
            'categoryCode': 'O'
        })
    

def test_fumble_stats():
    """
    Tests Retrieving the fumble stats.
    """
    
    document = pq(load_test_file())    
    stat_section = document('#gamepackage-fumbles')    
    stat_document = pq(stat_section)    
    stat_wrapper = stat_document('div.gamepackage-away-wrap')
    
    helper = BoxscoreHelper(BASE_URL)
    
    stats = helper.build_fumble_statistics(TEAM_ID, GAME_ID, stat_wrapper)
    
    assert_that(stats).is_not_empty()
    
    assert_that(stats)\
        .contains({
            'statisticCode': 'FUM',
            'playerUrl': 'https://www.espn.com/nfl/player/_/id/2577189/brett-hundley',
            'value': 1,
            'gameId': GAME_ID,
            'teamId': TEAM_ID,
            'categoryCode': 'O'
        })\
            .contains({
            'statisticCode': 'FREC',
            'playerUrl': 'https://www.espn.com/nfl/player/_/id/2577189/brett-hundley',
            'value': 0,
            'gameId': GAME_ID,
            'teamId': TEAM_ID,
            'categoryCode': 'O'
        })\
        .contains({
            'statisticCode': 'FLOST',
            'playerUrl': 'https://www.espn.com/nfl/player/_/id/2577189/brett-hundley',
            'value': 1,
            'gameId': GAME_ID,
            'teamId': TEAM_ID,
            'categoryCode': 'O'
        })
        
def test_interception_stats():
    """
    Tests retrieving the interception stats
    """
    
    document = pq(load_test_file())    
    stat_section = document('#gamepackage-interceptions')    
    stat_document = pq(stat_section)    
    stat_wrapper = stat_document('div.gamepackage-home-wrap')
    
    helper = BoxscoreHelper(BASE_URL)
    
    stats = helper.build_interception_statistics(TEAM_ID, GAME_ID, stat_wrapper)
    
    assert_that(stats).is_not_empty()
    
    assert_that(stats)\
        .contains({
            'statisticCode': 'INT',
            'playerUrl': 'https://www.espn.com/nfl/player/_/id/3054951/jarrad-davis',
            'value': 1,
            'gameId': GAME_ID,
            'teamId': TEAM_ID,
            'categoryCode': 'D'
        })\
            .contains({
            'statisticCode': 'TD',
            'playerUrl': 'https://www.espn.com/nfl/player/_/id/3054951/jarrad-davis',
            'value': 0,
            'gameId': GAME_ID,
            'teamId': TEAM_ID,
            'categoryCode': 'D'
        })
    
def test_interception_stats_empty():
    """
    Tests Retreiving the Interception stats when they are empty.
    """
    
    document = pq(load_test_file())    
    stat_section = document('#gamepackage-interceptions')    
    stat_document = pq(stat_section)    
    stat_wrapper = stat_document('div.gamepackage-away-wrap')
    
    helper = BoxscoreHelper(BASE_URL)
    
    stats = helper.build_interception_statistics(TEAM_ID, GAME_ID, stat_wrapper)
    
    assert_that(stats).is_empty()

def test_defensive_stats():
    """
    Tests retrieving the Defensive stats.
    """
    document = pq(load_test_file())    
    stat_section = document('#gamepackage-defensive')    
    stat_document = pq(stat_section)    
    stat_wrapper = stat_document('div.gamepackage-home-wrap')
    
    helper = BoxscoreHelper(BASE_URL)
    
    stats = helper.build_defensive_statistics(TEAM_ID, GAME_ID, stat_wrapper)
    
    assert_that(stats).is_not_empty()
    
    assert_that(stats)\
        .contains({
            'statisticCode': 'TACK',
            'playerUrl': 'https://www.espn.com/nfl/player/_/id/3054951/jarrad-davis',
            'value': 12,
            'gameId': GAME_ID,
            'teamId': TEAM_ID,
            'categoryCode': 'D'
        })\
        .contains({
            'statisticCode': 'SOLO',
            'playerUrl': 'https://www.espn.com/nfl/player/_/id/3054951/jarrad-davis',
            'value': 8,
            'gameId': GAME_ID,
            'teamId': TEAM_ID,
            'categoryCode': 'D'
        })\
        .contains({
            'statisticCode': 'SACK',
            'playerUrl': 'https://www.espn.com/nfl/player/_/id/3054951/jarrad-davis',
            'value': 0,
            'gameId': GAME_ID,
            'teamId': TEAM_ID,
            'categoryCode': 'D'
        })\
        .contains({
            'statisticCode': 'TFL',
            'playerUrl': 'https://www.espn.com/nfl/player/_/id/3054951/jarrad-davis',
            'value': 0,
            'gameId': GAME_ID,
            'teamId': TEAM_ID,
            'categoryCode': 'D'
        })\
        .contains({
            'statisticCode': 'PD',
            'playerUrl': 'https://www.espn.com/nfl/player/_/id/3054951/jarrad-davis',
            'value': 1,
            'gameId': GAME_ID,
            'teamId': TEAM_ID,
            'categoryCode': 'D'
        })\
        .contains({
            'statisticCode': 'HITS',
            'playerUrl': 'https://www.espn.com/nfl/player/_/id/3054951/jarrad-davis',
            'value': 0,
            'gameId': GAME_ID,
            'teamId': TEAM_ID,
            'categoryCode': 'D'
        })\
        .contains({
            'statisticCode': 'TD',
            'playerUrl': 'https://www.espn.com/nfl/player/_/id/3054951/jarrad-davis',
            'value': 0,
            'gameId': GAME_ID,
            'teamId': TEAM_ID,
            'categoryCode': 'D'
        })
    
    
def test_kick_return_stats():
    """
    Tests Retrieving the Kick Return stats
    """

    document = pq(load_test_file())    
    stat_section = document('#gamepackage-kickReturns')    
    stat_document = pq(stat_section)    
    stat_wrapper = stat_document('div.gamepackage-away-wrap')
    
    helper = BoxscoreHelper(BASE_URL)
    
    stats = helper.build_kick_return_statistics(TEAM_ID, GAME_ID, stat_wrapper)
    
    assert_that(stats).is_not_empty()
    
    assert_that(stats)\
        .contains({
            'statisticCode': 'KR',
            'playerUrl': 'https://www.espn.com/nfl/player/_/id/2573343/trevor-davis',
            'value': 3,
            'gameId': GAME_ID,
            'teamId': TEAM_ID,
            'categoryCode': 'S'
        })\
        .contains({
            'statisticCode': 'KRYDS',
            'playerUrl': 'https://www.espn.com/nfl/player/_/id/2573343/trevor-davis',
            'value': 36,
            'gameId': GAME_ID,
            'teamId': TEAM_ID,
            'categoryCode': 'S'
        })\
        .contains({
            'statisticCode': 'KRAVG',
            'playerUrl': 'https://www.espn.com/nfl/player/_/id/2573343/trevor-davis',
            'value': 12,
            'gameId': GAME_ID,
            'teamId': TEAM_ID,
            'categoryCode': 'S'
        })\
        .contains({
            'statisticCode': 'KRLONG',
            'playerUrl': 'https://www.espn.com/nfl/player/_/id/2573343/trevor-davis',
            'value': 15,
            'gameId': GAME_ID,
            'teamId': TEAM_ID,
            'categoryCode': 'S'
        })\
        .contains({
            'statisticCode': 'KRTD',
            'playerUrl': 'https://www.espn.com/nfl/player/_/id/2573343/trevor-davis',
            'value': 0,
            'gameId': GAME_ID,
            'teamId': TEAM_ID,            
            'categoryCode': 'S'
        })
    
def test_punt_return_stats():
    """
    Tests Retreiving the Punt Return stats
    """
    document = pq(load_test_file())    
    stat_section = document('#gamepackage-puntReturns')    
    stat_document = pq(stat_section)    
    stat_wrapper = stat_document('div.gamepackage-away-wrap')
    
    helper = BoxscoreHelper(BASE_URL)
    
    stats = helper.build_punt_return_statistics(TEAM_ID, GAME_ID, stat_wrapper)
    
    assert_that(stats).is_not_empty()
    
    assert_that(stats)\
        .contains({
            'statisticCode': 'PR',
            'playerUrl': 'https://www.espn.com/nfl/player/_/id/2573343/trevor-davis',
            'value': 2,
            'gameId': GAME_ID,
            'teamId': TEAM_ID,            
            'categoryCode': 'S'
        })\
        .contains({
            'statisticCode': 'PRYDS',
            'playerUrl': 'https://www.espn.com/nfl/player/_/id/2573343/trevor-davis',
            'value': 46,
            'gameId': GAME_ID,
            'teamId': TEAM_ID,            
            'categoryCode': 'S'
        })\
        .contains({
            'statisticCode': 'PRAVG',
            'playerUrl': 'https://www.espn.com/nfl/player/_/id/2573343/trevor-davis',
            'value': 23,
            'gameId': GAME_ID,
            'teamId': TEAM_ID,            
            'categoryCode': 'S'
        })\
        .contains({
            'statisticCode': 'PRLONG',
            'playerUrl': 'https://www.espn.com/nfl/player/_/id/2573343/trevor-davis',
            'value': 28,
            'gameId': GAME_ID,
            'teamId': TEAM_ID,            
            'categoryCode': 'S'
        })\
        .contains({
            'statisticCode': 'PRTD',
            'playerUrl': 'https://www.espn.com/nfl/player/_/id/2573343/trevor-davis',
            'value': 0,
            'gameId': GAME_ID,
            'teamId': TEAM_ID,            
            'categoryCode': 'S'
        })
            
    
    
def test_kicking_stats():
    """
    Tests retreiving the kicking stats
    """
    document = pq(load_test_file())    
    stat_section = document('#gamepackage-kicking')    
    stat_document = pq(stat_section)    
    stat_wrapper = stat_document('div.gamepackage-away-wrap')
    
    helper = BoxscoreHelper(BASE_URL)
    
    stats = helper.build_kicking_statistics(TEAM_ID, GAME_ID, stat_wrapper)
    
    assert_that(stats).is_not_empty()
    
    assert_that(stats)\
        .contains({
            'statisticCode': 'XPA',
            'playerUrl': 'https://www.espn.com/nfl/player/_/id/10636/mason-crosby',
            'value': 0,
            'gameId': GAME_ID,
            'teamId': TEAM_ID,            
            'categoryCode': 'S'
        })\
        .contains({
            'statisticCode': 'XPM',
            'playerUrl': 'https://www.espn.com/nfl/player/_/id/10636/mason-crosby',
            'value': 0,
            'gameId': GAME_ID,
            'teamId': TEAM_ID,            
            'categoryCode': 'S'
        })\
        .contains({
            'statisticCode': 'FGA',
            'playerUrl': 'https://www.espn.com/nfl/player/_/id/10636/mason-crosby',
            'value': 1,
            'gameId': GAME_ID,
            'teamId': TEAM_ID,            
            'categoryCode': 'S'
        })\
        .contains({
            'statisticCode': 'FGM',
            'playerUrl': 'https://www.espn.com/nfl/player/_/id/10636/mason-crosby',
            'value': 1,
            'gameId': GAME_ID,
            'teamId': TEAM_ID,            
            'categoryCode': 'S'
        })\
        .contains({
            'statisticCode': 'FGLONG',
            'playerUrl': 'https://www.espn.com/nfl/player/_/id/10636/mason-crosby',
            'value': 41,
            'gameId': GAME_ID,
            'teamId': TEAM_ID,            
            'categoryCode': 'S'
        })

def test_punting_stats():
    """
    Tests retrieving the punting stats.
    """
    document = pq(load_test_file())    
    stat_section = document('#gamepackage-punting')    
    stat_document = pq(stat_section)    
    stat_wrapper = stat_document('div.gamepackage-away-wrap')
    
    helper = BoxscoreHelper(BASE_URL)
    
    stats = helper.build_punting_statistics(TEAM_ID, GAME_ID, stat_wrapper)
    
    assert_that(stats).is_not_empty()
    
    assert_that(stats)\
        .contains({
            'statisticCode': 'PUNT',
            'playerUrl': 'https://www.espn.com/nfl/player/_/id/2980123/justin-vogel',
            'value': 6,
            'gameId': GAME_ID,
            'teamId': TEAM_ID,            
            'categoryCode': 'S'
        })\
        .contains({
            'statisticCode': 'PAVG',
            'playerUrl': 'https://www.espn.com/nfl/player/_/id/2980123/justin-vogel',
            'value': 44.8,
            'gameId': GAME_ID,
            'teamId': TEAM_ID,            
            'categoryCode': 'S'
        })\
        .contains({
            'statisticCode': 'PTB',
            'playerUrl': 'https://www.espn.com/nfl/player/_/id/2980123/justin-vogel',
            'value': 1,
            'gameId': GAME_ID,
            'teamId': TEAM_ID,            
            'categoryCode': 'S'
        })\
        .contains({
            'statisticCode': 'P20',
            'playerUrl': 'https://www.espn.com/nfl/player/_/id/2980123/justin-vogel',
            'value': 1,
            'gameId': GAME_ID,
            'teamId': TEAM_ID,            
            'categoryCode': 'S'
        })\
        .contains({
            'statisticCode': 'PLONG',
            'playerUrl': 'https://www.espn.com/nfl/player/_/id/2980123/justin-vogel',
            'value': 58,
            'gameId': GAME_ID,
            'teamId': TEAM_ID,            
            'categoryCode': 'S'
        })\
        .contains({
            'statisticCode': 'PNTYDS',
            'playerUrl': 'https://www.espn.com/nfl/player/_/id/2980123/justin-vogel',
            'value': 269,
            'gameId': GAME_ID,
            'teamId': TEAM_ID,            
            'categoryCode': 'S'
        })
