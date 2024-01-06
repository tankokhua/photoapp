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
from flask import Flask, render_template, request
import os
import logging
import re

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)

def process_order(orderid):
    orderid = orderid.upper()
    logging.info('photoid %s' % orderid)
    ret = 0
    
    if not re.search(r'^([0-9A-Z]+)$', orderid):
       ret = -1

    if len(orderid)!=12 and len(orderid)!=5:
       ret = -1

    group = orderid[0:2] 

    # Can't access sandbox
    if not os.path.exists("static/images/%s/%s.JPG" % (group, orderid)):
       logging.info('Photo for %s does not exist.' % orderid)
       ret = -1

    return ret, orderid, group 

@app.route('/getPhoto', methods=['GET', 'POST'])
def PhotoHandler():
    try:
        status, orderid, group = process_order(request.form.get("photoid").strip())
    except:
        status = -1
        orderid = process_order(request.form.get("photoid").strip())

    if status == 0:
       status = None

    _orderid = orderid + ".JPG"

    return render_template("answers.htm", error=status, classid=group, orderid=_orderid)

@app.route('/', methods=['GET', 'POST'])
def MainHandler():
    return render_template("index.htm", photoid="")

if __name__ == '__main__':
   app.run(host='127.0.0.1', port=8080, debug=True)
