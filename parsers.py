# -*- coding: utf-8 -*-

import requests
from datetime import datetime
from settings import api_key
from pprint import pprint
from database import Database, Fact, User


class Parser(object):
    """
        Parser API
    """
    pass


class ParserWeather(Parser):
    def __init__(self, query):
        super(ParserWeather, self).__init__()
        self.query = query.encode('utf-8')
        self.lang = 'RU'
        self.key = api_key
        self.api_url = "http://api.wunderground.com/api/{key}/".format(
            **{'key': self.key
               })
        self.features = "forecast"

    def forecast(self):
        json = self.request('hourly')
        hourly_forecast = (json['hourly_forecast'])
        facts = []
        for forecast in hourly_forecast:
            FCTTIME = forecast['FCTTIME']

            FCTTIMEfields = [
                FCTTIME['year'],
                FCTTIME['mon'],
                FCTTIME['mday'],
                FCTTIME['hour'],
                FCTTIME['min'],
                FCTTIME['sec']
            ]

            forecastDatetime = datetime(*list(map(int, FCTTIMEfields)))

            condition = forecast['condition']
            feelslike = float(forecast['feelslike']['metric'])
            windchill = float(forecast['feelslike']['metric'])
            place = self.query

            f = Fact(datetime  = forecastDatetime,
                     condition = condition,
                     feelslike = feelslike,
                     windchill = windchill,
                     place = place)

            facts.append(f)

        # for i, f in enumerate(facts):
        #     print i, f.datetime, f.condition

        return facts

    def request(self, feature):

        request = "{api_url}/{features}/{settings}/q/{query}.json".format(
            **{'api_url': self.api_url,
               'features': feature,
               'settings': self.lang,
               'query': self.query,
               })

        json = requests.get(request).json()

        return json


class ParserTelegram(Parser):
    def __init__(self, msg):
        super(ParserTelegram, self).__init__()
        self.msg = msg

    def getUser(self):
        user = self.msg['from']
        u = User(user_id   =user.get('id'),
                 first_name=user.get('first_name', ''),
                 last_name =user.get('last_name' , ''),
                 username  =user.get('username'  , '')
        )
        return u

    @property
    def getText(self):
        text = self.msg['text']
        return text

    @property
    def getCommand(self):
        text = self.msg['text']
        cmnds = text.split()
        try:
            cmd = cmnds[0]
            if cmd.startswith('/'):
                return cmd
            return False
        except:
            return False

    @property
    def getDate(self):
        date = self.msg['date']
        return date
