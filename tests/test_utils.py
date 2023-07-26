import pytest
from src.utils import *


def test_filter_strings():
    assert filter_strings('any <p>string \rfor filter\n') == 'any string for filter'


def test_filter_salary():
    assert filter_salary(None) is None

    assert filter_salary({
        'from': 10,
        'to': 20
    }) == 15

    assert filter_salary({
        'from': 10,
        'to': None
    }) == 10

    assert filter_salary({
        'from': None,
        'to': 10
    }) == 10


@pytest.fixture()
def employers():
    return get_employers([78638])


def test_get_employers(employers):
    assert type(employers) == list

    for company in employers:
        assert company["company"].get("name") == 'Тинькофф'
