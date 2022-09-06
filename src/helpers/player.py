"""
Player Helper Class to build and submit Players to the API.
"""

from pyquery import PyQuery as pq
from urllib.parse import urljoin
import requests
from helpers.positions import PositionHelper
import logging

class PlayerHelper:
    
    api_url:str
    player_url:str
    
    
    
    def __init__(self, url:str, api_base_url:str) -> None:
        
        self.player_url = url
        self.api_url = urljoin(api_base_url, '/api/player')
        logging.basicConfig(level=logging.INFO)
    
    def load_player_data(self)->pq:
        """
        Retrieves the data from the Url and Loads to PyQuery

        Returns:
            pq: PyQuery
        """
        
        response = requests.get(self.player_url)
        if response.status_code == 200:
            return pq(response.text)
        
    
    def add_player_information(self, player:dict) -> None:    
        """
        Adds the Player information to the API.
        """
        
        response = requests.post(self.api_url, json=player)
        if response.status_code != 200:
            logging.warning(f"PLAYER SAVE POSSIBLY FAILED: {self.player_url}")
            
    def build_player(self) -> dict:
        """
        Creates a player model to submit to the api.

        Returns:
            dict: Player Model.
        """
        
        document = self.load_player_data()
        
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
        