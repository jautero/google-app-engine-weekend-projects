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
    def __iter__(self):
        return self
    def next(self):
        while not self.today():
            self.date+=self.date.resolution
        retdate=self.date
        self.date+=self.date.resolution
        return retdate
        
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
        raise NotImplementedError
    def in_this_week(self):
        raise NotImplementedError
    def nth_weekday(self,count,weekday=0,date=None):
        if not date:
            date=self.date
        if count<0:
            day=self.last_weekday(weekday,date)+(count+1)*7
        else:
            day=self.first_weekday(weekday,date)+(count-1)*7
        return day==date.day

    def last_weekday(self,weekday=0,date=None):
        if not date:
            date=self.date
        last_day=self.month_lengths[date.month-1]
        if last_day==28 and self.is_leapyear(date.year):
            last_day=29
        candidate=last_day-(datetime.date(date.year,date.month,last_day).weekday()-weekday)
        if candidate>last_day:
            candidate-=7
        return candidate
        
    def first_weekday(self,weekday=0,date=None):
        if not date:
            date=self.date
        candidate=1+(weekday-datetime.date(date.year,date.month,1).weekday())
        if candidate<1:
            candidate+=7
        return candidate
    def nth_dayofthisweek(self,n):
        return self.date+(n-self.date.weekday())*self.date.resolution

class helsinki_mafia_calculator(mafia_calculator):
    def today(self):
        if self.in_this_week() and self.date.weekday()==3:
            return True
        else:
            return False
    def in_this_week(self):
        return self.weekno() % 2==1

class espoo_mafia_calculator(mafia_calculator):
    def today(self):
        return self.nth_weekday(-1)

    def in_this_week(self):
        newdate=self.nth_dayofthisweek(0)
        return self.nth_weekday(-1,0,newdate)

class turku_mafia_calculator(mafia_calculator):
    def today(self):
        return self.nth_weekday(1,3)

    def in_this_week(self):
        newdate=self.nth_dayofthisweek(3)
        return self.nth_weekday(1,3,newdate)

class tampere_mafia_calculator(mafia_calculator):
    def today(self):
        return self.nth_weekday(2,1) or self.nth_weekday(4,1)

    def in_this_week(self):
        newdate=self.nth_dayofthisweek(1)
        return self.nth_weekday(2,1,newdate) or self.nth_weekday(4,1,newdate)

class jyvaskyla_mafia_calculator(mafia_calculator):
    def today(self):
        return self.nth_weekday(3,1)
        
    def in_this_week(self):
        newdate=self.nth_dayofthisweek(1)
        return self.nth_weekday(3,1,newdate)

class rising_mafia_calculator(mafia_calculator):
    def today(self):
        return self.nth_weekday(2,5)
        
    def in_this_week(self):
        newdate=self.nth_dayofthisweek(5)
        return self.nth_weekday(2,5)
        
mafiat={"helsinki":helsinki_mafia_calculator, 
        "espoo":espoo_mafia_calculator,
        "turku":turku_mafia_calculator,
        "tampere":tampere_mafia_calculator,
        "jyvaskyla":jyvaskyla_mafia_calculator,
        "rising":rising_mafia_calculator}

class format_spec:
    def __init__(self,template,filter_dict):
        self.template=template
        self.filter_dict=filter_dict

    def __str__(self):
        output=self.template % self.filter_dict
        return output

    def set_mafia_calculator(self,calculator):
        for item in self.filter_dict.values():
            try:
                item.source=calculator
            except:
                pass
