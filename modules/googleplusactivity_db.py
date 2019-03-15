from pymongo import MongoClient
from modules.googleplusactivity_api import GoogleActivity
from config import Config


class ActivitySearch:

    def __init__(self):

        self.client = MongoClient(Config.DATABASE_CONFIG['host'], Config.DATABASE_CONFIG['port'])
        db = self.client.googleplus_db
        self.collection = db.activity
        self.dict = {}
        self.obj = GoogleActivity()

    def db_check(self, query):

        r = self.obj.google_activity(query)
        print(r)
        t = 0
        for i in r['data']['results']:
            if self.collection.find_one({'url': i['url']}):
                pass
            else:
                # print(i)
                t += 1
                self.collection.insert_one(i)
        self.client.close()
        print('no. of stored pages', t)
        # self.loop.close()

        results = self.db_fetch(query)
        #
        # # return {'results': m}
        return {'data': results}

  # ---------------------fetching total number of query pages from database----------------------------------------
    def db_fetch(self, query):
        self.collection.create_index([("title", "text"), ("content", "text"), ("author_name", "text"), ("author_image", "text")])

        lst = []
        cursor = self.collection.find(
            {"$text": {"$search": query}},
            {'score': {'$meta': "textScore"}}).sort([('score', {'$meta': "textScore"})])
        total = cursor.count()
        n = 0
        for i in cursor:
            # print(i)
            i.pop('_id')
            lst.append(i)
            n += 1

        # print('fetched pages from db', len(lst))
        # return {'results': lst,
        #         'total': n}
        return lst


if __name__ == '__main__':
    obj = ActivitySearch()
    print(obj.db_check("rolling"))

