"""
Schedule Helper Tests
"""

from src.helpers.schedule import ScheduleHelper
from assertpy import assert_that

SCHEDULE_DOCUMENT = './tests/test_files/schedule.html'

def load_test_file() -> str:
    """
    Loads the Test File.

    Returns:
        str: Test File data
    """
    
    with open(SCHEDULE_DOCUMENT, 'r', encoding='utf-8') as input_file:
        return input_file.read()


def test_get_schedule_entries():
    """
    Schedule Entry Retrieval Test
    """
    
    schedule_doc = load_test_file()
    
    helper = ScheduleHelper(schedule_doc)
    
    schedules = helper.get_schedule_entries(1,2022,'1')
    
    assert_that(schedules).is_length(32)
    
    # VALIDATE WE'RE GETTING BOTH SIDES FOR SCHEDULE ENTRIES.
    assert_that(schedules).contains({
        'teamUrl': 'https://www.espn.com/nfl/team/_/name/nyg/new-york-giants',
        'opponentUrl': 'https://www.espn.com/nfl/team/_/name/ne/new-england-patriots',
        'year': 2022,
        'week': 1,
        'gameId' : 401439619,
        'url': 'https://www.espn.com/nfl/game?gameId=401439619',
        'typeCode': '1',
        'homeGame': True
    })\
    .contains({
        'teamUrl': 'https://www.espn.com/nfl/team/_/name/ne/new-england-patriots',
        'opponentUrl': 'https://www.espn.com/nfl/team/_/name/nyg/new-york-giants',
        'year': 2022,
        'week': 1,
        'gameId' : 401439619,
        'url': 'https://www.espn.com/nfl/game?gameId=401439619',
        'typeCode': '1',
        'homeGame': False
    })
    
    
    
    
    
    