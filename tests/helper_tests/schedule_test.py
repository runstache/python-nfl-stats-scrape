"""
Schedule Helper Tests
"""

from src.helpers.schedule import ScheduleHelper
from assertpy import assert_that
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from football_data.models import Team, Schedule
from football_data.repositories import TeamRepository
import json


def load_event() -> dict:
    """
    Loads the Test file to dictionary.
    """
    with open('./tests/test_files/event.json', 'r', encoding='utf-8') as input_file:
        return json.load(input_file)


def create_maker() -> sessionmaker:
    """
    Creates a Session Maker
    """
    engine = create_engine('sqlite://')
    Team.metadata.create_all(bind=engine)
    Schedule.metadata.create_all(bind=engine)
    return sessionmaker(bind=engine, expire_on_commit=False)


def test_convert_event():
    """
    Tests converting the Event to Schedule Items.
    """
    event = load_event()
    maker = create_maker()

    repo = TeamRepository(maker)
    repo.save(Team(code='LAR', name='Los Angeles Rams', url='rams.com'))
    repo.save(Team(code='BUF', name='Buffalo Bills', url='bills.com'))

    helper = ScheduleHelper(maker)

    result = helper.convert_event(event, 1, 1, 2022)

    assert_that(result).is_not_empty().is_length(2)
    assert_that(result).extracting('game_id').contains(401437654)
    assert_that(list(filter(lambda x: x.team_id != x.opponent_id, result))).is_not_empty()


def test_convert_event_no_teams():
    """
    Tests Converting the Event that has no teams.
    """

    event = load_event()
    maker = create_maker()
    event['teams'] = []

    helper = ScheduleHelper(maker)
    result = helper.convert_event(event, 1, 1, 2022)
    assert_that(result).is_empty()
