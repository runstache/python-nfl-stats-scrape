"""
Box score Helper Class
"""
from football_data.models import Statistic, StatisticCode, StatisticCategory
from football_data.repositories import StatisticCategoryRepository
from selenium import webdriver
from sqlalchemy.orm import sessionmaker

from helpers.player import PlayerHelper


class BoxScoreHelper:
    maker: sessionmaker
    codes: list[StatisticCode]
    offense_category: StatisticCategory
    defense_category: StatisticCategory
    special_category: StatisticCategory

    def __init__(self, maker: sessionmaker, codes: list[StatisticCode]) -> None:
        """
        Constructor.
        Args:
            maker: Sql Alchemy Session Maker
            codes: List of Statistic Codes
        """
        self.maker = maker
        self.codes = codes
        repo = StatisticCategoryRepository(maker)
        self.offense_category = repo.get_statistic_category(code='O')
        self.defense_category = repo.get_statistic_category(code='D')
        self.special_category = repo.get_statistic_category(code='S')

    @staticmethod
    def get_box_score(game_id: str) -> dict | None:
        """
        Returns the box score data.
        Args:
            game_id: Game ID

        Returns: Dictionary or None

        """

        box_score_url = f"https://www.espn.com/nfl/boxscore/_/gameId/{game_id}"
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--ignore-certificate-errors')

        browser = webdriver.Chrome(options=options)
        browser.get(box_score_url)
        box_score_result: dict = browser.execute_script('return window.__espnfitt__')
        browser.quit()
        return box_score_result

    def get_statistic_code(self, group: str, code: str) -> StatisticCode | None:
        """
        Retrieves a Statistic Code from the listing.
        Args:
            group: Grouping
            code: Code Value

        Returns: Statistic Code
        """

        result = list(
            filter(lambda x:
                   str(x.code).upper() == code.replace(' ', '').upper()
                   and x.grouping == group, self.codes))
        if result:
            return result[0]
        return None

    @staticmethod
    def convert_value(value: str) -> float:
        """
        Converts String to Fload value.
        Returns: Float Value
        """
        try:
            return float(value)
        except ValueError:
            return 0

    def build_general_statistics(self, section: dict,
                                 schedule_id: int, group: str,
                                 category: StatisticCategory) -> list[Statistic]:
        """
        Builds General Statistic Entries based on the Section provided
        Args:
            section: Section
            schedule_id: Schedule Id
            group: Stat Code Group
            category: Statistic Category
        Returns: List of Statistics

        """
        stats = []
        helper = PlayerHelper(self.maker)
        athletes: list[dict] = section.get('athlts', [])

        if athletes:
            labels = section.get('lbls', [])
            for athlete in athletes:
                player = helper.resolve_player(athlete.get('athlt', {}).get('lnk', ''))
                stat_values = athlete.get('stats', [])
                for label in labels:
                    index = labels.index(label)
                    stat_code = self.get_statistic_code(group, label)
                    if stat_code:
                        stats.append(Statistic(statistic_code_id=stat_code.id,
                                               schedule_id=schedule_id,
                                               value=self.convert_value(stat_values[index]),
                                               category_id=category.id,
                                               player_id=player.id))

        return stats

    def build_passing_stats(self, passing_section: dict, schedule_id: int) -> list[Statistic]:
        """
        Maps the Passing Statistics to Statistic Items
        Args:
            passing_section: Passing Section
            schedule_id: Schedule Id

        Returns: List of Statistics
        """
        stats = self.build_general_statistics(passing_section, schedule_id, 'passing',
                                              self.offense_category)

        helper = PlayerHelper(self.maker)
        athletes: list[dict] = passing_section.get('athlts', [])

        if athletes:
            labels = passing_section.get('lbls', [])
            for athlete in athletes:
                player = helper.resolve_player(athlete.get('athlt', {}).get('lnk', ''))
                stat_values = athlete.get('stats', [])
                label_index = labels.index('C/ATT')
                attempt_code = self.get_statistic_code('passing', 'PA')
                complete_code = self.get_statistic_code('passing', 'PC')
                values = str(stat_values[label_index]).split('/')

                # Add the Passing Attempts and Completions
                stats.append(Statistic(statistic_code_id=attempt_code.id,
                                       schedule_id=schedule_id,
                                       value=self.convert_value(values[1]),
                                       category_id=self.offense_category.id,
                                       player_id=player.id))
                stats.append(Statistic(statistic_code_id=complete_code.id,
                                       schedule_id=schedule_id,
                                       value=self.convert_value(values[0]),
                                       category_id=self.offense_category.id,
                                       player_id=player.id))

        return stats

    def build_rushing_stats(self, rushing_section: dict, schedule_id: int) -> list[Statistic]:
        """
        Maps the Rushing Statistics to Statistic Items
        Args:
            rushing_section: Rushing Section
            schedule_id: Schedule Id

        Returns: List of Statistics

        """

        return self.build_general_statistics(rushing_section, schedule_id, 'rushing',
                                             self.offense_category)

    def build_receiving_stats(self, receiving_section: dict, schedule_id: int) -> list[Statistic]:
        """
        Maps the Receiving Statistics to Statistic Items
        Args:
            receiving_section: Statistic Section
            schedule_id: Schedule ID

        Returns: List of Statistics

        """

        return self.build_general_statistics(receiving_section, schedule_id, 'receiving',
                                             self.offense_category)

    def build_fumbles_stats(self, fumble_section: dict, schedule_id: int) -> list[Statistic]:
        """
        Maps the Fumbles statistics to Statistic Items.
        Args:
            fumble_section: Fumbles Section
            schedule_id: Schedule ID

        Returns: List of Statistics

        """
        return self.build_general_statistics(fumble_section, schedule_id, 'general',
                                             self.offense_category)

    def build_defensive_stats(self, defense_section: dict, schedule_id: int) -> list[Statistic]:
        """
        Maps the Defensive statistics to Statistic Items
        Args:
            defense_section: Defensive Section
            schedule_id: Schedule ID

        Returns: List of Defensive Statistics

        """
        return self.build_general_statistics(defense_section, schedule_id, 'defensive',
                                             self.defense_category)

    def build_interception_stats(self, interception_section: dict,
                                 schedule_id: int) -> list[Statistic]:
        """
        Maps the Interception statistics to Statistic Items.
        Args:
            interception_section: Interception Section
            schedule_id: Schedule ID

        Returns: List of Interception Statistics

        """

        return self.build_general_statistics(interception_section, schedule_id, 'general',
                                             self.defense_category)

    def build_kick_returns_stats(self, kick_return_section: dict,
                                 schedule_id: int) -> list[Statistic]:
        """
        Maps the Kick Return statistics to Statistics Items.
        Args:
            kick_return_section: Kick Return Section
            schedule_id: Schedule ID

        Returns: List of Statistics

        """
        return self.build_general_statistics(kick_return_section, schedule_id, 'kickReturns',
                                             self.special_category)

    def build_punt_returns_stats(self, punt_return_section: dict,
                                 schedule_id: int) -> list[Statistic]:
        """
        Maps the Punt Return statistics to Statistics Items.
        Args:
            punt_return_section: Punt Return Section
            schedule_id: Schedule ID

        Returns: List of Statistics

        """
        return self.build_general_statistics(punt_return_section, schedule_id, 'puntReturns',
                                             self.special_category)

    def build_kicking_stats(self, kicking_section: dict, schedule_id: int) -> list[Statistic]:
        """
        Maps the Kicking statistics to Statistics Items.
        Args:
            kicking_section: Kicking Section
            schedule_id: Schedule ID

        Returns: List of Statistics

        """
        stats = self.build_general_statistics(kicking_section, schedule_id, 'kicking',
                                              self.special_category)

        fg_attempt = self.get_statistic_code('kicking', 'FGA')
        fg_made = self.get_statistic_code('kicking', 'FGM')
        xp_attempt = self.get_statistic_code('kicking', 'XPA')
        xp_made = self.get_statistic_code('kicking', 'XPM')

        helper = PlayerHelper(self.maker)
        athletes: list[dict] = kicking_section.get('athlts', [])

        if athletes:
            labels = kicking_section.get('lbls', [])
            for athlete in athletes:
                player = helper.resolve_player(athlete.get('athlt', {}).get('lnk', ''))
                stat_values = athlete.get('stats', [])
                fg_index = labels.index('FG')
                xp_index = labels.index('XP')

                fg_values = str(stat_values[fg_index]).split('/')
                xp_values = str(stat_values[xp_index]).split('/')

                # Add the Passing Attempts and Completions
                stats.append(Statistic(statistic_code_id=fg_attempt.id,
                                       schedule_id=schedule_id,
                                       value=self.convert_value(fg_values[1]),
                                       category_id=self.special_category.id,
                                       player_id=player.id))
                stats.append(Statistic(statistic_code_id=fg_made.id,
                                       schedule_id=schedule_id,
                                       value=self.convert_value(fg_values[0]),
                                       category_id=self.special_category.id,
                                       player_id=player.id))
                stats.append(Statistic(statistic_code_id=xp_attempt.id,
                                       schedule_id=schedule_id,
                                       value=self.convert_value(xp_values[1]),
                                       category_id=self.special_category.id,
                                       player_id=player.id))
                stats.append(Statistic(statistic_code_id=xp_made.id,
                                       schedule_id=schedule_id,
                                       value=self.convert_value(xp_values[0]),
                                       category_id=self.special_category.id,
                                       player_id=player.id))

        return stats

    def build_punting_stats(self, punting_section: dict, schedule_id: int) -> list[Statistic]:
        """
        Maps the Punting statistics to Statistics Items.
        Args:
            punting_section: Punting Section
            schedule_id: Schedule ID

        Returns: List of Statistics

        """
        return self.build_general_statistics(punting_section, schedule_id, 'punting',
                                             self.special_category)
