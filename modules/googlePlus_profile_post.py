import requests
from credentials import creds
import datetime
import bs4
from modules.sentiment import SentimentAnalysis


class ProfilePost:

    def __init__(self):

        self.obj = SentimentAnalysis()
        self.headers = {
            'user-agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36"
                        }

    def data_processor(self, data):

        temp_list = list()
        for i in data:
            # print(i)
            temp_dict = dict()
            temp_dict['datetime'] = int(datetime.datetime.strptime(i['published'].split('.')[0].replace(
                'T', ' '), '%Y-%m-%d %H:%M:%S').timestamp())
            temp_dict['author_url'] = i['actor']['url']
            temp_dict['author_userid'] = i['actor']['id']
            temp_dict['author_name'] = i['actor']['displayName']
            temp_dict['author_image'] = i['actor']['image']['url'].split('=')[0]+'=800'
            temp_dict['url'] = i['url']

            # converting the html content to normal content format
            q = bs4.BeautifulSoup(i['object']['content'], 'lxml')
            # print(q.get_text())
            temp_dict['content'] = q.get_text()

            try:
                temp_dict['type'] = i['object']['attachments'][0]['objectType']

                # checking for type of posts
                if temp_dict['type'] == 'article':
                    temp_dict['type'] = 'link'
                elif temp_dict['type'] == 'photo':
                    temp_dict['type'] = 'image'
                elif temp_dict['type'] == 'album':
                    temp_dict['type'] = 'image'
                elif 'video' in temp_dict['type']:
                    temp_dict['type'] = 'video'

            except KeyError:
                temp_dict['type'] = 'status'

            temp_dict['title'] = i['title']
            if not temp_dict['title']:
                temp_dict['title'] = None

            if not temp_dict['content']:
                temp_dict['content'] = None

            try:
                pol = self.obj.analize_sentiment(temp_dict['content'])
            except TypeError:
                pol = 0

            if pol == 1:
                temp_dict['polarity'] = "positive"
            elif pol == -1:
                temp_dict['polarity'] = "negative"
            else:
                temp_dict['polarity'] = "neutral"

            try:
                temp_dict['thumbnail'] = i['object']['attachments'][0]['url']
            except:
                temp_dict['thumbnail'] = None

            temp_list.append(temp_dict)

        return temp_list

    def post_fetcher(self, userid):

        url = "https://www.googleapis.com/plus/v1/people/{}/activities/public?key={}&maxResults=100".format(
            userid, creds['google_api_key'])

        response = requests.get(url, headers=self.headers).json()
        posts = response['items']
        print(posts)
        return self.data_processor(posts)


if __name__ == '__main__':
    obj = ProfilePost()
    print(obj.post_fetcher('109506789978661910886'))

# 109506789978661910886
# 102273141544808273467
# 106882490785012474431
