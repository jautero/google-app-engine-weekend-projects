from google.appengine.ext import db
class VoittoRivi(db.Model):
    kierros=db.IntegerProperty()
    vuosi=db.IntegerProperty()
    numerot=db.ListProperty(int)
    lisanumerot=db.ListProperty(int)
    
class LottoRivi(db.Model):
    owner=db.UserProperty(auto_current_user_add=True)
    numerot=db.ListProperty(int)

class Voittoluokat(db.Model):
    numerot_count=db.IntegerProperty()
    lisanumerot_count=db.IntegerProperty()
    plus=db.BooleanProperty(default=False)
    
    def __str__(self):
        result = "%d" % self.numerot_count
        if self.lisanumerot_count > 0:
            result += "+%d" % self.lisanumerot_count
        result += " oikein"
        return result
    

class Asetukset(db.Model):
    user=db.UserProperty(auto_current_user_add=True)
    plus=db.BooleanProperty(default=False)