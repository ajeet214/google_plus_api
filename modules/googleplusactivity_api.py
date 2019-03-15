from googleapiclient.discovery import build
from modules.sentiment import SentimentAnalysis
import time
from credentials import creds
import requests
import bs4
# key='AIzaSyADXqoGWCJ22oEBsHIfihj39XwP6NubD5Y'


class GoogleActivity:

    def __init__(self):

        self.pos_count = 0
        self.neg_count = 0
        self.neu_count = 0
        self.key = self._get_credentials()['api_key']
        self.obj = SentimentAnalysis()
        self.result_list = []

    def _get_credentials(self):
        # change url as per credentials reequired
        url = "http://credsnproxy/api/v1/google"
        try:
            req = requests.get(url=url)
            if req.status_code != 200:
                raise ValueError
            return req.json()
        except:
            # return fallback object
            return {
                "api_key": creds['google_api_key'],
                "proxy_host": "185.193.36.122",
                "proxy_port": "23343"
            }

    def data_processor(self, item):
        new_dict = dict()
        # print(item)
        new_dict['author_url'] = item['actor']['url']
        new_dict['author_image'] = item['actor']['image']['url']
        new_dict['author_name'] = item['actor']['displayName']
        new_dict['author_userid'] = item['actor']['id']
        new_dict['polarity'] = item['polarity']
        new_dict['datetime'] = int(time.mktime(time.strptime(item['published'][:-5].replace('T', ' '),
                                                              '%Y-%m-%d %H:%M:%S'))) - time.timezone
        new_dict['title'] = item['title']
        if not new_dict['title']:
            new_dict['title'] = None

        new_dict['url'] = item['url']

        # converting the html content to normal content format
        q = bs4.BeautifulSoup(item['object']['content'], 'lxml')
        # print(q.get_text())
        new_dict['content'] = q.get_text()

        if not new_dict['content']:
            new_dict['content'] = None

        try:
            new_dict['category'] = item['object']['attachments'][0]['objectType']

            # check for post types
            if new_dict['category'] == 'article':
                new_dict['type'] = 'link'
            elif new_dict['category'] == 'photo':
                new_dict['type'] = 'image'
            elif new_dict['category'] == 'video':
                new_dict['type'] = 'video'
            elif new_dict['type'] == 'album':
                new_dict['type'] = 'image'

        except:
            new_dict['category'] = None
            new_dict['type'] = 'status'


        try:
            new_dict['thumbnail'] = item['object']['attachments'][0]['image']['url']

        except:
            new_dict['thumbnail'] = None

        try:
            new_dict['video_url'] = item['object']['attachments'][0]['embed']['url']
        except:
            new_dict['video_url'] = None

        self.result_list.append(new_dict)

    def google_activity(self, query, count=20):
        # obj = GoogleKey()
        # key = obj.keyinsert()

        c = 0
        service = build("plus", "v1", developerKey=self.key, cache_discovery=False)
        requestg = service.activities()
        k = requestg.search(query=query, maxResults=count).execute()

        for items in k['items']:
            # print(items['title'])
            pol = self.obj.analize_sentiment(items['object']['content'])
            items['polarity'] = pol

            if pol == 1:
                items['polarity'] = "positive"
                self.pos_count += 1
            elif pol == -1:
                items['polarity'] = "negative"
                self.neg_count += 1
            else:
                items['polarity'] = "neutral"
                self.neu_count += 1

            self.data_processor(items)

            c += 1
        ps = self.pos_count
        ng = self.neg_count
        nu = self.neu_count
        total = ps + ng + nu

        sentiments = dict()
        sentiments["positive"] = ps
        sentiments["negative"] = ng
        sentiments["neutral"] = nu

        return {'data': {
                        'results': self.result_list,
                        'total': c,
                        'sentiments': sentiments
                        }
                }

    # def poplesearch(self,query):
    #     service = build("people", "v1", developerKey=self.key)
    #
    #     people_resource = service.people()
    #
    #     people_document = people_resource.search(maxResults=10, query=query).execute()
    #
    #     if 'items' in people_document:
    #         print ('got page with %d' % len(people_document['items']))
    #         for person in people_document['items']:
    #             return (person['id'], person['displayName'])


if __name__ == '__main__':
    oj = GoogleActivity()
    # maximum activity search count is 20
    # print(oj.google_activity('football', 20))
    print(oj.google_activity('jumping'))
# print(oj.poplesearch("leeza"))


