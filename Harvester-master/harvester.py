#!/usr/bin/env python
# -*- coding: utf-8 -*-
import subprocess
from multiprocessing import Queue, Process
import time, random
import mypanda
import json, sys
import couchdb
import traceback
import threading
from collections import Counter
from collections import defaultdict
from ust import usm
from pt import p_tweets

def get_cities():
    '''    
    Read the city list from json file

    Returns        
        List of cities
    '''
    result_list = []
    with open('city.json', 'r') as f:
        city_dict = json.load(f)
        for city_list in city_dict.values():
            result_list.extend(city_list)
        f.close()
    return result_list

def h_tweets(city_list, start_date:str, end_date:str, queue):

    '''
    Harvester historic tweets from database by raw_twitter.sh

    Args:
        city_list:       A list of cities
        start_date:      The date starting to harvester, format: YYYYMMDD
        end_date:        The end date of harvester, format: YYYYMMDD
        queue            The queue used to as a buffer that stores the tweets json string

    '''

    # date_range stores the list of every date between start_date and end_date
    date_range = mypanda.get_date_range(start_date, end_date)
    for date_str in date_range: 
        for city in city_list:
            # Call the sh file and run it in subprocess 
            cmd = './raw_twitter.sh ' + city + ' ' + date_str + ' ' + date_str
            sub = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            # Get the stdout andd stderr of the subprocess
            out, err = sub.communicate()
            lines = str(out, encoding = "utf-8")
            lines = lines.splitlines()
            sys.stdout.write(cmd + ': ' + str(len(lines)) + '\n')
            # For each line, put it into the queue
            for line in lines:
                queue.put((city, line)) 
            # Since harvesting is much faster than processing, it is safer to pause a while
            time.sleep(10)

def main():
    '''
    Main entrance of this program.
    '''
    # args store two arguments of this program and ensure there are two arguments
    args = sys.argv[1:]
    if len(args) != 2:
        print('Error! 2 date needed (format:YYYYMMDD)')
        exit()
    start_date = args[0]
    end_date = args[1]

    # Get list of cities
    global city_list
    city_list = get_cities()
    print(city_list)

    # Initialize the interface to CouchDB
    couch = None
    tweet_db = None
    try:
        with open("couchdbconfig.json", "r") as fp:
            couchdb_config = json.load(fp)
            couchdb_address = couchdb_config["address"]
            db_name = couchdb_config["history_db_name"]
            print(couchdb_address)
            print(db_name)
            couch = couchdb.Server(couchdb_address)
            tweet_db = couch[db_name]
            fp.close()
    except:
        traceback.print_exc()
        print('Error! Reading couchdb configure failed')
        exit()

    if couch == None or tweet_db == None:
        print('Error! couchdb configure failed')
        exit()

    # q is a queue buffering the harvestered tweets
    q = Queue(10000)
    # hp is a process that harvester tweets from database so that it will not block the main process
    hp = Process(target = h_tweets, args = (city_list, start_date, end_date, q,))
    hp.start()

    
    # Processing tweets using pt.p_tweets
    p_tweets(q, tweet_db, False)

    print('Finish.')


if __name__ == '__main__':
    main()

