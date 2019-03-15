import pytest
from modules.googlePlus_profile_post import ProfilePost


@pytest.mark.parametrize("id", ['102273141544808273467', '109506789978661910886'])
def test_profile_post(id):
    obj = ProfilePost()
    response = obj.post_fetcher(id)

    for i in response:

        try:
            assert type(i['author_image']) == str
            assert i['author_image'].startswith('http')
            assert i['author_image'] != ""
        except AssertionError:
            assert i['author_image'] is None

        try:
            assert i['content'] != ""
            assert type(i['content']) == str
        except AssertionError:
            assert i['content'] is None

        try:
            assert type(i['author_url']) == str
            assert i['author_url'].startswith('http')
            assert i['author_url'] != ""
        except AssertionError:
            assert i['author_url'] is None

        try:
            assert type(i['url']) == str
            assert i['url'].startswith('http')
            assert i['url'] != ""
        except AssertionError:
            assert i['url'] is None

        assert type(i['author_userid']) == str

        try:
            assert i['polarity'] != ""
            assert type(i['polarity']) == str
        except AssertionError:
            assert i['polarity'] is None

        assert i['type'] is 'video' or i['type'] is 'image' or i['type'] is 'link' or i['type'] is 'status'

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

        try:
            assert i['title'] != ""
            assert type(i['title']) == str
        except AssertionError:
            assert i['title'] is None

        assert i['type'] == 'link' or i['type'] == 'image' or i['type'] == 'status' or i['type'] == 'video'













