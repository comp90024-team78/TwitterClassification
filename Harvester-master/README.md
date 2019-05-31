# Harvester
This is used to harvester tweets from history tweet database and real time steam API.

harvester.py is the main entrance of the harvesting history tweets.

1.1 Overview
According to requirements of this project, a system utilizing NoSQL database CouchDB and tweets harvesters is needed to support the data analysis afterwards. With CouchDB, a document-based database, a great number of tweets in json format can be stored. Moreover, with support of MapReduce, CouchDB allows for creating views of the documents to group the data that are often retrieved. Other data, such as AURIN data are also stored in the CouchDB.

1.2 Harvester
1.2.1 Harvester overview
There are two programs doing different harvester work, harvester of history tweets and real time tweets. The former collects the data	 on the	UniMelb Research Cloud while the latter fetches tweets by accessing Streaming API supported by tweepy library.

1.2.2	History tweets harvester
The first harvester is defined in “harvester.py”, which is used to collect historic tweets from database provided. After getting the cities that we are interested in, the process starts a process that grabs tweets by running shell file, raw_twitter.sh, and put each line into the queue. Meanwhile, a multiprocessing pool will run the filtering processes to remove tweets that do not contain coordinates and then insert them into the database. As shown below, the queue can be considered as a buffer that controls the reading speed. When the queue is full, the harvester process would be blocked until the filtering processes get several tweets from the queue, which ensure the memory leak would not occur due to a great number of tweets downloaded at the same time. Additionally, the filtering processes keep running so whenever the queue contains tweets, they will get them separately, discard the useless ones and save them in database.

1.2.3	Real-time tweets harvester
The second harvester utilizes Streaming API instead of Search API. In this harvester, the real time tweets that has coordinates are collected every minute. Specifically, the harvester keeps grabbing tweets until it finds coordinates in a tweet which will be saved in database. Once the tweet is saved, the harvester will then wait for a minute to continue harvesting, as classification needs a while, which will be explained later. If the tweets with coordinates are not found, the harvester keep searching instead of waiting.
There are some reasons that we choose Streaming API instead of Search API. Firstly, there is limitation of frequency of requests for Search API, while Streaming API maintain a persistent HTTP connection and it works in a request-reply way, so with Streaming API, the access to tweets will have less latency. Secondly, some tweets collected through Search API cannot be indexed,  so it is hard to remove duplicated tweets. Thirdly, Streaming API provides a filter so it can be used to get tweets in a range of location.

1.2.4 Duplicate Tweets Handling
As we consider the tweets with same id are duplicate, when tweets are inserted into database, the ids of tweets are set to be the ids of documents and those tweets with same id will only be inserted once. In both harvester, when the processes catch the exception of “bad request” sent from database, they will discard this kind of tweets.

1.2.5 Geographical Information
This part is only used in real-time harvester, as the historic tweets are fetched according to the city list defined before. To convert coordinates to city where the tweets were sent, geopy library is used. At the beginning, we considered the query of location information is executed locally. However, when the frequency of query increases, an http error about connection refused occurs because the query is actually based on http connection between clients and servers, and if the frequency of visits to the server is excessively large, the server will cancel the connection and refuse the connection for a few minutes. To solve this problem, RateLimiter in geopy library is utilized to set minimum delay between two requests so the connection will not be cancelled in this case. Afterwards, the detail information, including suburb, county, will be got from geopy server. If the coordinates of the real-time tweets cannot be converted by geopy, these tweets are discarded, and the harvester will continue searching for others.

2. Usage
Firstly, run  
  source harvester_pip.sh
  
For History tweets harvester

Step 1: Configure cities in city .json and CouchDB connection in couchdbconfig.json

Step 2: Run the python script on background:
  "python harvester.py [start date] [end date] >> ht.txt  &"
 
where start date and end date are in format “YYYYMMDD” and ht.txt will show which dates and cities the tweets belong to are finished.

For real time tweets harvester

Step 1: Configure CouchDB connection in couchdbconfig.json

Step 2: Run the python script on background:
  "python harvester_real_time.py [timeout] >> ht.txt  &"
where timeout is an integer defining how many seconds will be wait for after the harvester insert a tweet.

