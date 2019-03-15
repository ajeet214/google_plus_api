import pytest
from modules.googleprofile import GoogleProfile


def object_search(query):
    obj = GoogleProfile()
    result = obj.google_profile(query)
    return result


@pytest.mark.parametrize("name", ['113551191017950459231', '116122068057813357635'])
def test_profile_search(name):
    result1 = object_search(name)
    try:
        assert type(result1['profile_url']) == str
        # assert i['profile_url'].startswith('http')
        assert result1['profile_url'] != ""
    except AssertionError:
        assert result1['profile_url'] is None

    try:
        assert result1['objtype'] != ""
        assert type(result1['objtype']) == str
    except AssertionError:
        assert result1['objtype'] is None

    try:
        assert result1['etag'] != ""
        assert type(result1['etag']) == str
    except AssertionError:
        assert result1['etag'] is None

    assert type(result1['linked_urls']) == list

    try:
        assert result1['tagline'] != ""
        assert type(result1['tagline']) == str
    except AssertionError:
        assert result1['tagline'] is None

    try:
        assert result1['type'] != ""
        assert type(result1['type']) == str
    except AssertionError:
        assert result1['type'] is None

    try:
        assert result1['cover_photo'] != ""
        assert type(result1['cover_photo']) == str
    except AssertionError:
        assert result1['cover_photo'] is None

    try:
        assert result1['image'] != ""
        assert type(result1['image']) == str
    except AssertionError:
        assert result1['image'] is None

    try:
        assert result1['aboutMe'] != ""
        assert type(result1['aboutMe']) == str
    except AssertionError:
        assert result1['aboutMe'] is None

    assert type(result1['userid']) == int

    assert type(result1['circledByCount']) == int
    assert result1['type'] is 'identity'




