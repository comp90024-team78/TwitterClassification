import couchdb
import json


class TweetDBAPI:

    # Para@ url, usually "http://172.26.38.20"
    # para@ suburb_dir "suburb.json"
    def __init__(self, url="http://admin:admin@172.26.38.86:5984/"):
        self.db = couchdb.Server(url)['history_tweets']
        self.viewid = '_design/day_data_view/_view/day_view'


    # find the amount of a sin happened in a city
    # date: year(2015, 2016), city: name of city
    # label: sin name
    # return a number of count
    def sin_in_city(self, date: str, city: str, label: str):
        count = 0
        for row in self.db.view(self.viewid, group_level=3):
            if row["key"][0]==city and date in row["key"][1] and label==row["key"][2]:
               count += row["value"]

        return count



history_tweet = TweetDBAPI()

#
# cities = ["adelaide", "brisbane", "canberra", "hobart", "melbourne", "perth", "sydney"]
#
# years = ["2015", "2016"]
# labels = ["greed", "sloth"]
# tmp = {}
# for city in cities:
#     tmp[city] = {}
#     for year in years:
#         tmp[city][year] = {}
#         for label in labels:
#             tmp[city][year][label] = test.sin_in_city(year, city, label)
#
# print(tmp)




