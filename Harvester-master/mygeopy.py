#!/usr/bin/env python
# -*- coding: utf-8 -*-
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
import re

class mygeolocator:
    '''
    This class is based on geopy to search location according to coordinates

    Attributes:
        geolocator:     The object used to search location
        reverse:        The method used to convert coordinate to location information and 
                            is set the minimum delay ensure not to visit the geopy server excessively frequently
    '''

    def __init__(self, user_agent_name):
        '''
        Args:
            user_agent_name: Identifier of the geolocator
        '''
        self.geolocator = Nominatim(user_agent=user_agent_name)
        self.reverse = RateLimiter(self.geolocator.reverse, min_delay_seconds=0.3)

    def get_suburb(self, latitude_longitude):
        '''
        Args:
            latitude_and_longitude: string latitude and longitude (e.g."-37.807367, 144.962112")
        Return:
            String of suburb or None if thereis no information of the coordinates

        '''
        location = self.reverse(latitude_longitude, timeout=5)
        if isinstance(location.raw, dict) and 'address' in location.raw:
            if isinstance(location.raw['address'], dict) and 'suburb' in location.raw['address']: 
                return location.raw['address']['suburb']
        return None

    def get_city(self, latitude_longitude):
        '''
        Args:
            latitude_and_longitude: string latitude and longitude (e.g."-37.807367, 144.962112")
        Return:
            String of city or None if thereis no information of the coordinates

        '''
        location = self.reverse(latitude_longitude, timeout=5)
        if isinstance(location.raw, dict) and 'address' in location.raw:
            if isinstance(location.raw['address'], dict) and 'county' in location.raw['address']:
                city = location.raw['address']['county']
                city = city.lower()
                if 'city of' in city:
                    city_list = re.findall(r"city of (.*)",city)
                    if isinstance(city_list, list) and len(city_list) == 1:
                        return city_list[0].strip()
                else:
                    return city
        return None

# Singleton of the object to ensure not creating too much agents
singleton_locator = mygeolocator('tweet_harvester')

# test
if __name__ == '__main__':
    geolocator = singleton_locator
    print(geolocator.get_city('-37.9168282, 145.1452637'))


