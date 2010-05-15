#!/usr/bin/env python
# encoding: utf-8
"""
friendmodel.py

Created by Juha Autero on 2010-05-15.
Copyright (c) 2010 Juha Autero. All rights reserved.
"""

from google.appengine.ext import db
class Friend(db.Model):
	idurl=db.StringProperty()
	name=db.StringProperty()
	#cert=db.StringProprty()
