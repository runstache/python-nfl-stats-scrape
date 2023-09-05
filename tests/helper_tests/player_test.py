"""
Player Helper Tests
"""

from assertpy import assert_that
from helpers.player import PlayerHelper
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, select
from football_data.models import Player, Position
from football_data.repositories import PlayerRepository, PositionCodeRepository


def build_maker() -> sessionmaker:
    """
    Creates the Session Maker
    """
    engine = create_engine('sqlite://')
    Player.metadata.create_all(bind=engine)
    Position.metadata.create_all(bind=engine)
    return sessionmaker(bind=engine, expire_on_commit=False)


def test_resolve_player():
    """
    Tests resolving a Player that exists in the database.
    """

    maker = build_maker()
    pos_repo = PositionCodeRepository(maker)
    pos_repo.save(Position(id=1, code='QB', description='Quarterback'))

    player_repo = PlayerRepository(maker)
    player_repo.save(Player(id=1, name='Josh Allen',
                            url='https://www.espn.com/nfl/player/_/id/3918298/josh-allen',
                            position_id=1))

    helper = PlayerHelper(maker)
    result: Player = helper.resolve_player(
        'https://www.espn.com/nfl/player/_/id/3918298/josh-allen')

    assert_that(result).is_not_none()
    assert_that([result]).extracting('id', 'name', 'url').contains(
        (1, 'Josh Allen', 'https://www.espn.com/nfl/player/_/id/3918298/josh-allen'))

    session = maker()
    players = list(session.scalars(select(Player)).all())
    assert_that(players).is_not_empty().is_length(1)


def test_resolve_player_not_present():
    """
    Tests resolving a player that is not in the database.
    """

    maker = build_maker()
    pos_repo = PositionCodeRepository(maker)
    pos_repo.save(Position(code='QB', description='Quarterback'))
    pos_repo.save(Position(code='WR', description='Wide Receiver'))

    player_repo = PlayerRepository(maker)
    player_repo.save(Player(name='Jim Smith',
                            url='https://www.espn.com/nfl/player/_/id/3918298/jim-smith',
                            position_id=2))
    helper = PlayerHelper(maker)
    result = helper.resolve_player('https://www.espn.com/nfl/player/_/id/3918298/josh-allen')

    session = maker()
    items = list(session.scalars(select(Player)).all())
    assert_that(items).is_not_empty().is_length(2)
    assert_that(result).is_not_none()
