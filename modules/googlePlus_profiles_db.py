from modules.googleprofile import GoogleProfile
from pymongo import MongoClient
from config import Config


class ProfileFetch:

    def __init__(self):

        self.client = MongoClient(Config.DATABASE_CONFIG['host'], Config.DATABASE_CONFIG['port'])
        db = self.client.googleplus_db
        self.collection = db.plus_profile
        self.obj1 = GoogleProfile()

    def fetcher(self, q):

        result = self.obj1.google_profile(q)
        # print(result)
        return result

    def db_check(self, r):

        # print(r['profile_url'])
        # if database consists the profile
        if self.collection.find_one({'userid': r}):

            for doc in self.collection.find({'userid': r}):
                # print(doc)
                doc.pop('_id')
                # self.dict['profileExists'] = doc['profileExists']
                # self.dict['profile_id/num'] = doc['profile_id/num']
                #
                return {'data':
                            {'results': doc}}

        # when profile isn't in database
        else:
            data_from_fb = self.fetcher(r)
            data_from_fb['userid'] = str(data_from_fb['userid'])
            # print(data_from_fb)
            self.db_loader(data_from_fb)
            data_from_fb.pop('_id')

            return {'data':
                        {'results': data_from_fb}}

    def db_loader(self, data):

        # print(data)
        self.collection.insert_one(data)

        # close db connection
        self.client.close()


if __name__ == '__main__':
    obj = ProfileFetch()
    print(obj.db_check("105723085886093318643"))

# 113551191017950459231
# 110107458243955110887