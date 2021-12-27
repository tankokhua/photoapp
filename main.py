#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
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
import jinja2
import webapp2
import os
import logging
import re

jinja_environment = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

def process_order(orderid):
    orderid = orderid.upper()
    logging.info('rawscore %s' % orderid)
    ret = 0
    
    if not re.search(r'^([0-9A-Z]+)$', orderid):
       ret = -1

    if len(orderid)!=12 and len(orderid)!=5:
       ret = -1

    group = orderid[0:2] 

    # Can't access sandbox
#   if os.path.exists("static/images/%s/%s.JPG" % (group, rawscore)):
#      logging.info('File exists')

    return ret, orderid, group 

class PhotoHandler(webapp2.RequestHandler):
    def post(self):
        try:
            status, orderid, group = process_order(self.request.get("score").strip())
        except:
            status = -1
            orderid = process_order(self.request.get("score").strip())

        if status == 0:
           status = None

        template_values = {
                           "error": status,
                           "class": group,
                           "orderid": orderid + ".JPG",
                          }
        logging.info('template_values %s' % template_values)
        template = jinja_environment.get_template('templates/answers.htm')
        self.response.out.write(template.render(template_values))

class MainHandler(webapp2.RequestHandler):
    def get(self):
        template_values = {
                             "score":"",
                          }
        template = jinja_environment.get_template('templates/index.htm')
        self.response.out.write(template.render(template_values))

app = webapp2.WSGIApplication([
                                ('/', MainHandler),
                                ('/getPhoto', PhotoHandler),
                              ], debug=True)
