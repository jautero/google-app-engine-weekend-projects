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

default_template_values={"project":"Limukassa", "version":"1.0", "author":"Juha Autero <jautero@iki.fi>", "copyright":"Copyright 2010 Juha Autero <jautero@iki.fi>",
  "application":"limukassa"}
import logging
import wsgiref.handlers
import os

from google.appengine.ext.webapp import template
from google.appengine.ext import webapp
from model import Account, Product

class Limukassa(webapp.RequestHandler):

  def get(self):
    template_values=dict(default_template_values)
    path = os.path.join(os.path.dirname(__file__), 'index.html')
    for key in template_values.keys():
      logging.info(key)
    output= template.render(path, template_values)
    self.response.out.write(output)
    
  def post(self):
    userid=self.request.get("userid",None)
    productid=self.request.get("productid",None)
    name=self.request.get("name",None)
    product=self.request.get("product",None)
    price=self.request.get("price",None)
    logging.info("userid: %s productid: %s name: %s product: %s price: %s" % (userid,productid,name,product,price))
    template_values=dict(default_template_values)
    account=self.get_account(template_values,userid,name)
    product=self.get_product(template_values,productid,product,price)
    if product and account:
      account.balance += product.price
      account.put()
      template_values["balance"]=account.balance/100.0 # Update balance
    path = os.path.join(os.path.dirname(__file__), 'index.html')
    self.response.out.write(template.render(path, template_values))

  def get_account(self,values,userid,name):
    balance=None
    if userid:
      account=Account.gql("where userid=:1 limit 1",userid).get()
      if not account:
        if name:
          account=Account()
          account.userid=userid
          account.name=name
          account.balance=0
          account.put()
        else:
          account=None
      else:
        balance=account.balance
        name=account.name
    else:
      account=None
    values["userid"]=userid
    if balance:
      values["balance"]=balance/100.0
    else:
      values["balance"]=0.0
    values["name"]=name
    return account
  def get_product(self,values,productid,product,price):
    if productid:
      result=Product.gql("where ean=:1 limit 1",productid).get()
      if not result:
        if price and product:
          result=Product()
          result.ean=productid
          result.name=product
          result.price=int(float(price)*100)
          result.put()
      else:
        product=result.name
        price=result.price
    else:
      result=None
    values["productid"]=productid
    values["product"]=product
    values["price"]=price
    return result
    

def main():
  application = webapp.WSGIApplication([('/', Limukassa)],
                                       debug=True)
  wsgiref.handlers.CGIHandler().run(application)


if __name__ == '__main__':
  main()
