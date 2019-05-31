#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import re
import sys
import traceback
from ust import usm
import time
from multiprocessing import Queue

# Initialize model of universal sentence model
usm.definition()
 
def filter_json(tweet, city, is_raw = False):
    '''
    This method filters the raw tweet data and id, text, location and created time are left
    clean the text by getting rid of url,unicode,\n and \

    Args:
        tweet:1         A dict loaded from json-like string
        city:           Indicate which city the tweet belongs to
        is_raw          If the tweet is harvestered from tweepy, is_raw is True

    Returns:
        A dict of tweets or None if the tweet does not incclude coordinates
    '''
    t_id = tweet["id_str"] if is_raw else tweet["doc"]["id_str"]
    raw_text = tweet["text"] if is_raw else tweet["doc"]["text"]
    # Get rid of the useless content
    processed_text = re.sub('https?://[A-Za-z0-9./]+','',raw_text)
    processed_text = processed_text.encode('ascii', 'ignore').decode("utf-8")
    processed_text = processed_text.replace("\n","")
    processed_text = processed_text.replace("\\","")
    # Get coordinates of tweet.
    # If it does not include coordinates, return None to discard it
    try:
        location = getPoint(tweet, is_raw)
    except KeyError:
        location = None
    if location is None:
        return None
    # Convert the datetime format
    created_time = tweet["created_at"] if is_raw else tweet["doc"]["created_at"]
    created_time = convert_time(created_time)
    # Recreate a dict that include useful information
    filtered_tweet = {}
    filtered_tweet["_id"] = t_id
    filtered_tweet["text"] = processed_text
    filtered_tweet["coordinates"] = location
    filtered_tweet["city"] = city
    filtered_tweet["date"] = created_time
    filtered_tweet["label"] = usm.return_label(processed_text)
    return filtered_tweet

def getPoint(cur_json_obj, is_raw = False): 
    '''
    This method searches the coordinates in the two places according to whether the tweet is raw from tweepy API

    Args:
        cur_json_obj:       A dict loaded from json-like string
        is_raw:             If the tweet is harvestered from tweepy, is_raw is True

    Returns:
        A string of cooridinate ("<longitude>,<latitude>") or None
    '''

    # Raw tweets coordinate location: geo-->coordinates or coordinates-->coordinates
    # If they cannnot be found, return None
    if is_raw:
        temp_geo = cur_json_obj['geo']
        if isinstance(temp_geo, dict):
            temp_coordinates = temp_geo['coordinates']
            if isinstance(temp_coordinates, list) and len(temp_coordinates) == 2:
                temp_string = str(temp_coordinates[0])+","+ str(temp_coordinates[1])
                return temp_string

        temp_coordinates = cur_json_obj["coordinates"]
        if isinstance(temp_coordinates, dict):
            temp_coordinates2 = temp_coordinates["coordinates"]
            if isinstance(temp_coordinates2, list) and len(temp_coordinates2) == 2:
                temp_string2 = str(temp_coordinates2[0])+","+ str(temp_coordinates2[1])
                return temp_string2

    # Tweets from database coordinate location: value-->geometry-->coordinates or doc-->coordinates-->coordinates
    else:
        temp_value = cur_json_obj["value"]
        if isinstance(temp_value, dict):
            temp_geometry = temp_value["geometry"]
            if isinstance(temp_geometry, dict):
                temp_coordinates = temp_geometry["coordinates"]
                if isinstance(temp_coordinates, list) and len(temp_coordinates) == 2:
                    temp_string = str(temp_coordinates[0])+","+ str(temp_coordinates[1])
                    return temp_string

        temp_doc = cur_json_obj["doc"]
        if isinstance(temp_doc, dict):
            temp_coordinates = temp_doc["coordinates"]
            if isinstance(temp_coordinates, dict):
                temp_coordinates2 = temp_coordinates["coordinates"]
                if isinstance(temp_coordinates2, list) and len(temp_coordinates2) == 2:
                    temp_string2 = str(temp_coordinates2[0])+","+ str(temp_coordinates2[1])
                    return temp_string2
            elif isinstance(temp_coordinates, list) and len(temp_coordinates) == 2:
                temp_string = str(temp_coordinates[0])+","+ str(temp_coordinates[1])
                return temp_string
    return None

def convert_time(time_str):
    '''
    This method is used to convert the formate of date

    Args:
        time_str:       datetime format in tweet
    Returns:
        String of date in format YYYYMMDD
    '''
    result_str = time.strftime('%Y,%m,%d', time.strptime(time_str,'%a %b %d %H:%M:%S +0000 %Y'))
    return result_str

def p_tweets(queue, tweet_db, show_filtered, p_id=None):
    '''
    This method is used to filter tweet by calling filter_json method and save it into database
    Ignore those tweets that do not contain coordinates and those cannot be inserted into database
        due to duplicate '_id'
    
    Args:
        queue:          A tweets' queue that shared with harvesting process
        tweet_db:       Database that used to store the tweets
        show_filtered:  Decide whether the filtered tweets are printed
        p_id:           If using multiprocessing, the identifier of the process
    '''
    while True:
        try:
            city, line = queue.get()
        except:
            print('No tweets left')
            break
        line = line.strip()
        line = line[:-1]
        try:
            json_obj = json.loads(line)
            filtered_tweet = filter_json(json_obj, city)
            if filtered_tweet is not None:
                tweet_db.save(filtered_tweet)
                if show_filtered:
                    print('%d: %s' %(p_id, filtered_tweet))
        except:
            pass

# Test method
def test():
    q = Queue(1000)
    with open('tweet.json', 'r') as fp:
        for i, line in enumerate(fp.readlines()):
            if i > 500 or line is None:
                break
            q.put(('melbourne', line))
        fp.close()
    print(p_tweets(q))

if __name__ == '__main__':
    test()
    
