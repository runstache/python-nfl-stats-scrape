"""
Database Helper Classes
"""

from sqlalchemy import create_engine, URL
from sqlalchemy.orm import sessionmaker
from football_data.models import Team, TeamLeague, TeamStaff, TypeCode, StatisticCode, Statistic, StatisticCategory, Schedule, Player, Position, League

class DbHelper:
    """
    Helps generating items for interacting with the database.
    """

    @staticmethod
    def create_session_maker(server:str, database:str, user_name:str, password:str) -> sessionmaker:
        """
        Creates a Session Maker for the Database with all Models loaded
        Args:
            server: Server name
            database: Database name
            user_name: UserName
            password: Password

        Returns: Session Maker

        """
        url = URL.create('postgres', username=user_name, password=password, host=server, database=database)
        engine = create_engine(url)
        Team.metadata.create_all(bind=engine)
        TeamLeague.metadata.create_all(bind=engine)
        TeamStaff.metadata.create_all(bind=engine)
        TypeCode.metadata.create_all(bind=engine)
        StatisticCode.metadata.create_all(bind=engine)
        Statistic.metadata.create_all(bind=engine)
        StatisticCategory.metadata.create_all(bind=engine)
        Schedule.metadata.create_all(bind=engine)
        Player.metadata.create_all(bind=engine)
        Position.metadata.create_all(bind=engine)
        League.metadata.create_all(bind=engine)
        return sessionmaker(bind=engine, expire_on_commit=False)


