#!/usr/bin/env python
# encoding: utf-8
"""
icalformat.py

Created by Juha Autero on 2010-04-22.
Copyright (c) 2010 Juha Autero. All rights reserved.

"""

import datetime,icalendar,uuid
import unittest


class ical_generator:
    starttime=datetime.time(18,0,0)
    endtime=datetime.time(23,59,59)
    def __init__(self,upto,event_name):
        self.source=None
        self.name=event_name
        self.count=0
        self.enddate=None
        mycal=icalendar.Calendar()
        mycal.add('prodid', '-//Onko mafia//onkomafia.appspot.com//')
        mycal.add('version', '2.0')
        self.mycal=mycal
        try:
            self.enddate=datetime.datetime.strptime(upto,"%d.%m").date()
            self.enddate=self.enddate.replace(year=datetime.date.today().year)
        except Exception, e:
            try:
                self.count=int(upto)
            except Exception, e:
                self.count=10

    def __str__(self):
        return self.mycal.as_string()
    
    def set_mafia_calculator(self,calculator):
        mycal=self.mycal
        count=0
        for date in calculator:
            count+=1
            if self.count>0 and count>self.count:
                break
            if self.enddate and date > self.enddate:
                break
            event = icalendar.Event()
            event.add('summary',self.name)
            event.add('dtstart',date)
            event.add('dtend',date)
            event.add('dtstamp',datetime.date.today())
            event['uid'] = "%s@onkomafia.appspot.org" % (uuid.uuid4())
            mycal.add_component(event)

def datetime_generator(date=None):
    """generator of datetimes for unittest"""
    if not date:
        date=datetime.date.today()
        while True:
            date+=date.resolution
            yield date
        
class ical_generatorTests(unittest.TestCase):
    def set_daycount(self,count):
        self.daycount=count
        self.enddate=datetime.date.today()+self.daycount*datetime.date.resolution        
    def setUp(self):
        self.datetester=datetime_generator()
    def test_upto_date(self):
        self.set_daycount(12)
        self.test_calendar=ical_generator(self.enddate.strftime("%d.%m"),"test event")
        self.run_calendar_test()
    def test_upto_count(self):
        self.set_daycount(14)
        self.test_calendar=ical_generator("14","test event")
        self.run_calendar_test()
    def test_upto_nonsense(self):
        self.set_daycount(10)
        self.test_calendar=ical_generator("foobar","test event")
        self.run_calendar_test()
    def run_calendar_test(self):
        self.test_calendar.set_mafia_calculator(self.datetester)
        parsed_calendar=icalendar.Calendar.from_string(str(self.test_calendar))
        curdate=datetime.date.today()
        count=0
        for component in parsed_calendar.walk():
            if component.name=="VEVENT":
                count+=1
                curdate+=curdate.resolution
                self.check_event(component,curdate)
        self.assertEqual(count,self.daycount)
        self.assertEqual(curdate,self.enddate)
    def check_event(self,component,curdate):
        self.assertEqual(component["SUMMARY"],"test event")
        self.assertEqual(component.decoded('dtstart'),curdate)
        self.assertEqual(component.decoded('dtend'),curdate)
        self.assertEqual(component.decoded('dtstamp'),datetime.date.today())
if __name__ == '__main__':
    unittest.main()