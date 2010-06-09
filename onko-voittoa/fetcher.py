from lottorivitmodel import VoittoRivi
from google.appengine.api import urlfetch
from google.appengine.ext import webapp
from config import lottourl
from lottoparser import LottoPageParser
import datetime
    
class RivitHandler(webapp.RequestHandler):
    def get(self):
        parser=LottoPageParser()
        response=urlfetch.fetch(lottourl)
        if response.status_code == 200:
            parser.feed(response.content)
            kierros=parser.kierros
            year=datetime.date.today().year
            if kierros>5 and datetime.date.today().month==1:
                year-=1
            rivi=VoittoRivi(kierros=kierros,vuosi=year,numerot=parser.numerot,lisanumerot=parser.lisanumerot)
            rivi.put()
