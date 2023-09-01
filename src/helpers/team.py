"""
Team Helper Class for retrieving statistics.
"""

from lxml.html import HtmlElement
from pyquery import PyQuery


class MatchupHelper:
    """
    Helper Class for working with Team Level Stats.
    """
    document: PyQuery
    base_api_url: str

    def __init__(self, doc: str, api_url: str) -> None:
        self.base_api_url = api_url
        self.document = PyQuery(doc)

    @staticmethod
    def split_value(value: str, delimiter: str) -> tuple | None:
        """
        Returns a Tuple of the split value.

        Args:
            value (str): Value to split
            delimiter (str): delimiter

        Returns:
            tuple: Touple of value
        """

        parts = value.split(delimiter)
        if parts:
            return int(parts[0]), int(parts[1])
        return None

    @staticmethod
    def find_row(table: HtmlElement | PyQuery, identifier: str) -> PyQuery | None:
        """
        Finds a given row in the Row collection

        Args:
            table (HtmlElement | PyQuery): Collection of rows
            identifier (str): Row Identifier

        Returns:
            HtmlElement: Row Html Element
        """

        doc = PyQuery(table)
        row = doc.find('tr[data-stat-attr=' + identifier + ']')

        if len(row) > 1:
            return PyQuery(row[0])
        else:
            return row if row else None

    @staticmethod
    def process_row(row: PyQuery, home_id: int, away_id: int, game_id: int, code: str,
                    type_code: str) -> list | None:
        """
        Processes a row into a list of statistics

        Args:
            row (HtmlElement): Row to process
            home_id (int): Home team id
            away_id (int): Away team id
            game_id (int): Game Id
            code (str): Stat Code
            type_code (str): Type Code
        Returns:
            list: collection of stats
        """

        columns = []
        if row:
            columns = row.find('td')

        if len(columns) == 3:
            away_value = str(columns[1].text).strip()
            home_value = str(columns[2].text).strip()
            items = [
                (away_value, away_id),
                (home_value, home_id)
            ]
            stats = []
            for item in items:
                stats.append({
                    'statisticCode': code,
                    'value': float(item[0]),
                    'gameId': game_id,
                    'teamId': item[1],
                    'categoryCode': type_code
                })

            return stats
        return None

    def get_redzone_efficiency(self, table: HtmlElement | PyQuery, home_id: int, away_id: int,
                               game_id: int) -> list | None:
        """
        Returns the Red zone efficiency.

        Args:
            table (HtmlElement) Stat Table
            home_id (int): Home Id
            away_id (int): Away Id
            game_id (int): Game Id

        Returns:
            list|None: Collection of Stats
        """
        columns = []
        row = self.find_row(table, 'redZoneAttempts')
        if row:
            columns = row.find('td')

        if len(columns) == 3:
            away_value = str(columns[1].text).strip()
            home_value = str(columns[2].text).strip()

            items = [
                (away_value, away_id),
                (home_value, home_id)
            ]
            stats = []
            for item in items:
                values = self.split_value(item[0], '-')
                if values:
                    stats.append({
                        'statisticCode': 'RZA',
                        'value': values[1],
                        'gameId': game_id,
                        'teamId': item[1],
                        'categoryCode': 'O'
                    })
                    stats.append({
                        'statisticCode': 'RZC',
                        'value': values[0],
                        'gameId': game_id,
                        'teamId': item[1],
                        'categoryCode': 'O'
                    })
            return stats
        return None

    def get_third_down_efficiency(self, table: HtmlElement | PyQuery, home_id: int, away_id: int,
                                  game_id: int) -> list | None:
        """
        Returns the Third down efficiency.

        Args:
            table (HtmlElement | PyQuery) Stat Table
            home_id (int): Home Id
            away_id (int): Away Id
            game_id (int): Game Id

        Returns:
            list|None: Collection of Stats
        """
        columns = []
        row = self.find_row(table, 'thirdDownEff')
        if row:
            columns = row.find('td')

        if len(columns) == 3:
            away_value = str(columns[1].text).strip()
            home_value = str(columns[2].text).strip()

            items = [
                (away_value, away_id),
                (home_value, home_id)
            ]
            stats = []
            for item in items:
                values = self.split_value(item[0], '-')
                if values:
                    stats.append({
                        'statisticCode': '3DA',
                        'value': values[1],
                        'gameId': game_id,
                        'teamId': item[1],
                        'categoryCode': 'O'
                    })
                    stats.append({
                        'statisticCode': '3DC',
                        'value': values[0],
                        'gameId': game_id,
                        'teamId': item[1],
                        'categoryCode': 'O'
                    })
            return stats
        return None

    def get_fourth_down_efficiency(self, table: HtmlElement | PyQuery, home_id: int, away_id: int,
                                   game_id: int) -> list | None:
        """
        Gets the Fourth down efficiency.

        Args:
            table (HtmlElement | PyQuery) Stat Table
            home_id (int): 
            away_id (int): _description_
            game_id (int): _description_

        Returns:
            list|None: Collection of Stats
        """

        columns = []
        row = self.find_row(table, 'fourthDownEff')
        if row:
            columns = row.find('td')

        if len(columns) == 3:
            away_value = str(columns[1].text).strip()
            home_value = str(columns[2].text).strip()

            items = [
                (away_value, away_id),
                (home_value, home_id)
            ]
            stats = []
            for item in items:
                values = self.split_value(item[0], '-')
                if values:
                    stats.append({
                        'statisticCode': '4DA',
                        'value': values[1],
                        'gameId': game_id,
                        'teamId': item[1],
                        'categoryCode': 'O'
                    })
                    stats.append({
                        'statisticCode': '4DC',
                        'value': values[0],
                        'gameId': game_id,
                        'teamId': item[1],
                        'categoryCode': 'O'
                    })
            return stats
        return None

    def get_passing_efficiency(self, table: HtmlElement | PyQuery, home_id: int, away_id: int,
                               game_id: int) -> list | None:
        """
        Retrieves the Passing efficiency.

        Args:
            table (HtmlElement | PyQuery) Stat Table
            home_id (int): Home Id
            away_id (int): Away Id
            game_id (int): Game Id

        Returns:
            list|None: Collection of Stats
        """

        columns = []
        row = self.find_row(table, 'completionAttempts')
        if row:
            columns = row.find('td')

        if len(columns) == 3:
            away_value = str(columns[1].text).strip()
            home_value = str(columns[2].text).strip()

            items = [
                (away_value, away_id),
                (home_value, home_id)
            ]
            stats = []
            for item in items:
                values = self.split_value(item[0], '-')
                if values:
                    stats.append({
                        'statisticCode': 'PA',
                        'value': values[1],
                        'gameId': game_id,
                        'teamId': item[1],
                        'categoryCode': 'O'
                    })
                    stats.append({
                        'statisticCode': 'PC',
                        'value': values[0],
                        'gameId': game_id,
                        'teamId': item[1],
                        'categoryCode': 'O'
                    })
            return stats
        return None

    def get_penalties(self, table: PyQuery | HtmlElement, home_id: int, away_id: int,
                      game_id: int) -> list | None:
        """
        Retrieves the Penalties

        Args:
            table (HtmlElement) Stat Table
            home_id (int): Home Id
            away_id (int): Away Id
            game_id (int): Game Id

        Returns:
            list|None: Collection of Stats
        """

        columns = []
        row = self.find_row(table, 'totalPenaltiesYards')
        if row:
            columns = row.find('td')

        if len(columns) == 3:
            away_value = str(columns[1].text).strip()
            home_value = str(columns[2].text).strip()

            items = [
                (away_value, away_id),
                (home_value, home_id)
            ]
            stats = []
            for item in items:
                values = self.split_value(item[0], '-')
                if values:
                    stats.append({
                        'statisticCode': 'PENYDS',
                        'value': values[1],
                        'gameId': game_id,
                        'teamId': item[1],
                        'categoryCode': 'T'
                    })
                    stats.append({
                        'statisticCode': 'PEN',
                        'value': values[0],
                        'gameId': game_id,
                        'teamId': item[1],
                        'categoryCode': 'T'
                    })
            return stats
        return None

    def get_time_of_possession(self, table: HtmlElement | PyQuery, home_id: int, away_id: int,
                               game_id: int) -> list | None:
        """
        Retrieves the Time of Possession.

        Args:
            table (HtmlElement | PyQuery) Stat Table
            home_id (int): Home Id
            away_id (int): Away Id
            game_id (int): Game Id

        Returns:
            list|None: Collection of Stats
        """
        columns = []
        row = self.find_row(table, 'possessionTime')
        if row:
            columns = row.find('td')

        if len(columns) == 3:
            away_value = str(columns[1].text).strip()
            home_value = str(columns[2].text).strip()

            items = [
                (away_value, away_id),
                (home_value, home_id)
            ]
            stats = []
            for item in items:
                values = self.split_value(item[0], ':')
                if values:
                    stats.append({
                        'statisticCode': 'TOP',
                        'value': float((values[0] * 60) + values[1]),
                        'gameId': game_id,
                        'teamId': item[1],
                        'categoryCode': 'T'
                    })
            return stats
        return None

    def get_scores(self, home_id: str, away_id: str, game_id: str) -> list | None:
        """
        Retrieves the final scores from the page.

        Args:
            home_id (str): Home Team Id
            away_id (str): Away Team Id
            game_id (str): Game Id

        Returns:
            list|None: Collection of score stats.
        """

        table = self.document('#linescore')
        body = table('tbody')
        stats = []
        rows = body.find('tr')
        if rows:
            away_row = PyQuery(rows[0])
            home_row = PyQuery(rows[1])

            away_score_column = away_row.find('td.final-score')
            home_score_column = home_row.find('td.final-score')

            if away_score_column and home_score_column:
                home_score = int(home_score_column.text()) if str(
                    home_score_column.text()).isnumeric() else 0
                away_score = int(away_score_column.text()) if str(
                    away_score_column.text()).isnumeric() else 0

                stats.append({
                    'statisticCode': 'PTSA',
                    'value': home_score,
                    'gameId': int(game_id),
                    'teamId': int(away_id),
                    'categoryCode': 'T'
                })

                stats.append({
                    'statisticCode': 'PTSA',
                    'value': away_score,
                    'gameId': int(game_id),
                    'teamId': int(home_id),
                    'categoryCode': 'T'
                })

                stats.append({
                    'statisticCode': 'PTS',
                    'value': home_score,
                    'gameId': int(game_id),
                    'teamId': int(home_id),
                    'categoryCode': 'T'
                })

                stats.append({
                    'statisticCode': 'PTS',
                    'value': away_score,
                    'gameId': int(game_id),
                    'teamId': int(away_id),
                    'categoryCode': 'T'
                })

        return stats

    def build_team_stats(self, home_id: int, away_id: int, game_id: int) -> list | None:
        """
        Retrieves the values from the Match Up information and provides a 
        collection of statistics.

        Args:
            home_id (int): home team id
            away_id (int): away team id
            game_id (int) game id

        Returns:
            list: _description_
        """

        section = self.document('#gamepackage-matchup')
        table = section('table.mod-data')
        body = table('tbody')
        stats = []
        items = [
            ('firstDownsPassing', 'P1D', 'O'),
            ('firstDownsRushing', 'R1D', 'O'),
            ('totalOffensivePlays', 'PLAY', 'O'),
            ('totalYards', 'YDS', 'O'),
            ('totalDrives', 'DRV', 'O'),
            ('yardsPerPlay', 'YPP', 'O'),
            ('netPassingYards', 'PYDS', 'O'),
            ('yardsPerPass', 'PSAVG', 'O'),
            ('interceptions', 'PINT', 'O'),
            ('rushingYards', 'RYDS', 'O'),
            ('rushingAttempts', 'RCAR', 'O'),
            ('yardsPerRushAttempt', 'RAVG', 'O'),
            ('turnovers', 'TO', 'T'),
            ('fumblesLost', 'FLOST', 'T'),
            ('defensiveTouchdowns', 'TD', 'D')
        ]

        for item in items:
            row = self.find_row(body, item[0])
            results = self.process_row(
                row, home_id, away_id, game_id, item[1], item[2])
            if results:
                stats.extend(results)
            stats.extend(self.get_fourth_down_efficiency(body, home_id, away_id, game_id))
            stats.extend(self.get_passing_efficiency(body, home_id, away_id, game_id))
            stats.extend(self.get_penalties(body, home_id, away_id, game_id))
            stats.extend(self.get_redzone_efficiency(body, home_id, away_id, game_id))
            stats.extend(self.get_third_down_efficiency(body, home_id, away_id, game_id))
            stats.extend(self.get_time_of_possession(body, home_id, away_id, game_id))

        # Get the Score
        scores = self.get_scores(str(home_id), str(away_id), str(game_id))
        if scores:
            stats.extend(scores)

        return stats
