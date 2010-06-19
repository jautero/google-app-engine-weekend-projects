#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Copyright 2008 Juha Autero
#
# Copyright 2010 Juha Autero <jautero@iki.fi>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

project="Onko Voittoa"
version="1.0"
author="Juha Autero <jautero@iki.fi>"
copyright="Copyright &copy; 2010 Juha Autero <jautero@iki.fi>"
application="onko-voittoa"
import wsgiref.handlers
import os

from google.appengine.ext.webapp import template
from google.appengine.ext import webapp
from google.appengine.api import users

from fetcher import RivitHandler
from tarkista import LottoTarkistaja

import lottorivitmodel

class OnkoVoittoa(webapp.RequestHandler):

  def get(self):
    template_values=globals()
    current_user=users.get_current_user()
    asetukset=lottorivitmodel.Asetukset.gql("where user = :1", current_user).get()
    if not asetukset:
      asetukset=lottorivitmodel.Asetukset()
    rivit=lottorivitmodel.LottoRivi.gql("where owner = :1",current_user)
    voittoluokatplus=lottorivitmodel.Voittoluokat.all()
    voittoluokatnormaali=lottorivitmodel.Voittoluokat.gql("where plus=False")
    voittorivi=lottorivitmodel.VoittoRivi.gql("ORDER BY vuosi DESC,kierros DESC").get()
    if asetukset.plus:
        voittoluokat=voittoluokatplus
    else:
        voittoluokat=voittoluokatnormaali
    tarkistaja=LottoTarkistaja(voittorivi,voittoluokat)
    voitto=False
    template_values["logouturl"]=users.create_logout_url("/")
    template_values["voittorivi"]=voittorivi.numerot
    template_values["lisanumerot"]=voittorivi.lisanumerot
    template_values["kierros"]="%d/%d" % (voittorivi.kierros,voittorivi.vuosi)
    template_values["rivit"]=[]
    for rivi in rivit:
      template_values["rivit"].append(rivi.numerot)
      if tarkistaja.tarkista(rivi.numerot):
        voitto=True
    template_values["voitto"]=voitto
    if asetukset.plus:
      template_values["pluschecked"]="checked"
    else:
      template_values["pluschecked"]=""
    path = os.path.join(os.path.dirname(__file__), 'index.html')
    self.response.out.write(template.render(path, template_values))
    
  def post(self):
    id=self.request.get("id",None)
    if id:
      rivi=lottorivitmodel.LottoRivi.gql("where owner = :1 and id = :2",users.geet_current_user(),id)
    else:
      rivi=lottorivitmodel.LottoRivi()
    rivi.numerot=[int(n) for n in self.request.get_all("number")]
    rivi.put()
    self.get()

class VoitotHandler(webapp.RequestHandler):

      def get(self):
        template_values=globals()
        voittoluokat=lottorivitmodel.Voittoluokat.all()
        template_values["luokat"]=[]
        for luokka in voittoluokat:
          template_values["luokat"].append((luokka.numerot_count,luokka.lisanumerot_count,luokka.plus))
        path = os.path.join(os.path.dirname(__file__), 'voitot.html')
        self.response.out.write(template.render(path, template_values))

      def post(self):
        rivi=lottorivitmodel.Voittoluokat()
        rivi.numerot_count=int(self.request.get("numerot"))
        rivi.lisanumerot_count=int(self.request.get("lisanumerot"))
        rivi.plus=(self.request.get("plus","false")=="true")
        rivi.put()
        self.get()
        
class AsetuksetHandler(webapp.RequestHandler):
  def get(self):
    self.redirect("/")
  def post(self):
    asetukset=lottorivitmodel.Asetukset.gql("where owner = :1", users.get_current_user()).get()
    if not asetukset:
      asetukset=lottorivitmodel.Asetukset()
    asetukset.plus=(self.request.get("plus","false")=="true")
    asetukset.put()
    self.get()

def main():
  application = webapp.WSGIApplication([('/', OnkoVoittoa), ('/tulokset', RivitHandler), ("/voitot", VoitotHandler),
                                        ('/asetukset', AsetuksetHandler)],
                                       debug=True)
  wsgiref.handlers.CGIHandler().run(application)


if __name__ == '__main__':
  main()
