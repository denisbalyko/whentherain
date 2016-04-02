# -*- coding: utf-8 -*-

import json
from pprint import pprint
from database import User, Fact
from parsers import ParserTelegram, ParserWeather


def open_json(input_file_path):
        f = open(input_file_path, 'r')
        jsonobj = json.loads(''.join(f.readlines()).replace("\'", '"'))
        f.close()
        return jsonobj

jsontest = {'weather' : open_json('json/weather.json'),
            'telegram': open_json('json/telegram.json'),
            'telegramnocommand': open_json('json/telegramnocommand.json'),
            }


class ParserWeatherTest(ParserWeather):
    def __init__(self):
        super(ParserWeatherTest, self).__init__('testquery')

    def request(self, feature):
        return jsontest['weather']


class ParserTelegramTest(ParserTelegram):
    def __init__(self):
        super(ParserTelegramTest, self).__init__(jsontest['telegram'])


class ParserTelegramTestNoCommand(ParserTelegram):
    def __init__(self):
        super(ParserTelegramTestNoCommand, self).__init__(jsontest['telegramnocommand'])


InstanceWeatherTest = ParserWeatherTest()
InstanceTelegramTest = ParserTelegramTest()
InstanceTelegramTestNoCommand = ParserTelegramTestNoCommand()


def test_getUser():
    u = User(
        user_id=111222333,
        first_name='Denis',
        username='denisbalyko',
        last_name='Balyko'
    )
    u_test = InstanceTelegramTest.getUser()

    assert type(u) == type(u_test), 'type getUser'
    assert u_test.__repr__() == u.__repr__(), 'eq getUser'


def test_getHalfUser():
    u = User(
        user_id=111222333,
        first_name='Denis2',
        username='',
        last_name='BalykoTest'
    )
    u_test = InstanceTelegramTestNoCommand.getUser()

    assert type(u) == type(u_test), 'type getUser'
    assert u_test.__repr__() == u.__repr__(), 'eq getUser'



def test_getText():
    assert InstanceTelegramTest.getText == '/city Minsk', 'eq getText'
    assert InstanceTelegramTestNoCommand.getText == 'test text', 'eq getText'


def test_getCommand():
    assert InstanceTelegramTest.getCommand == '/city', 'eq getgetCommand'


def test_getNoCommand():
    assert InstanceTelegramTestNoCommand.getCommand == False, 'eq no getgetCommand'


def test_getDate():
    assert InstanceTelegramTest.getDate == 1111111111, 'eq getDate'
    assert InstanceTelegramTestNoCommand.getDate == 1112222111, 'eq getDate'

def test_forecast():
    facts = InstanceWeatherTest.forecast()
    f_test = facts[0]

    f = Fact(
        datetime='2016-03-21 21:00:00',
        condition='Mostly Cloudy',
        feelslike='-1.0',
        place='testquery'
    )

    assert type(f_test) == type(f), 'eq forecast type'
    assert f_test.__repr__() == f.__repr__(), 'eq forecast'