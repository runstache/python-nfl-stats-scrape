"""
Tests for the Box score helper.
"""

from assertpy import assert_that
from football_data.models import Player, Statistic, StatisticCode, StatisticCategory
from football_data.repositories import StatisticCodeRepository
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.helpers.box_score import BoxScoreHelper


def build_maker() -> sessionmaker:
    engine = create_engine('sqlite://')
    Player.metadata.create_all(bind=engine)
    Statistic.metadata.create_all(bind=engine)
    StatisticCode.metadata.create_all(bind=engine)
    StatisticCategory.metadata.create_all(bind=engine)
    return sessionmaker(bind=engine, expire_on_commit=False)


def filter_by_code(stats: list[Statistic],
                   codes: list[StatisticCode], code: str, value: float) -> list[Statistic]:
    """
    Filters the Stats List by Code
    Args:
        stats: list of Stats
        codes: List of Stat Codes
        code: Stat Code
        value: Value

    Returns: List of Matching items
    """
    filtered_code = list(filter(lambda x: x.code == code, codes))
    assert_that(filtered_code).is_not_empty()
    code_item = filtered_code[0]

    return list(filter(lambda s: s.statistic_code_id == code_item.id and s.value == value, stats))


def test_build_passing_stats():
    """
    Tests building the passing stats.
    """
    maker = build_maker()
    stat_code_repo = StatisticCodeRepository(maker)

    stat_code_repo.save(
        StatisticCode(code='PC', description='Passing Completions', grouping='passing'))
    stat_code_repo.save(
        StatisticCode(code='PA', description='Passing Attempts', grouping='passing'))
    stat_code_repo.save(StatisticCode(code='YDS', description='Passing Yards', grouping='passing'))
    stat_code_repo.save(
        StatisticCode(code='TD', description='Passing Touchdowns', grouping='passing'))
    stat_code_repo.save(
        StatisticCode(code='INT', description='Passing Interceptions', grouping='passing'))
    stat_code_repo.save(
        StatisticCode(code='QBR', description='Passing Attempts', grouping='passing'))
    stat_code_repo.save(StatisticCode(code='RTG', description='Rating', grouping='passing'))
    stat_code_repo.save(StatisticCategory(code='O', description='Offense'))
    stat_code_repo.save(Player(name='Jameis Winston',
                               url='http://www.espn.com/nfl/player/_/id/2969939/jameis-winston'))

    codes = stat_code_repo.get_statistic_codes()
    section = {
        "athlts": [
            {
                "athlt": {
                    "dspNm": "Jameis Winston",
                    "guid": "57af2581-cec9-d5a3-2afe-7a719925f78b",
                    "id": "2969939",
                    "lnk": "http://www.espn.com/nfl/player/_/id/2969939/jameis-winston",
                    "uid": "s:20~l:28~a:2969939"
                },
                "stats": [
                    "23/34",
                    "269",
                    "7.9",
                    "2",
                    "0",
                    "4-35",
                    "50.3",
                    "111.0"
                ]
            }
        ],
        "keys": [
            "completions/passingAttempts",
            "passingYards",
            "yardsPerPassAttempt",
            "passingTouchdowns",
            "interceptions",
            "sacks-sackYardsLost",
            "adjQBR",
            "QBRating"
        ],
        "lbls": [
            "C/ATT",
            "YDS",
            "AVG",
            "TD",
            "INT",
            "SACKS",
            "QBR",
            "RTG"
        ],
        "text": "New Orleans Passing",
        "ttls": [
            "23/34",
            "234",
            "7.9",
            "2",
            "0",
            "4-35",
            "--",
            "111.0"
        ],
        "type": "passing"
    }
    helper = BoxScoreHelper(maker, codes)
    results = helper.build_passing_stats(section, 1)
    assert_that(filter_by_code(results, codes, 'PA', 34.0)).is_not_empty()
    assert_that(filter_by_code(results, codes, 'PC', 23.0)).is_not_empty()
    assert_that(filter_by_code(results, codes, 'YDS', 269.0)).is_not_empty()
    assert_that(filter_by_code(results, codes, 'TD', 2.0)).is_not_empty()
    assert_that(filter_by_code(results, codes, 'INT', 0.0)).is_not_empty()
    assert_that(filter_by_code(results, codes, 'QBR', 50.3)).is_not_empty()
    assert_that(filter_by_code(results, codes, 'RTG', 111.0)).is_not_empty()


def test_build_rushing_stats():
    """
    Tests Building Rushing Stats.
    """
    maker = build_maker()
    stat_code_repo = StatisticCodeRepository(maker)

    stat_code_repo.save(StatisticCode(code='YDS', description='Rushing Yards', grouping='rushing'))
    stat_code_repo.save(
        StatisticCode(code='TD', description='Rushing Touchdowns', grouping='rushing'))
    stat_code_repo.save(
        StatisticCode(code='CAR', description='Rushing Carries', grouping='rushing'))
    stat_code_repo.save(StatisticCode(code='LONG', description='Longest Rush', grouping='rushing'))
    stat_code_repo.save(
        StatisticCode(code='AVG', description='Rushing Average', grouping='rushing'))
    stat_code_repo.save(StatisticCategory(code='O', description='Offense'))
    stat_code_repo.save(Player(name='Taysom Hill',
                               url='http://www.espn.com/nfl/player/_/id/2468609/taysom-hill'))

    codes = stat_code_repo.get_statistic_codes()
    section = {
        "athlts": [
            {
                "athlt": {
                    "dspNm": "Taysom Hill",
                    "guid": "b4348fe9-fd28-0531-ad90-dbc8d5e0d11e",
                    "id": "2468609",
                    "lnk": "http://www.espn.com/nfl/player/_/id/2468609/taysom-hill",
                    "uid": "s:20~l:28~a:2468609"
                },
                "stats": [
                    "4",
                    "81",
                    "20.3",
                    "1",
                    "57"
                ]
            }
        ],
        "keys": [
            "rushingAttempts",
            "rushingYards",
            "yardsPerRushAttempt",
            "rushingTouchdowns",
            "longRushing"
        ],
        "lbls": [
            "CAR",
            "YDS",
            "AVG",
            "TD",
            "LONG"
        ],
        "text": "New Orleans Rushing",
        "ttls": [
            "19",
            "151",
            "7.9",
            "1",
            "57"
        ],
        "type": "rushing"
    }
    helper = BoxScoreHelper(maker, codes)
    results = helper.build_rushing_stats(section, 1)
    assert_that(filter_by_code(results, codes, 'CAR', 4.0)).is_not_empty()
    assert_that(filter_by_code(results, codes, 'YDS', 81.0)).is_not_empty()
    assert_that(filter_by_code(results, codes, 'TD', 1.0)).is_not_empty()
    assert_that(filter_by_code(results, codes, 'AVG', 20.3)).is_not_empty()
    assert_that(filter_by_code(results, codes, 'LONG', 57.0)).is_not_empty()


def test_build_receiving_stats():
    """
    Test building Receiving Stats
    """
    maker = build_maker()
    stat_code_repo = StatisticCodeRepository(maker)

    stat_code_repo.save(StatisticCode(code='REC', description='Receptions', grouping='receiving'))
    stat_code_repo.save(
        StatisticCode(code='YDS', description='Receiving Yards', grouping='receiving'))
    stat_code_repo.save(
        StatisticCode(code='AVG', description='Receiving Average', grouping='receiving'))
    stat_code_repo.save(
        StatisticCode(code='TD', description='Receiving Touchdowns', grouping='receiving'))
    stat_code_repo.save(
        StatisticCode(code='LONG', description='Long Reception', grouping='receiving'))
    stat_code_repo.save(StatisticCode(code='TGTS', description='Targets', grouping='receiving'))
    stat_code_repo.save(StatisticCategory(code='O', description='Offense'))
    stat_code_repo.save(Player(name='Jarvis Landry',
                               url='http://www.espn.com/nfl/player/_/id/16790/jarvis-landry'))
    codes = stat_code_repo.get_statistic_codes()
    section = {
        "athlts": [
            {
                "athlt": {
                    "dspNm": "Jarvis Landry",
                    "guid": "b97e3db7-5579-cd1a-31c6-5a6301915701",
                    "id": "16790",
                    "lnk": "http://www.espn.com/nfl/player/_/id/16790/jarvis-landry",
                    "uid": "s:20~l:28~a:16790"
                },
                "stats": [
                    "7",
                    "114",
                    "16.3",
                    "0",
                    "40",
                    "9"
                ]
            }
        ],
        "keys": [
            "receptions",
            "receivingYards",
            "yardsPerReception",
            "receivingTouchdowns",
            "longReception",
            "receivingTargets"
        ],
        "lbls": [
            "REC",
            "YDS",
            "AVG",
            "TD",
            "LONG",
            "TGTS"
        ],
        "text": "New Orleans Receiving",
        "ttls": [
            "23",
            "269",
            "11.7",
            "2",
            "40",
            "32"
        ],
        "type": "receiving"
    }
    helper = BoxScoreHelper(maker, codes)
    results = helper.build_receiving_stats(section, 1)
    assert_that(filter_by_code(results, codes, 'REC', 7.0)).is_not_empty()
    assert_that(filter_by_code(results, codes, 'YDS', 114.0)).is_not_empty()
    assert_that(filter_by_code(results, codes, 'TD', 0)).is_not_empty()
    assert_that(filter_by_code(results, codes, 'AVG', 16.3)).is_not_empty()
    assert_that(filter_by_code(results, codes, 'LONG', 40.0)).is_not_empty()
    assert_that(filter_by_code(results, codes, 'TGTS', 9.0)).is_not_empty()


def test_build_interception_stats():
    """
    Tests building Interception Stats
    """
    maker = build_maker()
    stat_code_repo = StatisticCodeRepository(maker)

    stat_code_repo.save(StatisticCode(code='INT', description='Interceptions', grouping='general'))
    stat_code_repo.save(StatisticCategory(code='D', description='Defense'))
    stat_code_repo.save(Player(name='Jarvis Landry',
                               url='http://www.espn.com/nfl/player/_/id/16790/jarvis-landry'))
    codes = stat_code_repo.get_statistic_codes()
    section = {
        "athlts": [{
            "athlt": {
                "dspNm": "Jarvis Landry",
                "guid": "b97e3db7-5579-cd1a-31c6-5a6301915701",
                "id": "16790",
                "lnk": "http://www.espn.com/nfl/player/_/id/16790/jarvis-landry",
                "uid": "s:20~l:28~a:16790"
            },
            "stats": [
                "2",
                "25",
                "1"

            ]
        }],
        "keys": [
            "interceptions",
            "interceptionYards",
            "interceptionTouchdowns"
        ],
        "lbls": [
            "INT",
            "YDS",
            "TD"
        ],
        "text": "New Orleans Interceptions",
        "ttls": [],
        "type": "interceptions"
    }
    helper = BoxScoreHelper(maker, codes)
    results = helper.build_interception_stats(section, 1)
    assert_that(filter_by_code(results, codes, 'INT', 2)).is_not_empty()


def test_build_defensive_stats():
    """
    Tests Building Defensive Stats.
    """
    maker = build_maker()
    stat_code_repo = StatisticCodeRepository(maker)

    stat_code_repo.save(StatisticCode(code='TOT', description='Tackles', grouping='defensive'))
    stat_code_repo.save(
        StatisticCode(code='SOLO', description='Solo Tackles', grouping='defensive'))
    stat_code_repo.save(StatisticCode(code='SACKS', description='Sacks', grouping='defensive'))
    stat_code_repo.save(
        StatisticCode(code='TFL', description='Tackles for Loss', grouping='defensive'))
    stat_code_repo.save(
        StatisticCode(code='PD', description='Passes Defended', grouping='defensive'))
    stat_code_repo.save(StatisticCode(code='QBHTS', description='QB Hits', grouping='defensive'))
    stat_code_repo.save(
        StatisticCode(code='TD', description='Defensive Touchdowns', grouping='defensive'))
    stat_code_repo.save(StatisticCategory(code='D', description='Defense'))
    stat_code_repo.save(Player(name='Pete Werner',
                               url='http://www.espn.com/nfl/player/_/id/4241993/pete-werner'))
    codes = stat_code_repo.get_statistic_codes()
    section = {
        "athlts": [
            {
                "athlt": {
                    "dspNm": "Pete Werner",
                    "guid": "277bb1de-8f40-0354-dbb2-4af31ec07405",
                    "id": "4241993",
                    "lnk": "http://www.espn.com/nfl/player/_/id/4241993/pete-werner",
                    "uid": "s:20~l:28~a:4241993"
                },
                "stats": [
                    "13",
                    "12",
                    "0",
                    "1",
                    "0",
                    "0",
                    "0"
                ]
            }
        ],
        "keys": [
            "totalTackles",
            "soloTackles",
            "sacks",
            "tacklesForLoss",
            "passesDefended",
            "QBHits",
            "defensiveTouchdowns"
        ],
        "lbls": [
            "TOT",
            "SOLO",
            "SACKS",
            "TFL",
            "PD",
            "QB HTS",
            "TD"
        ],
        "text": "New Orleans Defensive",
        "ttls": [
            "72",
            "55",
            "0",
            "2",
            "2",
            "1",
            "0"
        ],
        "type": "defensive"
    }
    helper = BoxScoreHelper(maker, codes)
    results = helper.build_defensive_stats(section, 1)
    assert_that(filter_by_code(results, codes, 'TOT', 13)).is_not_empty()
    assert_that(filter_by_code(results, codes, 'SOLO', 12)).is_not_empty()
    assert_that(filter_by_code(results, codes, 'SACKS', 0)).is_not_empty()
    assert_that(filter_by_code(results, codes, 'TFL', 1)).is_not_empty()
    assert_that(filter_by_code(results, codes, 'PD', 0)).is_not_empty()
    assert_that(filter_by_code(results, codes, 'QBHTS', 0)).is_not_empty()
    assert_that(filter_by_code(results, codes, 'TD', 0)).is_not_empty()


def test_build_fumble_stats():
    """
    Tests Building Fumble Stats
    """
    maker = build_maker()
    stat_code_repo = StatisticCodeRepository(maker)

    stat_code_repo.save(StatisticCode(code='FUM', description='Fumbles', grouping='general'))
    stat_code_repo.save(StatisticCategory(code='O', description='Offense'))
    stat_code_repo.save(Player(name='Mark Ingram II',
                               url='http://www.espn.com/nfl/player/_/id/13981/mark-ingram-ii'))
    codes = stat_code_repo.get_statistic_codes()
    section = {
        "athlts": [
            {
                "athlt": {
                    "dspNm": "Mark Ingram II",
                    "guid": "b7122d38-15a6-0ef3-9f2b-d40b70b89b30",
                    "id": "13981",
                    "lnk": "http://www.espn.com/nfl/player/_/id/13981/mark-ingram-ii",
                    "uid": "s:20~l:28~a:13981"
                },
                "stats": [
                    "1",
                    "1",
                    "0"
                ]
            }
        ],
        "keys": [
            "fumbles",
            "fumblesLost",
            "fumblesRecovered"
        ],
        "lbls": [
            "FUM",
            "LOST",
            "REC"
        ],
        "text": "New Orleans Fumbles",
        "ttls": [
            "1",
            "1",
            "2"
        ],
        "type": "fumbles"
    }
    helper = BoxScoreHelper(maker, codes)
    results = helper.build_fumbles_stats(section, 1)
    assert_that(filter_by_code(results, codes, 'FUM', 1)).is_not_empty()


def test_build_kick_return_stats():
    """
    Tests building Kick Return Stats
    """
    maker = build_maker()
    stat_code_repo = StatisticCodeRepository(maker)

    stat_code_repo.save(
        StatisticCode(code='NO', description='Kick Returns', grouping='kickReturns'))
    stat_code_repo.save(
        StatisticCode(code='YDS', description='Kick Return Yards', grouping='kickReturns'))
    stat_code_repo.save(
        StatisticCode(code='AVG', description='Kick Return Average', grouping='kickReturns'))
    stat_code_repo.save(
        StatisticCode(code='LONG', description='Kick Return Long', grouping='kickReturns'))
    stat_code_repo.save(
        StatisticCode(code='TD', description='Kick Return Touchdowns', grouping='kickReturns'))
    stat_code_repo.save(StatisticCategory(code='S', description='Special Teams'))
    stat_code_repo.save(Player(name='Deonte Harty',
                               url='http://www.espn.com/nfl/player/_/id/4411193/deonte-harty'))
    codes = stat_code_repo.get_statistic_codes()
    section = {
        "athlts": [{
            "athlt": {
                "dspNm": "Deonte Harty",
                "guid": "89723537-3856-63e7-002e-8074d487f4e4",
                "id": "4411193",
                "lnk": "http://www.espn.com/nfl/player/_/id/4411193/deonte-harty",
                "uid": "s:20~l:28~a:4411193"
            },
            "stats": [
                "1",
                "12",
                "12.0",
                "12",
                "0"
            ]
        }],
        "keys": [
            "kickReturns",
            "kickReturnYards",
            "yardsPerKickReturn",
            "longKickReturn",
            "kickReturnTouchdowns"
        ],
        "lbls": [
            "NO",
            "YDS",
            "AVG",
            "LONG",
            "TD"
        ],
        "text": "New Orleans Kick Returns",
        "ttls": [],
        "type": "kickReturns"
    }
    helper = BoxScoreHelper(maker, codes)
    results = helper.build_kick_returns_stats(section, 1)
    assert_that(filter_by_code(results, codes, 'NO', 1)).is_not_empty()
    assert_that(filter_by_code(results, codes, 'YDS', 12)).is_not_empty()
    assert_that(filter_by_code(results, codes, 'AVG', 12.0)).is_not_empty()
    assert_that(filter_by_code(results, codes, 'LONG', 12)).is_not_empty()
    assert_that(filter_by_code(results, codes, 'TD', 0)).is_not_empty()


def test_build_punt_return_stats():
    """
    Tests Building Punt Return Stats.
    """
    maker = build_maker()
    stat_code_repo = StatisticCodeRepository(maker)

    stat_code_repo.save(
        StatisticCode(code='NO', description='Punt Returns', grouping='puntReturns'))
    stat_code_repo.save(
        StatisticCode(code='YDS', description='Punt Return yards', grouping='puntReturns'))
    stat_code_repo.save(
        StatisticCode(code='AVG', description='Punt Return Average', grouping='puntReturns'))
    stat_code_repo.save(
        StatisticCode(code='LONG', description='Punt Return Long', grouping='puntReturns'))
    stat_code_repo.save(
        StatisticCode(code='TD', description='Punt Return Touchdowns', grouping='puntReturns'))
    stat_code_repo.save(StatisticCategory(code='S', description='Special Teams'))
    stat_code_repo.save(Player(name='Deonte Harty',
                               url='http://www.espn.com/nfl/player/_/id/4411193/deonte-harty'))
    codes = stat_code_repo.get_statistic_codes()
    section = {
        "athlts": [
            {
                "athlt": {
                    "dspNm": "Deonte Harty",
                    "guid": "89723537-3856-63e7-002e-8074d487f4e4",
                    "id": "4411193",
                    "lnk": "http://www.espn.com/nfl/player/_/id/4411193/deonte-harty",
                    "uid": "s:20~l:28~a:4411193"
                },
                "stats": [
                    "1",
                    "12",
                    "12.0",
                    "12",
                    "0"
                ]
            }
        ],
        "keys": [
            "puntReturns",
            "puntReturnYards",
            "yardsPerPuntReturn",
            "longPuntReturn",
            "puntReturnTouchdowns"
        ],
        "lbls": [
            "NO",
            "YDS",
            "AVG",
            "LONG",
            "TD"
        ],
        "text": "New Orleans Punt Returns",
        "ttls": [
            "1",
            "12",
            "12.0",
            "12",
            "0"
        ],
        "type": "puntReturns"
    }
    helper = BoxScoreHelper(maker, codes)
    results = helper.build_punt_returns_stats(section, 1)
    assert_that(filter_by_code(results, codes, 'NO', 1)).is_not_empty()
    assert_that(filter_by_code(results, codes, 'YDS', 12)).is_not_empty()
    assert_that(filter_by_code(results, codes, 'AVG', 12.0)).is_not_empty()
    assert_that(filter_by_code(results, codes, 'LONG', 12)).is_not_empty()
    assert_that(filter_by_code(results, codes, 'TD', 0)).is_not_empty()


def test_build_punting_stats():
    """
    Tests Building Punting Stats.
    """
    maker = build_maker()
    stat_code_repo = StatisticCodeRepository(maker)

    stat_code_repo.save(StatisticCode(code='NO', description='Punts', grouping='punting'))
    stat_code_repo.save(StatisticCode(code='YDS', description='Punt Yards', grouping='punting'))
    stat_code_repo.save(StatisticCode(code='AVG', description='Punt Average', grouping='punting'))
    stat_code_repo.save(StatisticCode(code='TB', description='Punt Touchbacks', grouping='punting'))
    stat_code_repo.save(
        StatisticCode(code='IN20', description='Punt Inside 20', grouping='punting'))
    stat_code_repo.save(StatisticCode(code='LONG', description='Punt Long', grouping='punting'))
    stat_code_repo.save(StatisticCategory(code='S', description='Special Teams'))
    stat_code_repo.save(Player(name='Blake Gillikin',
                               url='http://www.espn.com/nfl/player/_/id/4045180/blake-gillikin'))
    codes = stat_code_repo.get_statistic_codes()
    section = {
        "athlts": [
            {
                "athlt": {
                    "dspNm": "Blake Gillikin",
                    "guid": "af1d32e3-64ab-5a8b-a1e5-a678d0e44876",
                    "id": "4045180",
                    "lnk": "http://www.espn.com/nfl/player/_/id/4045180/blake-gillikin",
                    "uid": "s:20~l:28~a:4045180"
                },
                "stats": [
                    "5",
                    "272",
                    "54.4",
                    "0",
                    "1",
                    "59"
                ]
            }
        ],
        "keys": [
            "punts",
            "puntYards",
            "grossAvgPuntYards",
            "touchbacks",
            "puntsInside20",
            "longPunt"
        ],
        "lbls": [
            "NO",
            "YDS",
            "AVG",
            "TB",
            "In 20",
            "LONG"
        ],
        "text": "New Orleans Punting",
        "ttls": [
            "5",
            "272",
            "54.4",
            "0",
            "1",
            "59"
        ],
        "type": "punting"
    }
    helper = BoxScoreHelper(maker, codes)
    results = helper.build_punting_stats(section, 1)
    assert_that(filter_by_code(results, codes, 'NO', 5)).is_not_empty()
    assert_that(filter_by_code(results, codes, 'YDS', 272)).is_not_empty()
    assert_that(filter_by_code(results, codes, 'AVG', 54.4)).is_not_empty()
    assert_that(filter_by_code(results, codes, 'TB', 0)).is_not_empty()
    assert_that(filter_by_code(results, codes, 'IN20', 1)).is_not_empty()
    assert_that(filter_by_code(results, codes, 'LONG', 59)).is_not_empty()


def test_build_kicking_stats():
    """
    Tests Building kicking stats.
    """
    maker = build_maker()
    stat_code_repo = StatisticCodeRepository(maker)

    stat_code_repo.save(
        StatisticCode(code='FGA', description='Field Goal Attempts', grouping='kicking'))
    stat_code_repo.save(
        StatisticCode(code='FGM', description='Field Goals Made', grouping='kicking'))
    stat_code_repo.save(
        StatisticCode(code='LONG', description='Field Goal Long', grouping='kicking'))
    stat_code_repo.save(
        StatisticCode(code='XPA', description='Extra Point Attempts', grouping='kicking'))
    stat_code_repo.save(
        StatisticCode(code='XPM', description='Extra Points Made', grouping='kicking'))
    stat_code_repo.save(StatisticCategory(code='S', description='Special Teams'))
    stat_code_repo.save(Player(name='Wil Lutz',
                               url='http://www.espn.com/nfl/player/_/id/2985659/wil-lutz'))
    codes = stat_code_repo.get_statistic_codes()
    section = {
        "athlts": [
            {
                "athlt": {
                    "dspNm": "Wil Lutz",
                    "guid": "ea08c425-ec7d-6abb-c79b-a0acae427a5e",
                    "id": "2985659",
                    "lnk": "http://www.espn.com/nfl/player/_/id/2985659/wil-lutz",
                    "uid": "s:20~l:28~a:2985659"
                },
                "stats": [
                    "2/3",
                    "67.0",
                    "51",
                    "1/1",
                    "7"
                ]
            }
        ],
        "keys": [
            "fieldGoalsMade/fieldGoalAttempts",
            "fieldGoalPct",
            "longFieldGoalMade",
            "extraPointsMade/extraPointAttempts",
            "totalKickingPoints"
        ],
        "lbls": [
            "FG",
            "PCT",
            "LONG",
            "XP",
            "PTS"
        ],
        "text": "New Orleans Kicking",
        "ttls": [
            "2/3",
            "66.7",
            "51",
            "1/1",
            "7"
        ],
        "type": "kicking"
    }
    helper = BoxScoreHelper(maker, codes)
    results = helper.build_kicking_stats(section, 1)
    assert_that(filter_by_code(results, codes, 'FGM', 2)).is_not_empty()
    assert_that(filter_by_code(results, codes, 'FGA', 3)).is_not_empty()
    assert_that(filter_by_code(results, codes, 'LONG', 51)).is_not_empty()
    assert_that(filter_by_code(results, codes, 'XPA', 1)).is_not_empty()
    assert_that(filter_by_code(results, codes, 'XPM', 1)).is_not_empty()
