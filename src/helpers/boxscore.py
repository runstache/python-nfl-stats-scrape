"""
Box score Helper Class
"""

import logging
from urllib.parse import urljoin

import requests
from lxml.html import HtmlElement
from pyquery import PyQuery as pq
from requests.exceptions import RequestException


class BoxscoreHelper:
    stat_api_url: str

    def __init__(self, base_url: str) -> None:
        self.stat_api_url = urljoin(base_url, '/api/statistics')
        logging.basicConfig(level=logging.INFO)

    @staticmethod
    def get_column_value(column: pq, path: str) -> str | None:
        """
        Returns the value of a column

        Args:
            column (pq): column
            path (str): path to value

        Returns:
            str: column value
        """

        value = column(path).text()
        return value if value != '' and value != '--' else None

    @staticmethod
    def split_values(value: str) -> list | None:
        """
        Splits a String value by the '/'

        Args:
            value (str): Value to split

        Returns:
            list|None: List of integers or None
        """

        parts = value.split('/')
        if parts and len(parts) == 2:
            results = []
            for part in parts:
                if str(part).isnumeric():
                    results.append(int(part))
            return results if len(results) == 2 else None

        return None

    def build_statistic(self, row: pq, path: str, team_id: int, game_id: int, type_code: str,
                        player_url: str, identifier: str) -> dict | None:
        """
        Builds a Statistic Object from the items

        Args:
            row (pq): Row to Query
            path (str): Path to Column Value
            team_id (int): Team Id
            game_id (int) Game Id
            type_code (str): Stat Type Code
            player_url (str): Player Url
            identifier (str): Stat identifier

        Returns:
            dict: Statistic
        """

        value = self.get_column_value(row, path)
        if value:
            return {
                'statisticCode': identifier,
                'playerUrl': player_url,
                'value': float(value),
                'teamId': team_id,
                'gameId': game_id,
                'categoryCode': type_code
            }

        return None

    def process_row(self, codes: list, row: pq, team_id: int, game_id: int, type_code: str) -> list:
        """
        Processes a Row into a collection of Statistics.

        Args:
            codes (list): Statistic Codes as Tuples
            row (pq): Row to process
            team_id (int): Team ID Number
            game_id (int): Game ID
            type_code (str): Stat Type Code (O, D, S)

        Returns:
            list: List of Schedule Items.
        """
        stats = []

        player_row = pq(row)
        player_column = player_row('td.name')
        ref = player_column.find('a')
        player_url = ref.attr('href')

        for item in codes:
            stat = self.build_statistic(
                player_row, item[1], team_id, game_id, type_code, player_url, item[0])
            if stat:
                stats.append(stat)
        return stats

    def add_statistic(self, stats: list) -> None:
        """
        Adds the Statistic to the Api

        Args:
            stats (list): List of Stats
        """

        for stat in stats:

            success = False
            max_retries = 5
            count = 0
            while not success and count <= max_retries:
                try:
                    response = requests.post(self.stat_api_url, json=stat)
                    if response.status_code != 200:
                        logging.warning('POSSIBLE FAILURE POSTING STAT')
                        success = False
                        count = count + 1
                    else:
                        success = True
                except RequestException:
                    logging.warning('REQUEST ERROR SAVING STATS, RETRYING...')
                    success = False
                    count = count + 1

    def build_passing_statistics(self, team_id: int, game_id: int, section: HtmlElement) -> list:
        """
        Creates statistics for the Passing section.

        Args:
            team_id (int): Team ID number
            game_id (int): Game ID Number
            section (HtmlElement): Passing Section

        Returns:
            list: List of passing statistics
        """
        stats = []

        player_stat_items = [
            ('PYDS', 'td.yds'),
            ('PSAVG', 'td.avg'),
            ('PTD', 'td.td'),
            ('PINT', 'td.int'),
            ('QBR', 'td.qbr'),
            ('RTG', 'td.rtg')
        ]

        stat_table = section.find('table')
        if stat_table is not None:
            table_body = stat_table.find('tbody')
            rows = table_body.find('tr')

            for row in rows:
                if row.attrib.get('class') is None:
                    player_row = pq(row)
                    player_column = player_row('td.name')
                    ref = player_column.find('a')
                    player_url = ref.attr('href')

                    comp_attempt = player_row('td.c-att').text()
                    parts = comp_attempt.split('/')
                    stats.append({
                        'statisticCode': 'PC',
                        'playerUrl': player_url,
                        'value': int(parts[0]),
                        'teamId': team_id,
                        'gameId': game_id,
                        'categoryCode': 'O'
                    })
                    stats.append({
                        'statisticCode': 'PA',
                        'playerUrl': player_url,
                        'value': int(parts[1]),
                        'teamId': team_id,
                        'gameId': game_id,
                        'categoryCode': 'O'
                    })

                    for item in player_stat_items:
                        stat = self.build_statistic(
                            player_row, item[1], team_id, game_id, 'O', player_url, item[0])
                        if stat:
                            stats.append(stat)

        return stats

    def build_rushing_statistics(self, team_id: int, game_id: int, section: HtmlElement) -> list:
        """
        Creates statistics for the Rushing Section.

        Args:
            team_id (int): Team Id
            game_id (int): Game Id
            section (HtmlElement): Rushing Section

        Returns:
            list: List of Rushing Stats.
        """
        stats = []
        player_stat_items = [
            ('RCAR', 'td.car'),
            ('RYDS', 'td.yds'),
            ('RAVG', 'td.avg'),
            ('RTD', 'td.td'),
            ('RLONG', 'td.long')
        ]

        stat_table = section.find('table')
        if stat_table != None:
            table_body = stat_table.find('tbody')
            rows = table_body.find('tr')

            for row in rows:
                if row.attrib.get('class') is None:
                    stats.extend(self.process_row(
                        player_stat_items, row, team_id, game_id, 'O'))
        return stats

    def build_receiving_statistics(self, team_id: int, game_id: int, section: HtmlElement) -> list:
        """
        Creates statistics for the Receiving Section.

        Args:
            team_id (int): Team Id
            game_id (int): Game Id
            section (HtmlElement): Receiving Section

        Returns:
            list: List of Receiving Stats.
        """
        stats = []
        player_stat_items = [
            ('REC', 'td.rec'),
            ('CYDS', 'td.yds'),
            ('CAVG', 'td.avg'),
            ('CTD', 'td.td'),
            ('CLONG', 'td.long'),
            ('TGTS', 'td.tgts')
        ]

        stat_table = section.find('table')
        if stat_table is not None:
            table_body = stat_table.find('tbody')
            rows = table_body.find('tr')

            for row in rows:
                if row.attrib.get('class') is None:
                    stats.extend(self.process_row(
                        player_stat_items, row, team_id, game_id, 'O'))
        return stats

    def build_fumble_statistics(self, team_id: int, game_id: int, section: HtmlElement) -> list:
        """
        Creates Statistics for the Fumbles Section.

        Args:
            team_id (int): Team Id
            game_id (int): Game Id
            section (HtmlElement): Fumbles Section

        Returns:
            list: List of Fumble Stats
        """
        stats = []
        player_stat_items = [
            ('FUM', 'td.fum'),
            ('FLOST', 'td.lost'),
            ('FREC', 'td.rec')
        ]

        stat_table = section.find('table')
        if stat_table is not None:
            table_body = stat_table.find('tbody')
            rows = table_body.find('tr')

            for row in rows:
                if row.attrib.get('class') is None:
                    stats.extend(self.process_row(
                        player_stat_items, row, team_id, game_id, 'O'))
        return stats

    def build_defensive_statistics(self, team_id: int, game_id: int, section: HtmlElement) -> list:
        """
        Creates Statistics for the Defensive Section.

        Args:
            team_id (int): Team Id
            game_id (int): Game Id
            section (HtmlElement): Defensive Section

        Returns:
            list: List of Defensive stats
        """

        stats = []
        player_stat_items = [
            ('TACK', 'td.tot'),
            ('SOLO', 'td.solo'),
            ('SACK', 'td.sacks'),
            ('TFL', 'td.tfl'),
            ('PD', 'td.pd'),
            ('HITS', 'td.qb'),
            ('TD', 'td.td')
        ]

        stat_table = section.find('table')
        if stat_table is not None:
            table_body = stat_table.find('tbody')
            rows = table_body.find('tr')

            for row in rows:
                if row.attrib.get('class') is None:
                    stats.extend(self.process_row(
                        player_stat_items, row, team_id, game_id, 'D'))
        return stats

    def build_interception_statistics(self, team_id: int, game_id: int,
                                      section: HtmlElement) -> list:
        """
        Creates Statistics for the Interceptions section.

        Args:
            team_id (int): Team Id
            game_id (int): Game Id
            section (HtmlElement): Interception Section

        Returns:
            list: List of Interception Stats.
        """
        stats = []
        player_stat_items = [
            ('INT', 'td.int'),
            ('TD', 'td.td')
        ]

        stat_table = section.find('table')
        if stat_table is not None:
            table_body = stat_table.find('tbody')
            rows = table_body.find('tr')

            for row in rows:
                if row.attrib.get('class') is None:
                    stats.extend(self.process_row(
                        player_stat_items, row, team_id, game_id, 'D'))
        return stats

    def build_kick_return_statistics(self, team_id: int, game_id: int,
                                     section: HtmlElement) -> list:
        """
        Creates Statistics for the Kick Returns section.

        Args:
            team_id (int): Team Id
            game_id (int): Game Id
            section (HtmlElement): kick returns section

        Returns:
            list: List of kick return stats
        """
        stats = []
        player_stat_items = [
            ('KR', 'td.no'),
            ('KRYDS', 'td.yds'),
            ('KRAVG', 'td.avg'),
            ('KRLONG', 'td.long'),
            ('KRTD', 'td.td')
        ]

        stat_table = section.find('table')
        if stat_table is not None:
            table_body = stat_table.find('tbody')
            rows = table_body.find('tr')

            for row in rows:
                if row.attrib.get('class') is None:
                    stats.extend(self.process_row(
                        player_stat_items, row, team_id, game_id, 'S'))
        return stats

    def build_punt_return_statistics(self, team_id: int, game_id: int,
                                     section: HtmlElement) -> list:
        """
        Creates statistics for the Punt Returns Section.

        Args:
            team_id (int): Team Id
            game_id (int): Game Id
            section (HtmlElement): Punt Return Section

        Returns:
            list: list of Punt Return stats
        """
        stats = []
        player_stat_items = [
            ('PR', 'td.no'),
            ('PRYDS', 'td.yds'),
            ('PRAVG', 'td.avg'),
            ('PRLONG', 'td.long'),
            ('PRTD', 'td.td')
        ]

        stat_table = section.find('table')
        if stat_table is not None:
            table_body = stat_table.find('tbody')
            rows = table_body.find('tr')

            for row in rows:
                if row.attrib.get('class') is None:
                    stats.extend(self.process_row(
                        player_stat_items, row, team_id, game_id, 'S'))
        return stats

    def build_kicking_statistics(self, team_id: int, game_id: int, section: HtmlElement) -> list:
        """
        Creates Statistics for the Kicking Section.

        Args:
            team_id (int): Team Id
            game_id (int): Game Id
            section (HtmlElement): Kicking Section

        Returns:
            list: List of Kicking Stats
        """
        stats = []
        player_stat_items = [
            ('FGLONG', 'td.long')
        ]

        stat_table = section.find('table')
        if stat_table is not None:
            table_body = stat_table.find('tbody')
            rows = table_body.find('tr')

            for row in rows:
                if row.attrib.get('class') is None:
                    player_row = pq(row)
                    player_column = player_row('td.name')
                    ref = player_column.find('a')
                    player_url = ref.attr('href')

                    fg_comp_attempt = player_row('td.fg').text()
                    fg_parts = self.split_values(fg_comp_attempt)
                    if fg_parts:
                        stats.append({
                            'statisticCode': 'FGM',
                            'playerUrl': player_url,
                            'value': int(fg_parts[0]),
                            'teamId': team_id,
                            'gameId': game_id,
                            'categoryCode': 'S'
                        })
                        stats.append({
                            'statisticCode': 'FGA',
                            'playerUrl': player_url,
                            'value': int(fg_parts[1]),
                            'teamId': team_id,
                            'gameId': game_id,
                            'categoryCode': 'S'
                        })
                    xp_comp_attempt = player_row('td.xp').text()
                    xp_parts = self.split_values(xp_comp_attempt)
                    if xp_parts:
                        stats.append({
                            'statisticCode': 'XPA',
                            'playerUrl': player_url,
                            'value': int(xp_parts[1]),
                            'teamId': team_id,
                            'gameId': game_id,
                            'categoryCode': 'S'
                        })
                        stats.append({
                            'statisticCode': 'XPM',
                            'playerUrl': player_url,
                            'value': int(xp_parts[0]),
                            'teamId': team_id,
                            'gameId': game_id,
                            'categoryCode': 'S'
                        })

                    stats.extend(self.process_row(
                        player_stat_items, row, team_id, game_id, 'S'))

        return stats

    def build_punting_statistics(self, team_id: int, game_id: int, section: HtmlElement) -> list:
        """
        Creates Statistics for the Punting section.

        Args:
            team_id (int): Team Id
            game_id (int): Game Id
            section (HtmlElement): Punting section

        Returns:
            list: list of punting stats
        """

        stats = []
        player_stat_items = [
            ('PUNT', 'td.no'),
            ('PAVG', 'td.avg'),
            ('PNTYDS', 'td.yds'),
            ('PTB', 'td.tb'),
            ('P20', 'td.in'),
            ('PLONG', 'td.long')
        ]

        stat_table = section.find('table')
        if stat_table is not None:
            table_body = stat_table.find('tbody')
            rows = table_body.find('tr')

            for row in rows:
                if row.attrib.get('class') is None:
                    stats.extend(self.process_row(
                        player_stat_items, row, team_id, game_id, 'S'))
        return stats
