import requests
from credentials import creds


def country(q):
    header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 ('
                          'KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
            }
    loc = requests.get('https://maps.google.com/maps/api/geocode/json?address=' + q + '&key='+creds['geo_key'],
                     headers=header)
    res = loc.json()
    for i in res['results'][0]['address_components']:
        # print(i)
        if i['types'][0] == 'country':
            return {i['long_name'], i['short_name']}


print(country('atlanta'))

