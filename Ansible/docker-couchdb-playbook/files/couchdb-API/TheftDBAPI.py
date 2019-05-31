import couchdb
import json


class TheftDBAPI:

    # Para@ url, usually "http://172.26.38.20"
    # para@ suburb_dir "suburb.json"
    def __init__(self, url="http://admin:admin@172.26.38.86:5984/"):
        self.db = couchdb.Server(url)["theft"]

    # query theft data according to date 2015 or 2016 in a city
    # we only have data of ["Great Melbourne", "Great Syndeny" , "Canberra"]
    def query(self, city: str, year: int):
        count = 0
        mongo = {'selector': {"City": city, "Date": year},
                 'fields': ['Count']
                 }
        for row in self.db.find(mongo):
            count = row["Count"]
        return count

    def results(self):
        cities = ['melbourne', 'canberra', 'sydney']
        years = [2015, 2016]
        result = []
        for city in cities:
            for year in years:
                result.append(self.query(city, year))
        return result

theftdb = TheftDBAPI()















