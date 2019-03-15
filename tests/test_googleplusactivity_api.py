import pytest
from modules.googleplusactivity_api import GoogleActivity


def object_search(query):
    obj = GoogleActivity()
    result = obj.google_activity(query)
    return result


@pytest.mark.parametrize("name", ['billiards','jump'])
def test_activity_search(name):
    result1 = object_search(name)
    for i in result1['data']['results']:
        try:
            assert type(i['url']) == str
            assert i['url'].startswith('http')
            assert i['url'] != ""
        except AssertionError:
            assert i['url'] is None

        try:
            assert type(i['author_url']) == str
            assert i['author_url'].startswith('http')
            assert i['author_url'] != ""
        except AssertionError:
            assert i['author_url'] is None

        try:
            assert type(i['author_image']) == str
            assert i['author_image'].startswith('http')
            assert i['author_image'] != ""
        except AssertionError:
            assert i['author_image'] is None

        try:
            assert i['polarity'] != ""
            assert type(i['polarity']) == str
        except AssertionError:
            assert i['polarity'] is None

        try:
            assert i['content'] != ""
            assert type(i['content']) == str
        except AssertionError:
            assert i['content'] is None

        try:
            assert i['title'] != ""
            assert type(i['title']) == str
        except AssertionError:
            assert i['title'] is None

        try:
            assert i['category'] != ""
            assert type(i['category']) == str
        except AssertionError:
            assert i['category'] is None

        try:
            assert i['author_name'] != ""
            assert type(i['author_name']) == str
        except AssertionError:
            assert i['author_name'] is None

        try:
            assert i['thumbnail'] != ""
            assert type(i['thumbnail']) == str
        except AssertionError:
            assert i['thumbnail'] is None

        assert type(i['datetime']) == int
        assert type(i['author_userid']) == str

        assert i['type'] is 'video' or i['type'] is 'image' or i['type'] is 'link' or i['type'] is 'status'





