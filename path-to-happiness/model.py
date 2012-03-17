from google.appengine.ext import db
class PathToHappiness(db.Model):
    owner = db.UserProperty(required=True)
    title=db.StringProperty()
    description=db.TextProperty()
    
class MilestoneInThePath(db.Model):
    path=db.ReferenceProperty(PathToHappiness)
    created=db.DateTimeProperty(auto_now_add=True)
    title=db.StringProperty()
    description=db.TextProprety()
    goal=db.IntegerProperty()
    progress=db.IntegerProperty()
    