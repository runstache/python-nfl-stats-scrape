"""
Tests for the MatchupHelper.
"""

from src.helpers.team import MatchupHelper
from assertpy import assert_that


TEST_FILE = './tests/test_files/teams.html'
API_URL = 'http://localhost/api'
TEAM_ID = 1
AWAY_ID = 2
GAME_ID = 323

def load_test_file() -> str:
    """
    Loads the Test File HTML

    Returns:
        str: HTML Content
    """
    
    with open(TEST_FILE, 'r', encoding='utf-8') as test_file:
        return test_file.read()
    
def test_passing_first_downs():
    """
    Tests retrieving the first downs from the stats.
    """
    
    doc = load_test_file()
    helper = MatchupHelper(doc, API_URL)
    
    stats = helper.build_team_stats(TEAM_ID, AWAY_ID, GAME_ID)
    
    assert_that(stats).contains({
            'statisticCode': 'P1D',            
            'value': 14,
            'gameId': GAME_ID,
            'teamId': TEAM_ID,
            'categoryCode': 'O'
    })\
    .contains({
            'statisticCode': 'P1D',            
            'value': 15,
            'gameId': GAME_ID,
            'teamId': AWAY_ID,
            'categoryCode': 'O'
    })

def test_rushing_first_downs():
    """
    Tests retrieiving Rushing First downs
    """
    
    doc = load_test_file()
    helper = MatchupHelper(doc, API_URL)
    
    stats = helper.build_team_stats(TEAM_ID, AWAY_ID, GAME_ID)
    
    assert_that(stats).contains({
            'statisticCode': 'R1D',            
            'value': 3,
            'gameId': GAME_ID,
            'teamId': TEAM_ID,
            'categoryCode': 'O'
    })\
    .contains({
            'statisticCode': 'R1D',            
            'value': 7,
            'gameId': GAME_ID,
            'teamId': AWAY_ID,
            'categoryCode': 'O'
    })
    
def test_third_down_efficiency():
    """
    Tests retrieving the 3rd Down Efficiency
    """    
    doc = load_test_file()
    helper = MatchupHelper(doc, API_URL)
    
    stats = helper.build_team_stats(TEAM_ID, AWAY_ID, GAME_ID)
    
    assert_that(stats).contains({
            'statisticCode': '3DA',            
            'value': 13,
            'gameId': GAME_ID,
            'teamId': TEAM_ID,
            'categoryCode': 'O'
    })\
    .contains({
            'statisticCode': '3DA',            
            'value': 10,
            'gameId': GAME_ID,
            'teamId': AWAY_ID,
            'categoryCode': 'O'
    })\
    .contains({
            'statisticCode': '3DC',            
            'value': 6,
            'gameId': GAME_ID,
            'teamId': TEAM_ID,
            'categoryCode': 'O'
    })\
    .contains({
            'statisticCode': '3DC',            
            'value': 9,
            'gameId': GAME_ID,
            'teamId': AWAY_ID,
            'categoryCode': 'O'
    })
    
def test_fourth_down_conversion():
    """
    Tests getting fourth down conversion rate.
    """
    
    doc = load_test_file()
    helper = MatchupHelper(doc, API_URL)
    
    stats = helper.build_team_stats(TEAM_ID, AWAY_ID, GAME_ID)
    
    assert_that(stats).contains({
            'statisticCode': '4DA',            
            'value': 3,
            'gameId': GAME_ID,
            'teamId': TEAM_ID,
            'categoryCode': 'O'
    })\
    .contains({
            'statisticCode': '4DA',            
            'value': 0,
            'gameId': GAME_ID,
            'teamId': AWAY_ID,
            'categoryCode': 'O'
    })\
    .contains({
            'statisticCode': '4DC',            
            'value': 2,
            'gameId': GAME_ID,
            'teamId': TEAM_ID,
            'categoryCode': 'O'
    })\
    .contains({
            'statisticCode': '4DC',            
            'value': 0,
            'gameId': GAME_ID,
            'teamId': AWAY_ID,
            'categoryCode': 'O'
    })
    
def test_total_plays():
    """
    Tests getting the total plays
    """
    
    doc = load_test_file()
    helper = MatchupHelper(doc, API_URL)
    
    stats = helper.build_team_stats(TEAM_ID, AWAY_ID, GAME_ID)
    
    assert_that(stats).contains({
            'statisticCode': 'PLAY',            
            'value': 66,
            'gameId': GAME_ID,
            'teamId': TEAM_ID,
            'categoryCode': 'O'
    })\
    .contains({
            'statisticCode': 'PLAY',            
            'value': 58,
            'gameId': GAME_ID,
            'teamId': AWAY_ID,
            'categoryCode': 'O'
    })

def test_total_yards():
    """
    Tests getting the total yards
    """
    
    doc = load_test_file()
    helper = MatchupHelper(doc, API_URL)
    
    stats = helper.build_team_stats(TEAM_ID, AWAY_ID, GAME_ID)
    
    assert_that(stats).contains({
            'statisticCode': 'YDS',            
            'value': 243,
            'gameId': GAME_ID,
            'teamId': TEAM_ID,
            'categoryCode': 'O'
    })\
    .contains({
            'statisticCode': 'YDS',            
            'value': 413,
            'gameId': GAME_ID,
            'teamId': AWAY_ID,
            'categoryCode': 'O'
    })
    
def test_total_drives():
    """
    Tests getting the total drives
    """
    
    doc = load_test_file()
    helper = MatchupHelper(doc, API_URL)
    
    stats = helper.build_team_stats(TEAM_ID, AWAY_ID, GAME_ID)
    
    assert_that(stats).contains({
            'statisticCode': 'DRV',            
            'value': 10,
            'gameId': GAME_ID,
            'teamId': TEAM_ID,
            'categoryCode': 'O'
    })\
    .contains({
            'statisticCode': 'DRV',            
            'value': 10,
            'gameId': GAME_ID,
            'teamId': AWAY_ID,
            'categoryCode': 'O'
    })
    
def test_yards_per_play():
    """
    Tests getting the yards per play
    """
    
    doc = load_test_file()
    helper = MatchupHelper(doc, API_URL)
    
    stats = helper.build_team_stats(TEAM_ID, AWAY_ID, GAME_ID)
    
    assert_that(stats).contains({
            'statisticCode': 'YPP',            
            'value': 3.7,
            'gameId': GAME_ID,
            'teamId': TEAM_ID,
            'categoryCode': 'O'
    })\
    .contains({
            'statisticCode': 'YPP',            
            'value': 7.1,
            'gameId': GAME_ID,
            'teamId': AWAY_ID,
            'categoryCode': 'O'
    })

def test_total_passing():
    """
    Tests getting total passing yards
    """
    
    doc = load_test_file()
    helper = MatchupHelper(doc, API_URL)
    
    stats = helper.build_team_stats(TEAM_ID, AWAY_ID, GAME_ID)
    
    assert_that(stats).contains({
            'statisticCode': 'PYDS',            
            'value': 191,
            'gameId': GAME_ID,
            'teamId': TEAM_ID,
            'categoryCode': 'O'
    })\
    .contains({
            'statisticCode': 'PYDS',            
            'value': 292,
            'gameId': GAME_ID,
            'teamId': AWAY_ID,
            'categoryCode': 'O'
    })
    
def test_passing_efficiency():
    """
    Tests getting the passing efficiency.
    """
    
    doc = load_test_file()
    helper = MatchupHelper(doc, API_URL)
    
    stats = helper.build_team_stats(TEAM_ID, AWAY_ID, GAME_ID)
    
    assert_that(stats).contains({
            'statisticCode': 'PC',            
            'value': 29,
            'gameId': GAME_ID,
            'teamId': TEAM_ID,
            'categoryCode': 'O'
    })\
    .contains({
            'statisticCode': 'PC',            
            'value': 26,
            'gameId': GAME_ID,
            'teamId': AWAY_ID,
            'categoryCode': 'O'
    })\
    .contains({
            'statisticCode': 'PA',            
            'value': 41,
            'gameId': GAME_ID,
            'teamId': TEAM_ID,
            'categoryCode': 'O'
    })\
    .contains({
            'statisticCode': 'PA',            
            'value': 31,
            'gameId': GAME_ID,
            'teamId': AWAY_ID,
            'categoryCode': 'O'
    })

def test_yards_per_pass():
    """
    Tests get yards per pass
    """
    
    doc = load_test_file()
    helper = MatchupHelper(doc, API_URL)
    
    stats = helper.build_team_stats(TEAM_ID, AWAY_ID, GAME_ID)
    
    assert_that(stats).contains({
            'statisticCode': 'PSAVG',            
            'value': 4.0,
            'gameId': GAME_ID,
            'teamId': TEAM_ID,
            'categoryCode': 'O'
    })\
    .contains({
            'statisticCode': 'PSAVG',            
            'value': 8.8,
            'gameId': GAME_ID,
            'teamId': AWAY_ID,
            'categoryCode': 'O'
    })
    
def test_passing_interceptions():
    """
    Tests get passing interceptions
    """
    
    doc = load_test_file()
    helper = MatchupHelper(doc, API_URL)
    
    stats = helper.build_team_stats(TEAM_ID, AWAY_ID, GAME_ID)
    
    assert_that(stats).contains({
            'statisticCode': 'PINT',            
            'value': 3,
            'gameId': GAME_ID,
            'teamId': TEAM_ID,
            'categoryCode': 'O'
    })\
    .contains({
            'statisticCode': 'PINT',            
            'value': 2,
            'gameId': GAME_ID,
            'teamId': AWAY_ID,
            'categoryCode': 'O'
    })

def test_rushing_yards():
    """
    Tests get rushing yards.
    """
    
    doc = load_test_file()
    helper = MatchupHelper(doc, API_URL)
    
    stats = helper.build_team_stats(TEAM_ID, AWAY_ID, GAME_ID)
    
    assert_that(stats).contains({
            'statisticCode': 'RYDS',            
            'value': 52,
            'gameId': GAME_ID,
            'teamId': TEAM_ID,
            'categoryCode': 'O'
    })\
    .contains({
            'statisticCode': 'RYDS',            
            'value': 121,
            'gameId': GAME_ID,
            'teamId': AWAY_ID,
            'categoryCode': 'O'
    })
    
def test_rushing_attempts():
    """
    Tests get rushing attempts
    """
    
    doc = load_test_file()
    helper = MatchupHelper(doc, API_URL)
    
    stats = helper.build_team_stats(TEAM_ID, AWAY_ID, GAME_ID)
    
    assert_that(stats).contains({
            'statisticCode': 'RCAR',            
            'value': 18,
            'gameId': GAME_ID,
            'teamId': TEAM_ID,
            'categoryCode': 'O'
    })\
    .contains({
            'statisticCode': 'RCAR',            
            'value': 25,
            'gameId': GAME_ID,
            'teamId': AWAY_ID,
            'categoryCode': 'O'
    })
    
def test_yards_per_rush():
    """
    Test get yards per rush
    """
    
    doc = load_test_file()
    helper = MatchupHelper(doc, API_URL)
    
    stats = helper.build_team_stats(TEAM_ID, AWAY_ID, GAME_ID)
    
    assert_that(stats).contains({
            'statisticCode': 'RAVG',            
            'value': 2.9,
            'gameId': GAME_ID,
            'teamId': TEAM_ID,
            'categoryCode': 'O'
    })\
    .contains({
            'statisticCode': 'RAVG',            
            'value': 4.8,
            'gameId': GAME_ID,
            'teamId': AWAY_ID,
            'categoryCode': 'O'
    })

def test_red_zone_efficiency():
    """
    Tests get redzone efficiency
    """
    
    doc = load_test_file()
    helper = MatchupHelper(doc, API_URL)
    
    stats = helper.build_team_stats(TEAM_ID, AWAY_ID, GAME_ID)
    
    assert_that(stats).contains({
            'statisticCode': 'RZA',            
            'value': 2,
            'gameId': GAME_ID,
            'teamId': TEAM_ID,
            'categoryCode': 'O'
    })\
    .contains({
            'statisticCode': 'RZA',            
            'value': 2,
            'gameId': GAME_ID,
            'teamId': AWAY_ID,
            'categoryCode': 'O'
    })\
    .contains({
            'statisticCode': 'RZC',            
            'value': 1,
            'gameId': GAME_ID,
            'teamId': TEAM_ID,
            'categoryCode': 'O'
    })\
    .contains({
            'statisticCode': 'RZC',            
            'value': 2,
            'gameId': GAME_ID,
            'teamId': AWAY_ID,
            'categoryCode': 'O'
    })
    
def test_penalties():
    """
    Test get penalties
    """

    doc = load_test_file()
    helper = MatchupHelper(doc, API_URL)
    
    stats = helper.build_team_stats(TEAM_ID, AWAY_ID, GAME_ID)
    
    assert_that(stats).contains({
            'statisticCode': 'PEN',            
            'value': 4,
            'gameId': GAME_ID,
            'teamId': TEAM_ID,
            'categoryCode': 'T'
    })\
    .contains({
            'statisticCode': 'PEN',            
            'value': 5,
            'gameId': GAME_ID,
            'teamId': AWAY_ID,
            'categoryCode': 'T'
    })\
    .contains({
            'statisticCode': 'PENYDS',            
            'value': 30,
            'gameId': GAME_ID,
            'teamId': TEAM_ID,
            'categoryCode': 'T'
    })\
    .contains({
            'statisticCode': 'PENYDS',            
            'value': 35,
            'gameId': GAME_ID,
            'teamId': AWAY_ID,
            'categoryCode': 'T'
    })
    
def test_defensive_touchdowns():
    """
    Test get defensive touchdowns
    """
    
    doc = load_test_file()
    helper = MatchupHelper(doc, API_URL)
    
    stats = helper.build_team_stats(TEAM_ID, AWAY_ID, GAME_ID)
    
    assert_that(stats).contains({
            'statisticCode': 'TD',            
            'value': 0,
            'gameId': GAME_ID,
            'teamId': TEAM_ID,
            'categoryCode': 'D'
    })\
    .contains({
            'statisticCode': 'TD',            
            'value': 0,
            'gameId': GAME_ID,
            'teamId': AWAY_ID,
            'categoryCode': 'D'
    })

def test_time_of_possesion():
    """
    Test get time of possession
    """
    
    doc = load_test_file()
    helper = MatchupHelper(doc, API_URL)
    
    stats = helper.build_team_stats(TEAM_ID, AWAY_ID, GAME_ID)
    
    assert_that(stats).contains({
            'statisticCode': 'TOP',            
            'value': 1726,
            'gameId': GAME_ID,
            'teamId': TEAM_ID,
            'categoryCode': 'T'
    })\
    .contains({
            'statisticCode': 'TOP',            
            'value': 1874,
            'gameId': GAME_ID,
            'teamId': AWAY_ID,
            'categoryCode': 'T'
    })
    
def test_get_turnovers():
    """
    Test get Turnovers.
    """
    
    doc = load_test_file()
    helper = MatchupHelper(doc, API_URL)
    
    stats = helper.build_team_stats(TEAM_ID, AWAY_ID, GAME_ID)
    
    assert_that(stats).contains({
            'statisticCode': 'TO',            
            'value': 3,
            'gameId': GAME_ID,
            'teamId': TEAM_ID,
            'categoryCode': 'T'
    })\
    .contains({
            'statisticCode': 'TO',            
            'value': 4,
            'gameId': GAME_ID,
            'teamId': AWAY_ID,
            'categoryCode': 'T'
    })
        