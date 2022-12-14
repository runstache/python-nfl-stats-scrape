"""
Player Helper Class to build and submit Players to the API.
"""

import logging
from urllib.parse import urljoin

import requests
from pyquery import PyQuery as pq
from requests.exceptions import RequestException

from helpers.positions import PositionHelper


class PlayerHelper:
    
    api_url:str
    player_url:str
    
    
    
    def __init__(self, url:str, api_base_url:str) -> None:
        
        self.player_url = url
        self.api_url = urljoin(api_base_url, '/api/player')
        logging.basicConfig(level=logging.INFO)
    
    def load_player_data(self)->pq|None:
        """
        Retrieves the data from the Url and Loads to PyQuery

        Returns:
            pq: PyQuery
        """
        
        success = False
        count = 0
        max_attempts = 5
        while not success and count <= max_attempts:
            try:
                response = requests.get(self.player_url, timeout=60)
                
                if response.status_code == 200:
                    success = True
                    return pq(response.text)
                else:
                    success = False
            except (TimeoutError, RequestException):
                logging.warning('PLAYER RETRIEVAL ISSUE')
                success = False
            count = count + 1 
            
        return None
                
        
    
    def add_player_information(self, player:dict) -> None:    
        """
        Adds the Player information to the API.
        """
        
        max_retries = 5
        count = 0
        success = False
        
        while not success and count <= max_retries:        
            try:
                response = requests.post(self.api_url, json=player)
                success = True
                if response.status_code != 200:
                    logging.warning(f"PLAYER SAVE POSSIBLY FAILED: {self.player_url}")
                    success = False
            except RequestException:
                logging.warning('ISSUE SAVING PLAYER TO API, RETRYING...')
                success = False
            count = count + 1
            
            
    def build_player(self) -> dict|None:
        """
        Creates a player model to submit to the api.

        Returns:
            dict: Player Model.
        """
        
        document = self.load_player_data()
        
        if  document != None:
            name_header = document('h1.PlayerHeader__Name')
            pieces = name_header.find('span')
        
            name = ''
            for piece in pieces:
                name = name + ' ' + piece.text
        
            team_info = document('ul.PlayerHeader__Team_Info')
        
            items = team_info.find('li')
            position = None
            helper = PositionHelper()
            for item in items:
                position = helper.translate_position(item.text)
                if position:
                    break
        
            return {
                'url': self.player_url,
                'name': name.strip(),
                'positionCode': position            
            }
        return None
        