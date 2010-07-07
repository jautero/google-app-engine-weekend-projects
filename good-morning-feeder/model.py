from google.appengine.ext import db
class datastore(db.Model):
    url=db.StrinProperty()
    greetings=db.ListProperty(string)
    latestgreeting=db.DateTimeProperty()