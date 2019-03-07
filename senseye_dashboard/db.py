# -*- coding: utf-8 -*-
"""
Created on Sun Mar  3 13:02:16 2019

@author: Raphael
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///test.db')
db_session = scoped_session(sessionmaker(autocommit = False,
                                         autoflush = False,
                                         bind = engine))

def init_db():
    from .models import (
            User,
            Range,
            Device,
            Measurement,
            Sensor,
            RaspberryPi
            )
    Base.metadata.create_all(bind = engine)