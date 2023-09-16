"""
Team Helper Class for retrieving statistics.
"""

from sqlalchemy.orm import sessionmaker
from football_data.models import StatisticCode, Statistic, StatisticCategory
from football_data.repositories import StatisticCodeRepository, StatisticCategoryRepository
from selenium import webdriver


class MatchUpHelper:
    """
    Helper Class for working with Team Level Stats.
    """
    maker: sessionmaker
    codes: list[StatisticCode]
    category: StatisticCategory
    translations: dict

    def __init__(self, maker: sessionmaker) -> None:
        self.maker = maker

        cat_repo = StatisticCategoryRepository(maker)
        code_repo = StatisticCodeRepository(maker)
        self.codes = code_repo.get_statistic_codes(grouping='team')
        self.category = cat_repo.get_statistic_category(code='T')
        self.translations = {
            'completionAttempts': ['PC', 'PA'],
            'defensiveTouchdowns': ['DTD'],
            'firstDownsPassing': ['P1D'],
            'firstDownsRushing': ['R1D'],
            'fourthDownEff': ['4DC', '4DA'],
            'fumblesLost': ['FLOST'],
            'interceptions': ['INT'],
            'netPassingYards': ['PYDS'],
            'possessionTime': ['TOP'],
            'redZoneAttempts': ['RZC', 'RZA'],
            'rushingAttempts': ['RA'],
            'rushingYards': ['RYDS'],
            'thirdDownEff': ['3DC', '3DA'],
            'totalDrives': ['DRV'],
            'totalOffensivePlays': ['PLAY'],
            'totalPenaltiesYards': ['PEN', 'PENYDS'],
            'totalYards': ['YDS'],
            'turnovers': ['TO'],
            'yardsPerPass': ['PSAVG'],
            'yardsPerPlay': ['YPP'],
            'yardsPerRushAttempt': ['RAVG']

        }

    @staticmethod
    def get_match_up(game_id: str) -> dict | None:
        """
        Retrieves the Match up data.
        Args:
            game_id: Game Id

        Returns: Match Up Data Dictionary
        """
        url = f"https://www.espn.com/nfl/matchup/_/gameId/{game_id}"
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--ignore-certificate-errors')

        browser = webdriver.Chrome(options=options)
        browser.get(url)
        return browser.execute_script('return window.__espnfitt__')

    @staticmethod
    def convert_value(value: str) -> float:
        """
        Converts String to Fload value.
        Returns: Float Value
        """
        try:
            if ':' in value:
                split_values = value.split(':')
                return (MatchUpHelper.convert_value(
                    split_values[0]) * 60) + MatchUpHelper.convert_value(split_values[1])
            return float(value)
        except ValueError:
            return 0

    def get_statistic_code(self, code: str) -> StatisticCode | None:
        """
        Retrieves a Statistic Code from the listing.
        Args:
            code: Code Value

        Returns: Statistic Code
        """

        result = list(
            filter(lambda x:
                   str(x.code).upper() == code.upper(), self.codes))
        if result:
            return result[0]
        return None

    def build_statistic(self, values: dict, code: str, team_id: int,
                        schedule_id: int) -> Statistic | None:
        """
        Converts a Statistic Value dictionary to a Statistic object
        Args:
            values: Stat Values
            code: Statistic Code
            team_id: Team Id
            schedule-id: Schedule ID

        Returns: Statistics
        """
        code_value = self.get_statistic_code(code)
        if not code_value:
            return None

        entry_value = self.convert_value(values.get('d', ''))
        return Statistic(schedule_id=schedule_id, team_id=team_id, category_id=self.category.id,
                         statistic_code_id=code_value.id, value=entry_value)

    def build_split_statistic(self, values: dict, codes: list[str], team_id: int,
                              schedule_id: int) -> list[Statistic]:
        """
        Creates a list of Statistics from a stat value needing split.
        Args:
            values: statistic value entry
            codes: Codes in order of split
            team_id: Team ID
            schedule_id: Schedule ID

        Returns:

        """
        entry_value = values.get('d', '')
        if not entry_value:
            return []

        split_values = entry_value.split('-')
        if len(split_values) != len(codes):
            return []

        stats = []
        for split_value in split_values:
            code_item = self.get_statistic_code(codes[split_values.index(split_value)])
            if code_item:
                stats.append(Statistic(team_id=team_id, schedule_id=schedule_id,
                                       statistic_code_id=code_item.id,
                                       value=self.convert_value(split_value),
                                       category_id=self.category.id))

        return stats

    def generate_stats(self, team_id: int, schedule_id: int, entries: dict) -> list[Statistic]:
        """
        Generates the Statistic entries for provided team and schedule id
        Args:
            team_id: Team Id
            schedule_id: Schedule id
            entries: Stats entries

        Returns: List of statistics
        """
        stats = []
        for key in entries:
            translation = self.translations.get(key, [])
            values = dict(entries[key])
            if len(translation) > 1:
                stats.extend(self.build_split_statistic(values, translation, team_id, schedule_id))
            else:
                if len(translation) == 1:
                    stat = self.build_statistic(values, translation[0], team_id, schedule_id)
                    if stat:
                        stats.append(stat)

        return stats
