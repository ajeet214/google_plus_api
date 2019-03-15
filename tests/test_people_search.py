import pytest
from modules.people_search import GooglePlusSearch


def search(name):
    obj = GooglePlusSearch()
    return obj.search(name)


@pytest.mark.parametrize("query", ['trump', 'Nguyễn Phú Trọng'])
def test_people_search(query):
    res = search(query)
    for i in res:

        try:
            assert type(i['url']) == str
            assert i['url'].startswith('http')
            assert i['url'] != ""
        except AssertionError:
            assert i['url'] is None

        try:
            assert type(i['country']) == str
            assert i['country'] != ""
        except AssertionError:
            assert i['country'] is None

        try:
            assert type(i['country_code']) == str
            assert i['country_code'] != ""
            assert len(i['country_code']) == 2
        except AssertionError:
            assert i['country_code'] is None

        try:
            assert type(i['location']) == str
            assert i['location'] != ""
        except AssertionError:
            assert i['location'] is None

        try:
            assert type(i['name']) == str
            assert i['name'] != ""
        except AssertionError:
            assert i['name'] is None

        try:
            assert i['description'] != ""
            assert type(i['description']) == str
        except AssertionError:
            assert i['description'] is None

        try:
            assert i['image'] != ""
            assert type(i['image']) == str
            assert i['image'].startswith('http')
        except AssertionError:
            assert i['image'] is None

        assert type(i['userid']) == str
        assert i['type'] is 'identity'






