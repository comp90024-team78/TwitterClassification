#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Import the necessary methods from tweepy library
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import time
from multiprocessing import Queue
import sys
from pt import filter_json
import couchdb
import json
from mygeopy import singleton_locator 

#Variables that contains the user credentials to access Twitter API from tweet_key.json
with open("tweet_key.json", "r") as fp:
    key_str = fp.readline()
    keys = json.loads(key_str)
    access_token = keys['access_token']
    access_token_secret = keys['access_token_secret']
    consumer_key = keys['consumer_key']
    consumer_secret = keys['consumer_secret']
    fp.close()

#This is a listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):
    '''
    This class is used to configure a stream API in tweepy

    Attributes:
        timeout:        The interval between two harvested tweets that include coordinates
        tweet_db:       The database that storage the real time tweets
    '''
    def __init__(self, timeout:int, tweet_db):
        StreamListener.__init__(self)
        self.timeout = timeout
        self.tweet_db = tweet_db

    def on_data(self, data):
        # The method is called when harvester tweet 
        send_to_db(self.tweet_db, data, self.timeout)
        return True

    def on_error(self, status):
        # The method that shows the error
        print(status)

def send_to_db(tweet_db, data, timeout):
    '''
    This method is used to filter the tweets that is in correct format and send to database

    Args:
        tweet_db:       The database that storage the real time tweets
        data:           The raw tweets string harvested from tweepy stream API
        timeout:        The interval between two harvested tweets that include coordinates
    '''
    tweet = json.loads(data)
    # Filter tweets that in correct format and show the tweets are raw tweet
    filtered_tweet = filter_json(tweet, None, True)
    if filtered_tweet is not None:
        # Get city according to coordinates using geopy
        filtered_tweet['city'] = singleton_locator.get_city(filtered_tweet['coordinates'])
        # Adjust the sequence of coordinate string to longitude and latitude
        lal = filtered_tweet['coordinates'].split(',')
        latitude_and_longitude = lal[1] + ',' + lal[0]
        filtered_tweet['coordinates'] = latitude_and_longitude
        # Insert file into CouchDB and ignore the duplicate tweets id
        try:
            tweet_db.save(filtered_tweet)
        except:
            pass
        print(filtered_tweet)
        time.sleep(timeout)


def main():
    # Argument of the program is timeout and the default timeout is 60 seconds
    args = sys.argv[1:]

    timeout = 60
    try:
        if len(args) > 0:
            timeout = int(args[0])
    except:
        timeout = 60

    # Initialize the interface to couchdb
    couch = None
    tweet_db = None
    try:
        with open("couchdbconfig.json", "r") as fp:
            couchdb_config = json.load(fp)
            couchdb_address = couchdb_config["address"]
            db_name = couchdb_config["real_db_name"]
            couch = couchdb.Server(couchdb_address)
            tweet_db = couch[db_name]
            fp.close()
    except:
        print('Error! couchdb configure failed')
        exit()

    if couch == None or tweet_db == None:
        print('Error! couchdb configure failed')
        exit()

    # This handles Twitter authetification and the connection to Twitter Streaming API
    l = StdOutListener(timeout, tweet_db)
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)

    # Filter the tweets that is form Australia
    stream.filter(locations=[113.8, -43.65, 153.8, -10.8])

    print('Finish.')

if __name__ == '__main__':
	main()
