"""
Tests for the MatchupHelper.
"""

from assertpy import assert_that

from src.helpers.team import MatchUpHelper
import json
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker

from football_data.models import Team, Statistic, Schedule, StatisticCategory, StatisticCode
from football_data.repositories import StatisticCodeRepository
import csv

TEST_FILE = './tests/test_files/matchup-stats.json'
STATS_CODES = './tests/test_files/team_statistic_codes.csv'


def load_test_file() -> dict:
    """
    Loads the Test File HTML

    Returns:
        str: HTML Content
    """

    with open(TEST_FILE, 'r', encoding='utf-8') as test_file:
        return json.load(test_file)


def load_stats_codes(maker: sessionmaker) -> None:
    """
    Loads the Statistic Codes into the session.
    Args:
        maker: session maker
    Returns: None
    """

    repo = StatisticCodeRepository(maker)
    csv.register_dialect('input', delimiter=',')
    with open(STATS_CODES, 'r', encoding='utf-8') as input_file:
        reader: list[dict] = list(
            csv.DictReader(input_file, dialect='input'))
        for item in reader:
            code = StatisticCode(code=item.get('code', ''), description=item.get('description', ''),
                                 grouping=item.get('grouping', ''))
            repo.save(code)


def build_maker() -> sessionmaker:
    """
    Builds a session maker.
    Returns: Session Maker

    """

    engine = create_engine("sqlite://")
    StatisticCode.metadata.create_all(bind=engine)
    StatisticCategory.metadata.create_all(bind=engine)
    return sessionmaker(bind=engine, expire_on_commit=False)


def test_build_statistic():
    """
    Tests building a Statistic.
    """
    maker = build_maker()
    payload = load_test_file()
    team_stats = payload.get('tmStats', {})
    home_stats = team_stats.get('home', {}).get('s', {})

    stat_repo = StatisticCodeRepository(maker)
    stat_repo.save(StatisticCode(code='DTD', description='Defensive Touchdowns', grouping='team'))
    stat_repo.save(StatisticCategory(code='T', description='Team'))

    helper = MatchUpHelper(maker)
    result = helper.build_statistic(home_stats.get('defensiveTouchdowns', {}), 'DTD', 1, 1)

    assert_that(result).is_not_none()
    assert_that([result]).extracting('value').contains(1)


def test_build_statistic_split_value():
    """
    Tests Building a Statistic with a split value
    """
    maker = build_maker()
    payload = load_test_file()
    team_stats = payload.get('tmStats', {})
    home_stats = team_stats.get('home', {}).get('s', {})

    stat_repo = StatisticCodeRepository(maker)
    pa_code = StatisticCode(code='PA', description='Passing Attemtps', grouping='team')
    stat_repo.save(pa_code)
    pc_code = StatisticCode(code='PC', description='Passing Completions', grouping='team')
    stat_repo.save(pc_code)
    stat_repo.save(StatisticCategory(code='T', description='Team'))

    helper = MatchUpHelper(maker)
    results = helper.build_split_statistic(home_stats.get('completionAttempts', {}), ['PC', 'PA'],
                                           1, 1)

    assert_that(results).is_not_empty()
    assert_that(list(filter(lambda x: x.value == 33 and x.statistic_code_id == pa_code.id,
                            results))).is_not_empty()
    assert_that(
        list(filter(lambda x: x.value == 20 and x.statistic_code_id == pc_code.id,
                    results))).is_not_empty()


def test_build_statistic_no_value():
    """
    Tests building a statistic with no entry value.
    """
    maker = build_maker()
    stat_repo = StatisticCodeRepository(maker)
    stat_repo.save(StatisticCode(code='PA', description='Passing Attemtps', grouping='team'))
    stat_repo.save(StatisticCode(code='PC', description='Passing Completions', grouping='team'))
    stat_repo.save(StatisticCategory(code='T', description='Team'))

    helper = MatchUpHelper(maker)
    results = helper.build_split_statistic({'l': 'Comp-Att', 'n': 'completionAttempts'},
                                           ['PC', 'PA'],
                                           1, 1)

    assert_that(results).is_empty()


def test_generate_statistics():
    """
    Tests Generating the statistics.
    """

    maker = build_maker()
    load_stats_codes(maker)
    repo = StatisticCodeRepository(maker)
    repo.save(StatisticCategory(code='T', description='Team'))
    payload = load_test_file()
    team_stats = payload.get('tmStats', {})
    home_stats = team_stats.get('home', {}).get('s', {})
    helper = MatchUpHelper(maker)

    result = helper.generate_stats(1, 1, home_stats)
    assert_that(result).is_not_empty().is_length(26)


def test_convert_value():
    """
    Tests converting the Value.
    """
    assert_that(MatchUpHelper.convert_value('10')).is_equal_to(10)


def test_convert_value_not_numeric():
    """
    Tests converting a non-numeric value.
    """
    assert_that(MatchUpHelper.convert_value('A')).is_zero()


def test_convert_value_time():
    """
    Tests converting a time value to total seconds.
    """

    assert_that(MatchUpHelper.convert_value('1:10')).is_equal_to(70)
