from google.appengine.ext import db

class Festival(db.Model):
    name=db.StringProperty()
    month=db.IntegerProperty()
    year=db.IntegerProperty()
    switchbuffer=db.TimeProperty()
class Movie(db.Model):
    festival=db.ReferenceProperty(Festival)
    name=db.StringProperty()
    length=db.TimeProperty()
    Director=db.StringProperty()
class Screening(db.Model):
    movie=db.ReferenceProperty(Festival)
    theatre=db.StringProperty()
    starttime=db.DateTimeProperty()
    soldout=db.BooleanProperty()
