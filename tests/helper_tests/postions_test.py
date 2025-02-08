"""
Tests for Position Translation
"""

from src.helpers.positions import PositionHelper
from assertpy import assert_that


def translation_position():
    """
    Tests translating the Position Name to a code.
    """

    helper = PositionHelper()
    assert_that(helper.translate_position('fullback')).is_equal_to('FB')


def test_translate_position_not_present():
    """
    Tests Translating a Position not in the list.
    """

    helper = PositionHelper()
    assert_that(helper.translate_position('farts')).is_none()
