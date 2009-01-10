from google.appengine.ext import db
class KunnonKansalainen(db.Model):
  action=db.StringProperty()
  time=db.FloatProperty()
  unit=db.StringProperty()
  freq=db.StringProperty()
  total_time=db.IntegerProperty()
  date = db.DateTimeProperty(auto_now_add=True)