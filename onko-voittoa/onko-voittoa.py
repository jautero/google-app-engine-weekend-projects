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
copyright="Copyright 2010 Juha Autero <jautero@iki.fi>"
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
    rivit=lottorivitmodel.LottoRivi.gql("where author = :1",users.get_current_user())
    voittoluokat=lottorivitmodel.Voittoluokat.all()
    voittorivi=lottorivitmodel.VoittoRivi.gql("ORDER BY vuosi DESC,kierros DESC").get()
    tarkistaja=LottoTarkistaja(voittorivi,voittoluokat)
    voitto=False
    for rivi in rivit:
      if tarkistaja.tarkista(rivi):
        voitto=True
    template_values["rivit"]=rivit
    template_values["voitto"]=voitto
    path = os.path.join(os.path.dirname(__file__), 'index.html')
    self.response.out.write(template.render(path, template_values))

def main():
  application = webapp.WSGIApplication([('/', OnkoVoittoa), ('/tulokset', RivitHandler)],
                                       debug=True)
  wsgiref.handlers.CGIHandler().run(application)


if __name__ == '__main__':
  main()
