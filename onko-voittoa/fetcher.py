from lottorivitmodel import VoittoRivi
from google.appengine.api.labs import taskqueue
from google.appengine.api import urlfetch
from google.appengine.ext import webapp
from config import lottourl
from lottoparser import LottoPageParser
import datetime
    
class RivitHandler(webapp.RequestHandler):
    def get(self):
        tuorein_kierros=VoittoRivi.gql("ORDER BY vuosi DESC,kierros DESC").get().kierros
        taskqueue.add(self.request.path,params={"kierros":tuorein_kierros})
            
    def post(self):
        edellinen_kierros=self.request.get("kierros",None)
        parser=LottoPageParser()
        response=urlfetch.fetch(lottourl)
        if response.status_code == 200:
            parser.feed(response.content)
            kierros=parser.kierros
            year=datetime.date.today().year
            if kierros>5 and datetime.date.today().month==1:
                year-=1
            if edellinen_kierros and kierros != edellinen_kierros:
                rivi=VoittoRivi(kierros=kierros,vuosi=year,numerot=parser.numerot,lisanumerot=parser.lisanumerot)
                rivi.put()
            else:
                self.error(500)
                
