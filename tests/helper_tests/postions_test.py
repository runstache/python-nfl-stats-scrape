"""
Tests for Position Translation
"""

from src.helpers.positions import PositionHelper
from assertpy import assert_that

def test_position_translation():
    """
    Tests position translation
    """
    
    helper = PositionHelper()
    
    assert_that(helper.translate_position('Wide Receiver')).is_equal_to('WR')
    
def test_position_translation_not_found():
    """
    Test Position translation failure
    """
    
    helper = PositionHelper()
    
    assert_that(helper.translate_position('Fart')).is_none()