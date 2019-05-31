import json

from flask import Flask, render_template, request, jsonify

#import the custom funtions that interacts with couch db
from TweetDBAPI import history_tweet
from RealAPI import real_time_api
from TheftDBAPI import theftdb
#name of the flask application
app = Flask(__name__)


#Set route for home page

@app.route('/')
def homepage():
    return render_template('map.html', page="Map")


#set router for comparision

@app.route('/comparision')
def comparision():

	#fetch theft data

    script_data = theftdb.results()

	#fetch data from history records

    history_data = get_history_data()

    melbourne = {'theft': {'2015': script_data[0], '2016': script_data[1]},
                 'greed': {'2015': history_data['melbourne']['2015']['greed'],
                           '2016': history_data['melbourne']['2016']['greed']}}
    canberra = {'theft': {'2015': script_data[2], '2016': script_data[3]},
                'greed': {'2015': history_data['canberra']['2015']['greed'],
                          '2016': history_data['canberra']['2016']['greed']}}
    sydney = {'theft': {'2015': script_data[4], '2016': script_data[5]},
              'greed': {'2015': history_data['sydney']['2015']['greed'],
                        '2016': history_data['sydney']['2016']['greed']}}

    #print(canberra)
    #exit()
	
	#pass data for Jinja2 template

    return render_template('comparision.html', page="Comparison", melbourne=melbourne, sydney=sydney, canberra=canberra)


@app.route('/chart')
def chart():
    list = []
	
	#fetch data from Real Time api function

    real_time_data = real_time_api.current_sin('2019,05,11')

    # sins_file = open('./sins.json', mode='r')
    # sins = sins_file.read()
    # sins_file.close()
    # sins_json = json.loads(sins)

    # print(sins_json)

    for data in real_time_data:
        if data['label'] != 'unkown':
            list.append(data)


	#convert to json so the front end supports it
    sins_json = json.loads(json.dumps(list))

    return render_template('marker_map.html', page="Chart", sins_data=sins_json)

#has the history data that was fetched from the couchdb

def get_history_data():
    history_data = {'adelaide': {'2015': {'greed': 6256, 'sloth': 15583}, '2016': {'greed': 182, 'sloth': 614}},
                    'brisbane': {'2015': {'greed': 7360, 'sloth': 21632}, '2016': {'greed': 1997, 'sloth': 7460}},
                    'canberra': {'2015': {'greed': 2962, 'sloth': 7001}, '2016': {'greed': 429, 'sloth': 1292}},
                    'hobart': {'2015': {'greed': 0, 'sloth': 0}, '2016': {'greed': 0, 'sloth': 0}},
                    'melbourne': {'2015': {'greed': 10381, 'sloth': 26475}, '2016': {'greed': 250, 'sloth': 773}},
                    'perth': {'2015': {'greed': 8247, 'sloth': 22197}, '2016': {'greed': 319, 'sloth': 1034}},
                    'sydney': {'2015': {'greed': 37489, 'sloth': 74547}, '2016': {'greed': 8699, 'sloth': 16383}}}

    return history_data

#to fetch data to display for dialog

@app.route('/map_chart')
def map_chart():
    state_id = request.args.get('state_id')

    history_data = get_history_data()

    city_name = get_map_cities(state_id)

    if city_name == 'None':
        year_data = {'2015': {'greed': 0, 'sloth': 0}}
    else:
        year_data = history_data[city_name]

    return render_template('dialog_chart.html', year_data=year_data)

#list of cities and their id from geojson
def get_map_cities(state_id):
    d = dict()

    d['7'] = 'melbourne'  # Greater Melbourne
    d['3'] = 'sydney'  # Greater Sydney
    d['11'] = 'brisbane'  # Greater Brisbane
    d['15'] = 'adelaide'  # Greater Adelaide
    d['17'] = 'darwin'  # Greater Darwin
    d['31'] = 'canberra'  # Australian Capital Territory
    d['19'] = 'perth'  # Greater Perth
    d['23'] = 'hobart'  # Greater Hobart

    if state_id in d.keys():
        return d[state_id]
    else:
        return "None"


#fetch the data from various cities to display on the map

@app.route('/get_data')
def get_data():
    list = []

    d = dict()

    d['state'] = 7  # Greater Melbourne
    # d['data'] = {'sloth': history_tweet.sin_in_city('2015,01,01', 'melbourne', 'sloth'),
    #              'greed': history_tweet.sin_in_city('2015,01,01', 'melbourne', 'greed')}

    history_data = get_history_data()

    d['data'] = {
        'sloth': history_data[get_map_cities('7')]['2015']['sloth'] + history_data[get_map_cities('7')]['2016'][
            'sloth'],
        'greed': history_data[get_map_cities('7')]['2015']['greed'] + history_data[get_map_cities('7')]['2016'][
            'greed'],
    }

    list.append(d)

    d = dict()

    d['state'] = 3  # Greater Sydney
    # d['data'] = {'sloth': history_tweet.sin_in_city('2015,01,01', 'sydney', 'sloth'),
    #              'greed': history_tweet.sin_in_city('2015,01,01', 'sydney', 'greed')}

    d['data'] = {
        'sloth': history_data[get_map_cities('3')]['2015']['sloth'] + history_data[get_map_cities('3')]['2016'][
            'sloth'],
        'greed': history_data[get_map_cities('3')]['2015']['greed'] + history_data[get_map_cities('3')]['2016'][
            'greed'],
    }

    list.append(d)

    d = dict()

    d['state'] = 11  # Greater Brisbane
    # d['data'] = {'sloth': history_tweet.sin_in_city('2015,01,01', 'brisbane', 'sloth'),
    #              'greed': history_tweet.sin_in_city('2015,01,01', 'brisbane', 'greed')}

    d['data'] = {
        'sloth': history_data[get_map_cities('11')]['2015']['sloth'] + history_data[get_map_cities('11')]['2016'][
            'sloth'],
        'greed': history_data[get_map_cities('11')]['2015']['greed'] + history_data[get_map_cities('11')]['2016'][
            'greed'],
    }

    list.append(d)

    d = dict()
    d['state'] = 15  # Greater Adelaide
    # d['data'] = {'sloth': history_tweet.sin_in_city('2015,01,01', 'adelaide', 'sloth'),
    #              'greed': history_tweet.sin_in_city('2015,01,01', 'adelaide', 'greed')}

    d['data'] = {
        'sloth': history_data[get_map_cities('15')]['2015']['sloth'] + history_data[get_map_cities('15')]['2016'][
            'sloth'],
        'greed': history_data[get_map_cities('15')]['2015']['greed'] + history_data[get_map_cities('15')]['2016'][
            'greed'],
    }

    list.append(d)

    # d = dict()
    # d['state'] = 27  # Greater Darwin
    # d['data'] = {'sloth': history_tweet.sin_in_city('2015,01,01', 'darwin', 'sloth'),
    #              'greed': history_tweet.sin_in_city('2015,01,01', 'darwin', 'greed')}

    # d['data'] = {'sloth': history_data[get_map_cities('27')]['2015']['sloth'],+'sloth': history_data[get_map_cities('27')]['2016']['sloth'],
    #            'greed': history_data[get_map_cities('27')]['2015']['greed'],+'greed': history_data[get_map_cities('27')]['2016']['greed'],
    #           }

    # list.append(d)

    d = dict()
    d['state'] = 31  # Australian Capital Territory
    # d['data'] = {'sloth': history_tweet.sin_in_city('2015,01,01', 'canberra', 'sloth'),
    #              'greed': history_tweet.sin_in_city('2015,01,01', 'canberra', 'greed')}

    d['data'] = {
        'sloth': history_data[get_map_cities('31')]['2015']['sloth'] + history_data[get_map_cities('31')]['2016'][
            'sloth'],
        'greed': history_data[get_map_cities('31')]['2015']['greed'] + history_data[get_map_cities('31')]['2016'][
            'greed'],
    }

    list.append(d)

    d = dict()
    d['state'] = 19  # Greater Perth
    # d['data'] = {'sloth': history_tweet.sin_in_city('2015,01,01', 'perth', 'sloth'),
    #              'greed': history_tweet.sin_in_city('2015,01,01', 'perth', 'greed')}

    d['data'] = {
        'sloth': history_data[get_map_cities('19')]['2015']['sloth'] + history_data[get_map_cities('19')]['2016'][
            'sloth'],
        'greed': history_data[get_map_cities('19')]['2015']['greed'] + history_data[get_map_cities('19')]['2016'][
            'greed'],
    }

    list.append(d)

    d = dict()
    d['state'] = 23  # Greater Hobart
    # d['data'] = {'sloth': history_tweet.sin_in_city('2015,01,01', 'hobart', 'sloth'),
    #              'greed': history_tweet.sin_in_city('2015,01,01', 'hobart', 'greed')}

    d['data'] = {
        'sloth': history_data[get_map_cities('23')]['2015']['sloth'] + history_data[get_map_cities('23')]['2016'][
            'sloth'],
        'greed': history_data[get_map_cities('23')]['2015']['greed'] + history_data[get_map_cities('23')]['2016'][
            'greed'],
    }

    list.append(d)

    return json.dumps(list)


#run the application in debug mode

if __name__ == "__main__":
    app.run(debug=True)
