"""
Transalates values to position codes.
"""


class PositionHelper:
    positions: dict

    def __init__(self) -> None:
        self.positions = {
            'quarterback': 'QB',
            'runningback': 'RB',
            'widereceiver': 'WR',
            'tightend': 'TE',
            'fullback': 'FB',
            'tackle': 'T',
            'offensivetackle': 'T',
            'offensiveguard': 'G',
            'guard': 'G',
            'center': 'C',
            'defensiveend': 'DE',
            'defensivetackle': 'DT',
            'nosetackle': 'DT',
            'linebacker': 'LB',
            'cornerback': 'CB',
            'defensiveback': 'CB',
            'safety': 'S',
            'punter': 'P',
            'kicker': 'K',
            'placekicker': 'K',
            'longsnapper': 'C',
            'kickreturner': 'WR',
            'offensivelineman': 'OL'
        }

    def translate_position(self, value: str) -> str | None:
        """
        Translates the Position values based on the defined lisiting.

        Args:
            value (str): Value to translate
            
        Returns:
            str|None: Translated value or none
        """
        if value:
            return self.positions.get(value.lower().replace(' ', ''), None)
