"""
Player Helper Tests
"""

from assertpy import assert_that
import responses

from helpers.player import PlayerHelper


TEST_FILE = './tests/test_files/player.html'
API_URL = 'http://k3-main:30082/api/player'


def load_test_file() -> str:
    """
    Loads the Test File.

    Returns:
        str: String output of the file
    """

    with open(TEST_FILE, 'r', encoding='utf-8') as test_file:
        return test_file.read()


@responses.activate
def test_build_player():
    """
    Tests Building a  Player from the player page.
    """

    url = 'http://localhost/api/player/1'
    resp = responses.Response(method='GET', url=url,
                              status=200, body=load_test_file())
    responses.add(resp)

    helper = PlayerHelper(url, 'http://localhost')

    result = helper.build_player()

    assert_that(result).contains_entry({'name': 'Matthew Stafford'})\
        .contains_entry({'positionCode': 'QB'})\
        .contains_entry({'url': url})
