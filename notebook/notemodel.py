#!/usr/bin/env python
# encoding: utf-8
"""
notemodel.py

Created by Juha Autero on 2008-04-26.
Copyright (c) 2008 Juha Autero. All rights reserved.
"""

from google.appengine.ext import db
class Note(db.Model):
	id=db.StringProperty()
	title=db.StringProperty()
	content=db.StringProperty(multiline=True)
