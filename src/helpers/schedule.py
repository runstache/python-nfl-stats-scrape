"""
Schedule Module for Converting Schedule Entries from the listing.
"""

from urllib.parse import parse_qs, urljoin, urlparse

from lxml.html import HtmlElement
from pyquery import PyQuery as pq


class ScheduleHelper:

    document: pq

    def __init__(self, doc: str):
        """
        Constructor
        """

        self.document = pq(doc)

    def get_schedule_entries(self, week: int, year: int, type_code: str) -> list:
        """
        Retrieves the Schedule values from the HTML Document.

        Args:
            week (int): Week Number
            year (int): Year Value
            type_code (str): Season Type

        Returns:
            list: List of Schedule Entries
        """

        schedule_tables = self.document('table.Table')
        schedule_entries = []
        for schedule_table in schedule_tables:

            body = schedule_table.find('tbody')
            rows = body.findall('tr')
            for row in rows:
                schedule_entries.extend(
                    self.build_entries_from_row(row, year, week, type_code))

        return schedule_entries

    def build_entries_from_row(self, row: HtmlElement, year: int, week: int, type_code: str) -> list:
        """
        Builds a Set of Schedule Entries from a Row

        Args:
            row (HtmlElement): Table Row
            year (int): Year
            week (int): Week
            type_code (str): Type Code

        Returns:
            list: List of Schedule Entries
        """

        links = []
        schedule_entries = []
        columns = row.findall('td')
        for column in columns:
            column_doc = pq(column)
            refs = column_doc('a.AnchorLink')
            for ref in refs:
                href = ref.attrib.get('href')
                if 'player' not in href and href not in links and 'accuweather' not in href and 'vividseats' not in href:
                    links.append(href)
        if len(links) == 3:
            game_url = urljoin('https://www.espn.com', links.pop())
            away_team = links.pop()
            home_team = links.pop()

            parsed_url = urlparse(game_url)
            game_id = parse_qs(parsed_url.query).get('gameId', [0])[0]
            if int(game_id) > 0:
                schedule_entries.append({
                    'teamUrl': urljoin('https://www.espn.com', home_team),
                    'opponentUrl': urljoin('https://www.espn.com', away_team),
                    'url': game_url,
                    'year': year,
                    'week': week,
                    'typeCode': type_code,
                    'homeGame': True,
                    'gameId': int(game_id)
                })
                schedule_entries.append({
                    'opponentUrl': urljoin('https://www.espn.com', home_team),
                    'teamUrl': urljoin('https://www.espn.com', away_team),
                    'url': game_url,
                    'year': year,
                    'week': week,
                    'typeCode': type_code,
                    'homeGame': False,
                    'gameId': int(game_id)
                })
        return schedule_entries
