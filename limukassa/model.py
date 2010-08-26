from google.appengine.ext import db
class Account(db.Model): # A Tale of the Waking World
  userid=db.StringProperty()
  name=db.StringProperty()
  balance=db.IntegerProperty()

class Product(db.Model):
  ean=db.StringProperty()
  name=db.StringProperty()
  price=db.IntegerProperty()


