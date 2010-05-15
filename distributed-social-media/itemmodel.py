#!/usr/bin/env python
# encoding: utf-8
"""
itemmodel.py

Created by Juha Autero on 2010-05-15.
Copyright (c) 2010 Juha Autero. All rights reserved.
"""

from google.appengine.ext import db
from friendmodel import Friend
class Item(db.Expando):
	sender=db.ReferenceProprety(Friend)
	date=db.DateProperty()
      	title=db.StringProperty()
	content=db.StringProperty(multiline=True)
