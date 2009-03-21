import datetime
import logging
class filter:
    def __init__(self,yes,no,mafia_source=None):
        self.yes=yes
        self.no=no
        self.source=mafia_source
    def __str__(self):
        return None

class filter_weekly(filter):
    """This instance is for is mafia on this week"""
    def __str__(self):
        if self.source.in_this_week():
            return self.yes
        else:
            return self.no

class filter_daily(filter):
    """This instance is for is mafia on today"""
    def __str__(self):
        if self.source.today():
            return self.yes
        else:
            return self.no

class mafia_calculator:
    month_lengths=[31,28,31,30,31,30,31,31,30,31,30,31]
    def __init__(self,target_date=None):
        if target_date:
            self.date=target_date
        else:
            self.date=datetime.date.today()

    def is_leapyear(self,year=None):
        if year==None:
            year=self.date.year
        return (year%4==0 and year%100!=0 or year%400==0)

    def year_day(self):
        if self.is_leapyear() and self.date.month > 2:
            # Add leap day
            return sum(self.month_lengths[0:self.date.month-1])+self.date.day+1
        else:
            return sum(self.month_lengths[0:self.date.month-1])+self.date.day

    def weekno(self):
        year_weekday=datetime.date(self.date.year,1,1).weekday()
        weekno=((self.year_day()-1)+year_weekday)/ 7
        if year_weekday in range(0,4):
            weekno+=1
        if (weekno==53):
            if not year_weekday==3 or (year_weekday==2 and self.is_leapyear()):
                weekno=1
        if (weekno==0):
            year_weekday=datetime.date(self.date.year-1,1,1).weekday()
            if year_weekday==3 or (year_weekday==2 and self.is_leapyear(self.date.year-1)):
                weekno=53
            else:
                weekno=52
        return weekno
    def today(self):
        return None
    def in_this_week(self):
        return None

class helsinki_mafia_calculator(mafia_calculator):
    def today(self):
        if self.in_this_week() and self.date.weekday()==3:
            return True
        else:
            return False
    def in_this_week(self):
        return self.weekno() % 2==1

class format_spec:
    def __init__(self,template,filter_dict):
        self.template=template
        self.filter_dict=filter_dict

    def __str__(self):
        logging.info("Getting string representation")
        return self.template % self.filter_dict

    def set_mafia_calculator(self,calculator):
        for item in self.filter_dict.values():
            logging.info(item)
            try:
                item.source=calculator
            except:
                pass
