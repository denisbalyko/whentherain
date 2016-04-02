# -*- coding: utf-8 -*-

from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, func, Column, Integer, DateTime, String, Float, BigInteger
from sqlalchemy.orm.exc import NoResultFound

Base = declarative_base()


class Fact(Base):
    __tablename__ = 'facts'
    id = Column(Integer, primary_key=True)
    datetime = Column(DateTime)
    condition = Column(String)
    feelslike = Column(Float)
    windchill = Column(Float)
    place = Column(String)

    def __repr__(self):
       return u"<Fact(datetime='{t}', condition='{c}', feelslike='{f}')>".format(
           **{'t': self.datetime, 'c': self.condition, 'f': self.feelslike})


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    user_id = Column(BigInteger, unique=True)
    username = Column(String)
    first_name = Column(String)
    last_name = Column(String)

    def __repr__(self):
       return u"<User(id='{id}', user_id='{uid}', username='{uname}')>".format(
           **{'id': self.id, 'uid': self.user_id, 'uname': self.username})


class Subscription(Base):
    __tablename__ = 'subscriptions'
    id = Column(Integer, primary_key=True)
    user_id = Column(BigInteger)
    place = Column(String)
    condition = Column(String, default='Rain')

    def __repr__(self):
       return u"<Subscription(id='{id}', user_id='{uid}', place='{place}')>".format(
           **{'id': self.id, 'uid': self.user_id, 'place': self.place})


class Database(object):
    """docstring for Database"""
    def __init__(self):
        self.engine = create_engine('sqlite:///db.sqlite3')
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        super(Database, self).__init__()

    def add(self, item):
        self.session.add(item)
        self.session.commit()

    def upd(self, item, const_fields):

        try:
            # uniq_db_item = self.session.query(item._sa_instance_state.class_)\
            #            .filter(*dict((field, getattr(item, field)) for field in const_fields))\
            #            .one()

            q = self.session.query(item._sa_instance_state.class_)
            for field in const_fields:
                q.filter(*{field: getattr(item, field)})
            uniq_db_item = q.one()

            print 'uniq_db_item', uniq_db_item
            print 'item', item

            if set([getattr(uniq_db_item, v) for v in const_fields]) == set([getattr(item, v) for v in const_fields]):
                # @TODO рассмотреть вариант изменения данных в полях кроме const_fields и update их
                print u"Уже есть такой {0}".format(item)
        except NoResultFound:
            self.session.add(item)
            self.session.commit()

    def add_all(self, items):
        self.session.add_all(items)
        self.session.commit()

    def upd_all(self, items, const_fields):
        for item in items:
            self.upd(item, const_fields)

    def create_tables(self):
        Base.metadata.create_all(self.engine)

    def getCities(self):
        cities = self.session.query(Subscription.place)\
                             .group_by(Subscription.place)\
                             .all()
        return cities

    def getCountCities(self):
        cities = self.session.query(func.count(Subscription.place),
                                    Subscription.place)\
                             .group_by(Subscription.place)\
                             .all()
        return cities

    def getAlarming(self, place, condition='Rain'):
        users = self.session.query(User, Subscription)\
                            .filter(User.user_id == Subscription.user_id)\
                            .filter(Subscription.place == place)\
                            .filter(Subscription.condition == condition)\
                            .all()
        return users

if __name__ == '__main__':
    Database().create_tables()
    print 'database created'
