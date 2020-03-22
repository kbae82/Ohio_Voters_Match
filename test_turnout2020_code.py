import pytest
from fuzzywuzzy import fuzz
from dateutil.parser import parse


@pytest.mark.parametrize('birth_date_string, birth_year, result',
                         [("1977-12-12", 1977, True),
                          ("1955-06-23", 1977, False),
                          ("1912-05-01", 1912, True),
                          ("1966-05-09", 1966, True),
                          ("1952-07-12", 1953, False)])
def test_parse_year_from_date(birth_date_string, birth_year, result):
    assert (parse(birth_date_string, fuzzy=True).year == birth_year) == result


@pytest.mark.parametrize('address_input, address_data, result',
                         [("N Main Street", "MAIN ST", True),
                          ("Riverbend Drive", "RIVERBEND DR", True),
                          ("S Broadway Street", "LIBERTY ST", False),
                          ("WALNUT ST E", "E WALNUT ST", True),
                          ("Magee Jones Rd", "PEACH MOUNTAIN LN", False)])
def test_address_fuzzy_compare(address_input, address_data, result):
    assert (fuzz.partial_ratio(address_input.lower(), address_data.lower()) > 80) == result


@pytest.mark.parametrize('name_input, name_src, result',
                         [("Katherine M Inkrott", "KATHERINE MICHELLE INKROTT", True),
                          ("Young Rae", "YOUNG R JASON", True),
                          ("Ben Johnson", "BEHRLE J STEPHEN", False),
                          ("Easter Carol", "EASTER CAROLYN SUE", True),
                          ("Magee Jones", "SAM MARK LEE", False)])
def test_name_fuzzy_compare(name_input, name_src, result):
    assert (fuzz.partial_ratio(name_src.lower(), name_input.lower()) > 70 or \
            fuzz.token_sort_ratio(name_src.lower(), name_input.lower()) > 70) == result