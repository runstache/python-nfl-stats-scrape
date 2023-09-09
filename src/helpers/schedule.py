"""
Schedule Module for Converting Schedule Entries from the listing.
"""

from sqlalchemy.orm import sessionmaker
from football_data.models import Schedule, Team
from football_data.repositories import TeamRepository, ScheduleRepository
from selenium import webdriver


class ScheduleHelper:
    """
    Helper Class for working with Schedules.
    """

    maker: sessionmaker

    def __init__(self, maker: sessionmaker):
        """
        Constructor
        """
        self.maker = maker

    @staticmethod
    def get_schedule(week_number: int, year_value: int, type_code: str) -> dict | None:
        """
        Retrieves the Schedule Meta Data
        Args:
            week_number: Week Number
            year_value: Year
            type_code: Type Code (1,2,3)

        Returns: Dictionary

        """
        schedule_url = f"https://www.espn.com/nfl/schedule/_/week/{week_number}" \
                       + f"/year/{year_value}/seasontype/{type_code}"

        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--ignore-certificate-errors')

        browser = webdriver.Chrome(options=options)
        browser.get(schedule_url)
        schedule_result: dict = browser.execute_script('return window.__espnfitt__')
        browser.quit()
        return schedule_result

    def resolve_teams(self, event_item: dict) -> dict:
        """
        Resolves a Team to the Database and Adds it if it is not present.
        Args:
            event_item: Event Item

        Returns: Team
        """
        result = {}
        teams: list[dict] = event_item.get('teams', [])
        for team in teams:
            team_code = team.get('abbrev')
            if team_code:
                repo = TeamRepository(self.maker)
                team_item = repo.get_team(code=team_code)
                if not team_item:
                    team_item = Team(code=team_code, name=team.get('displayName'),
                                     url=team.get('links'))
                    repo.save(team_item)
                if team.get('isHome', False) is True:
                    result['home_team'] = team_item
                else:
                    result['away_team'] = team_item

        return result

    def resolve_schedule(self, team_id: int, opponent_id: int, game_id: int, year: int, week: int,
                         url: str, is_home: bool, type_id: int) -> Schedule:
        """
        Resolves the Schedule from the Database or creates a new one.
        Args:
            team_id: Team ID
            opponent_id: Opponent ID
            game_id: Event
            year: Year Value
            week: Week Value
            url: Game Url
            is_home: Denotes it is for the home team.
            type_id: Schedule Type (1,2,3)

        Returns: Schedule
        """

        repo = ScheduleRepository(self.maker)
        schedule = repo.get_schedule(team_id=team_id, game_id=game_id)
        if not schedule:
            schedule = Schedule(team_id=team_id, opponent_id=opponent_id, game_id=game_id,
                                week_number=week, year_value=year, url=url, type_id=type_id,
                                is_home=is_home)
            repo.save(schedule)
        return schedule

    def convert_event(self, event_item: dict, type_id: int, week: int, year: int) -> list[Schedule]:
        """
        Converts an Event to a list of schedule items.
        Args:
            event_item: Event Item
            type_id: Schedule Type
            week: Week Number
            year: Year value

        Returns: List of Schedule
        """

        teams = self.resolve_teams(event_item)
        schedules = []
        game_id = int(event_item.get('id', 0))
        url = event_item.get('lnk', '')
        if teams:
            home_team = teams.get('home_team')
            away_team = teams.get('away_team')
            home_schedule = self.resolve_schedule(home_team.id, away_team.id, game_id, year, week,
                                                  url, True, type_id)
            away_schedule = self.resolve_schedule(away_team.id, home_team.id, game_id, year, week,
                                                  url, True, type_id)
            schedules.append(home_schedule)
            schedules.append(away_schedule)
        return schedules
