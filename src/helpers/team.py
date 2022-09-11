"""
Team Helper Class for retrieving statistics.
"""

from pyquery import PyQuery as pq
from lxml.html import HtmlElement

class MatchupHelper:
    
    document:pq
    base_api_url:str
    
    def __init__(self, doc:str, api_url:str) -> None:
        self.base_api_url = api_url
        self.document = pq(doc)
        
        
    def split_value(self, value:str, delimiter:str) -> tuple|None:
        """
        Returns a Touple of the split value.

        Args:
            value (str): Value to split
            delimiter (str): delimiter

        Returns:
            tuple: Touple of value
        """
        
        parts = value.split(delimiter)
        if parts:
            return (int(parts[0]), int(parts[1]))
        return None
        
        
    def find_row(self, table:HtmlElement, identifier:str) -> pq|None:
        """
        Finds a given row in the Row collection

        Args:
            table (HtmlElement): Collection of rows
            identifier (str): Row Identifier

        Returns:
            PyQuery: Row Html Element
        """
        
        doc = pq(table)
        row = doc.find('tr[data-stat-attr=' + identifier + ']')
        
        if len(row) > 1:
            return pq(row[0])
        else:
            return row if row else None
    
    def process_row(self, row:pq, home_id:int, away_id:int, game_id:int, code:str, type_code:str) -> list|None:
        """
        Processes a row into a list of statistics

        Args:
            row (PyQuery): Row to process
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
    
    def get_redzone_efficiency(self, table:pq, home_id:int, away_id:int, game_id:int) -> list|None:
        """
        Returns the Redzone efficiency.

        Args:
            table (PyQuery) Stat Table
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
        
    def get_third_down_efficiency(self, table:pq, home_id:int, away_id:int, game_id:int) -> list|None:
        """
        Returns the Third down efficiency.

        Args:
            table (PyQuery) Stat Table
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
        
    def get_fourth_down_efficiency(self, table:pq, home_id:int, away_id:int, game_id:int) -> list|None:
        """
        Gets the Fourth down efficiency.

        Args:
            table (PyQuery) Stat Table
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
        
    def get_passing_efficiency(self, table:pq, home_id:int, away_id:int, game_id:int) -> list|None:
        """
        Retrieves the Passing efficiency.

        Args:
            table (PyQuery) Stat Table
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
    
    def get_penalties(self, table:pq, home_id:int, away_id:int, game_id:int) -> list|None:
        """
        Retrieves the Penalties

        Args:
            table (PyQuery) Stat Table
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

    def get_time_of_possession(self, table:pq, home_id:int, away_id:int, game_id:int) -> list|None:
        """
        Retreives the Time of Possession.

        Args:
            table (PyQuery) Stat Table
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

    
    def build_team_stats(self, home_id:int, away_id:int, game_id:int) -> list|None:
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
            ('firstDownsPassing','P1D','O'),
            ('firstDownsRushing', 'R1D', 'O'),
            ('totalOffensivePlays', 'PLAY', 'O'),
            ('totalYards', 'YDS', 'O'),
            ('totalDrives', 'DRV', 'O'),
            ('yardsPerPlay', 'YPP', 'O'),
            ('netPassingYards', 'PYDS', 'O'),
            ('yardsPerPass', 'PSAVG', 'O'),
            ('interceptions','PINT', 'O'),
            ('rushingYards','RYDS', 'O'),
            ('rushingAttempts', 'RCAR', 'O'),
            ('yardsPerRushAttempt', 'RAVG', 'O'),
            ('turnovers','TO','T'),
            ('fumblesLost', 'FLOST', 'T'),
            ('defensiveTouchdowns','TD','D')
        ]
        
        splitters = [
            self.get_fourth_down_efficiency,
            self.get_passing_efficiency,
            self.get_penalties,
            self.get_redzone_efficiency,
            self.get_third_down_efficiency,
            self.get_time_of_possession
        ]
        
        for item in items:
            row = self.find_row(body, item[0])
            results = self.process_row(row,home_id, away_id, game_id, item[1], item[2])
            if results:
                stats.extend(results)
        
        for method in splitters:
            results = method(body,home_id, away_id, game_id)
            if results:
                stats.extend(results)
        
        
        return stats