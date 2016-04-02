# -*- coding: utf-8 -*-

import sys
import time
import telepot
from settings import TOKEN
from pprint import pprint
from parsers import ParserTelegram
from database import Database, Subscription


class whentherainBot(telepot.Bot):
    def on_chat_message(self, msg):
        # content_type, chat_type, chat_id = telepot.glance(msg)
        telmsg = ParserTelegram(msg)
        user = telmsg.getUser()
        text = telmsg.getText
        print text
        # /city 'city'
        if text.startswith('/city '):
            db = Database()
            db.upd(user, ['user_id'])
            city = text[6:]
            subscr = Subscription(user_id=user.user_id, place=city)
            db.upd(subscr, ['user_id', 'place'])
            print "subscr", user, subscr
        # text
        else:
            self.sendMessage(user.user_id, u'Ничего не понимаю в: {0}, попробуйте /city "Название места"'.format(text))
            print "text", user, text

    def on_inline_query(self, msg):
        pass

    def on_chosen_inline_result(self, msg):
        pass

    def send_condition(self, id, condition):
        self.sendMessage(id, condition)

bot = whentherainBot(TOKEN)

if __name__ == '__main__':
    bot.notifyOnMessage()
    print('Listening ...')

    # Keep the program running.
    while 1:
        time.sleep(3)

__all__ = [bot]
