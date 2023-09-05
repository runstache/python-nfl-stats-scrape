"""
Player Helper Class to build and submit Players to the API.
"""

from sqlalchemy.orm import sessionmaker
from football_data.models import Player, Position
from football_data.repositories import PlayerRepository, PositionCodeRepository
from selenium import webdriver


class PlayerHelper:
    maker: sessionmaker

    def __init__(self, maker: sessionmaker) -> None:
        """
        Constructor.
        Args:
            maker: Session Maker
        """
        self.maker = maker

    def resolve_player(self, url: str) -> Player:
        """
        Resolves the Player against the Database. Adds the player if they do not exist.
        Args:
            url: Player Url

        Returns: Player
        """
        repo = PlayerRepository(self.maker)
        player = repo.get_player(url=url)
        if player:
            return player
        return self.build_player(url)

    def build_player(self, url: str) -> Player | None:
        """
        Builds a Player from the Url Site
        Args:
            url: Site Url

        Returns: Player
        """

        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--ignore-certificate-errors')

        browser = webdriver.Chrome(options=options)
        browser.get(url)
        player_result: dict = browser.execute_script('return window.__espnfitt__')
        browser.quit()

        player_info = player_result.get('page', {}).get('content', {}).get('player', {}).get(
            'plyrHdr', {}).get('ath', {})

        if player_info:
            position_code = player_info.get('posAbv')
            if position_code:
                pos_code_repo = PositionCodeRepository(self.maker)
                code: Position = pos_code_repo.get_position_code(code=position_code)
                player = Player(name=player_info.get('dspNm'), url=url, position_id=code.id)
                player_repo = PlayerRepository(self.maker)
                player_repo.save(player)
                return player
        return None
