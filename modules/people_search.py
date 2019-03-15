import json
import demjson
from bs4 import BeautifulSoup
import requests
from requests_futures.sessions import FuturesSession
from concurrent.futures import ThreadPoolExecutor
from credentials import creds
import sys


class GooglePlusSearch:

    def __init__(self):
        self.proxy = self._get_proxy()
        self.session = FuturesSession(executor=ThreadPoolExecutor(max_workers=5))

    def _get_proxy(self):
        url = "http://credsnproxy/api/v1/proxy"
        try:
            req = requests.get(url=url)
            if req.status_code != 200:
                raise ValueError
            return req.json()
        except:
            return {"proxy_host": '185.121.139.55',
                    "proxy_port": '21186'}

    def search(self, search):
        header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
        }
        response = requests.get('https://plus.google.com/s/' + search + '/people', headers=header,
                                proxies={
                                    "http": "socks5://"+self.proxy['proxy_host']+':'+self.proxy['proxy_port']}).text

        # print(response)

        soup = BeautifulSoup(response, 'lxml')

        # print(soup.prettify())
        lst = []
        for x in soup.find_all("script"):
            Text = x.text
            lst.append(Text)

        content = lst[-2][86:-4]
        set = json.loads(content)
        print(set[3])
        result = {}
        output = []
        count = 0
        address_list = []

        try:
            for k in set[3]:
                # print(k)
                d = dict()
                d['url'] = "https://plus.google.com/" + k[0]
                d['userid'] = k[0]
                d['image'] = k[2][0][0]
                d['name'] = k[1]
                try:
                    d['description'] = k[12]['105913524'][1]
                except:
                    d['description'] = None
                # try:
                #     d['Subtext'] = k[12]['105913524'][2]
                #
                # except:
                #     d['Subtext'] = None
                try:
                    d['followers'] = k[12]['105913524'][4]
                except IndexError:
                    d['followers'] = None

                try:
                    d['location'] = k[12]['105913524'][3]
                except IndexError:
                    d['location'] = None
                address_list.append(d['location'])
                # if d['location'] == None:
                #     d['location'] = '@'
                #     address_list.append(d['location'])
                # else:
                #     address_list.append(d['location'])

                output.append(d)
                
                count += 1
            print(address_list)
            result['result'] = output
            result['count'] = count

            # mapping each address in the address list to their corresponding country name and country code
            rs = []
            for u in address_list:
                rs.append(self.session.get('https://maps.google.com/maps/api/geocode/json?address=' +
                                           str(u)+'&key='+creds['geo_key']))

            results = []
            for response in rs:
                temp_dict = {}
                r = response.result()
                lt = demjson.decode(r.content.decode('utf-8'))
                # print(lt)
                # print(lt['results'][0]['address_components'])
                try:
                    for i in lt['results'][0]['address_components']:
                        if i['types'][0] == 'country':
                            # print(i['long_name'])
                            temp_dict['country_code'] = i['short_name']
                            temp_dict['country'] = i['long_name']
                            results.append(temp_dict)
                except:
                    temp_dict['country_code'] = None
                    temp_dict['country'] = None
                    results.append(temp_dict)
            #
            print(results)

            result2 = result['result']
            final_list = []
            for i in range(len(result2)):
                final_dict = dict()
                final_dict['location'] = result2[i]['location']
                if result2[i]['location'] is None:
                    final_dict['country_code'] = None
                    final_dict['country'] = None
                else:
                    final_dict['country_code'] = results[i]['country_code']
                    final_dict['country'] = results[i]['country']

                final_dict['url'] = result2[i]['url']
                final_dict['userid'] = result2[i]['userid']
                final_dict['image'] = result2[i]['image']
                final_dict['name'] = result2[i]['name']
                final_dict['followers'] = result2[i]['followers']
                final_dict['description'] = result2[i]['description']
                final_dict['type'] = 'identity'
                final_list.append(final_dict)
            return final_list

        except IndexError:
            print('No result found')
            return sys.exc_info()


if __name__ == '__main__':

    obj = GooglePlusSearch()
    print(obj.search('john'))

# Test Cases
# Emmanuel Macron
# bill gates
# Nguyễn Phú Trọng
# Erna Solberg
# niger delta avengers