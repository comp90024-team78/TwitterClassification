import couchdb
class RealAPI:

    # Para@ url, usually "http://172.26.38.20"
    # para@ suburb_dir "suburb.json"
    def __init__(self, url="http://admin:admin@172.26.38.86:5984/"):
        self.db = couchdb.Server(url)['real_time_tweet']


    # find the amount of a sin happened in a city
    # date: year(2015, 2016), city: name of city
    # label: sin name
    # return a number of count
    def current_sin(self, date: str):

        results = []

        for docid in self.db.view('_all_docs'):
            item = self.db.get(docid["id"])
            #print(item)
            if date == item['date']:
                tmp = {}
                tmp['text'] = item["text"]
                tmp['coordinates'] = item["coordinates"]
                tmp['label'] = item["label"]
                results.append(tmp)
        return results

real_time_api = RealAPI()

