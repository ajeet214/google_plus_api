import requests
import json
from credentials import creds
#from pymongo import MongoClient
import bs4


class GoogleProfile():
    # def mongoinsertion(self,data):
    #     client=MongoClient()
    #     db=client.googleprofiledb
    #     collection=db.googleprofilecol
    #     collection.insert(data)

    def __init__(self):

        self.key = self._get_credentials()['api_key']

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
                # "email": "fraserjonathan423@gmail.com",
                # "password": "jeeJ5Hei0ee",
                "api_key": creds['google_api_key'],
                "proxy_host": "185.193.36.122",
                "proxy_port": "23343"
            }

    def google_profile(self, userId):

        d={}
        # key="AIzaSyDIduQkgDj-v0s0uwKJNje2wTaB5gLDt_c"
        url = "https://www.googleapis.com/plus/v1/people/"+userId+"?key="+self.key
        header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
        }
        res = requests.get(url, headers=header)
        # print(result.text)
        r = (json.loads(res.text))
        # print(r)

        try:
            d["type"] = r["kind"]
        except KeyError:
            d["type"] = None
        try:
            d["etag"] = r["etag"]
        except KeyError:
            d["etag"] = None
        try:
            d["objtype"]=r["objectType"]
        except KeyError:
            d["objtype"] = None
        d["userid"] = int(r["id"])
        d["profile_url"] = r["url"]
        d["displayname"] = r["displayName"]

        try:
            d["tagline"] = r["tagline"]
        except:
            pass
        try:
            d["cover_photo"] = r["cover"]['coverPhoto']['url']
        except:
            pass

        try:
            d["placesLived"] = r["placesLived"]
        except:
            pass

        try:
            d["organizations"] = r["organizations"]
        except:
            pass

        try:
            d["nickname"] = r["nickname"]
        except:
            pass

        try:
            d["occupation"] = r["occupation"]
        except:
            pass

        try:
            d["skills"] = r["skills"]
        except:
            pass

        try:
            d["gender"] = r["gender"]
        except:
            pass
        try:
            d["braggingRights"] = r["braggingRights"]
        except:
            pass

        try:
            d["linked_urls"] = r["urls"]
        except:
            pass

        try:
            a = bs4.BeautifulSoup(r["aboutMe"], 'lxml')
            d["aboutMe"] = a.get_text()

        except:
            pass

        try:
            d["name"] = r["name"]
        except:
            pass

        d["image"] = r["image"]["url"]
        try:
            d["circledByCount"] = r["circledByCount"]
        except:
            pass
        d['type'] = 'identity'
        # self.mongoinsertion({"result":d})
        # return {'result': d}
        return d


if __name__ == '__main__':
    obj = GoogleProfile()
    print(obj.google_profile("113551191017950459231"))

#113551191017950459231

# "116122068057813357635"