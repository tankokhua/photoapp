#!/usr/bin/env python
import jinja2
import webapp2
import os
import logging
import re
import time
import datetime
import random
import csv
from os import getenv
from google.appengine.ext import db
from google.appengine.api import mail
from google.appengine.api import users
from kinds import *
import json

USE_JSON = True

HOUSES = {
                1:"Ravenclaw",
                2:"Hufflepuff",
                3:"Gryffindor",
                4:"Slytherin",
              'r':"Ravenclaw",
              'h':"Hufflepuff",
              'g':"Gryffindor",
              's':"Slytherin",
      "Ravenclaw":1,
     "Hufflepuff":2,
     "Gryffindor":3,
      "Slytherin":4,
         }

menu = {
         "Beefy Jack Burger"    : 6.90,
         "Chargrill Chicken"    : 8.90,
         "Crispy Fried Fish"    : 9.50,
         "Plain Water"          : 0.30,
         "Pepsi"                : 1.80,
         "7-Up"                 : 1.80,
         "Mug Rootbeer"         : 1.80,
         "Mug Grape"            : 1.80,
         "Hot Tea"              : 1.50,
         "Specialty Tea"        : 1.80,
         "Espresso"             : 1.50,
         "Freshly Brewed Coffee": 1.90,
       }

menu_count = [
         "Beefy Jack Burger",
         "Chargrill Chicken",
         "Crispy Fried Fish",
         "Plain Water"      ,
         "Pepsi"            ,
         "7-Up"             ,
         "Mug Rootbeer"     ,
         "Mug Grape"        ,
         "Hot Tea"          ,
         "Specialty Tea"    ,
         "Espresso"         ,
         "Freshly Brewed Coffee",
         "Coleslaw",
         "French Fries",
         "Potato Salad",
         "Pasta Salad",
         "Mac & Cheese",
         "House Salad",
         "Mashed Potato",
         "Baked Potato",
         "Onion Rings",
         "BBQ Beans",
         "Potato Wedges",
         "Corn on the Cob",
         "Tasty Rice",
]

ministry = ['tankokhua','sereneho','lampuisuan','limbeebee','ckoh','keshav']
helpers = ['enghai', 'angus']
team_leaders = ['huifen', 'yanghao', 'rsumaputra', 'joannlee', 'teckyeelim', 'ysgoh', 'yping', 'evanter', 'louisegohth', 'andychowlt', 'bennyong', 'kianchai', 'amyloi', 'tankkiang', 'huaiseng', 'yeewan']
vegetarian = ['tanchunseng', 'balakumaranr', 'xiaowen', 'ranganathan', 'anila', 'liyan']
halal   = ['dhika', 'irfanabid', 'ahmadmazhar', 'rachmatw']
jinja_environment = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

def get_users():
    json_data = open("groups.json").read()
    data = json.loads(json_data)
    users = []
    for house in data:
        for year in data[house]:
            users.extend(data[house][year])
    return users

def get_house_and_year(user):
    json_data = open("groups.json").read()
    data = json.loads(json_data)
    for house in data:
        for year in data[house]:
            if user in data[house][year]:
               return  (house, int(year))

def send_mail(user, body):
    try:
       switch = Switch.gql('WHERE func = :1', "email").get()
       status = switch.status
    except:
       status = 0
    if status==0:
       logging.info("Email functionality is switched off")
       return
    email = mail.EmailMessage()
    email.sender  = "Singapore-OCT-TeamBuilding@wizardry-tournament.appspotmail.com"
    if status==3:
       email.to      = "%s@micron.com" % user
    elif status==2:
       email.to      = "tankokhua@micron.com"
    elif status==1:
       email.to      = "tankokhua@outlook.com"
    else:
       logging.info("Unknown value for email status.")
       return
    email.subject = "Wizardry Tournament 2014 - Lunch Order Confirmation"
    email.body    = ""
    email.html   = body + "<br><br>Regards<br>OCT Team Building Committee"
    if email.is_initialized():
       logging.info("Mail is initialized.")
       email.send()
    else:
       logging.info("Mail not initialized")

def set_switch(func, status):
    switch = Switch.gql('WHERE func = :1', func).get()
    if switch:
       switch.status = status
    else:
       switch = Switch(func=func, status=status)
    switch.put()
    logging.info("%s status set to %d\n" % (func, status))
    self.response.out.write("%s set to %d\n" % (func, status))

class SwitchHandler(webapp2.RequestHandler):
    def get(self):
        func   = self.request.get("func")
        status = int(self.request.get("status"))
        set_switch(func, status)

class PhotosHandler(webapp2.RequestHandler):

    def get(self):
        slides = range(1, 225)
        for x in range(152, 157):
            slides.remove(x)
        random.shuffle(slides)
        template_values = {'slides':slides }
        template = jinja_environment.get_template('templates/photos.htm')
        self.response.out.write(template.render(template_values))

class MemoryHandler(webapp2.RequestHandler):

    def get(self):
        slides = range(1, 36)
        random.shuffle(slides)
        template_values = {'slides':slides }
        template = jinja_environment.get_template('templates/memory.htm')
        self.response.out.write(template.render(template_values))

class RulesHandler(webapp2.RequestHandler):

    def get(self):
        template_values = { }
        template = jinja_environment.get_template('templates/rules.htm')
        self.response.out.write(template.render(template_values))

class GroupHandler(webapp2.RequestHandler):
    def get(self):
        output = ["""<html><head><style> b#sly {font-size:18; background-color:grey; color:green} b#gry {font-size:18; background-color:grey;color:red} b#huf {font-size:18; background-color:grey;color:yellow} b#rav {font-size:18; background-color:grey; color:blue} b#leader {color:blue;} b#halal { background-color:yellow; color:black} </style></head><pre>\n"""]
        json_data = open("groups.json").read()
        data = json.loads(json_data)
        for house in sorted(data.keys()):
            output.append("<b id='%s'>%s</b>:" % (house.lower()[:3], house))
            for year in sorted(data[house].keys()):
                group = map(lambda x:str(x), data[house][year])
                new_group = []
                for user in group:
                    if user in team_leaders:
                       new_group.append("<b id='leader'>%s</b>" % user)
                   #elif user in halal:
                   #   new_group.append("<b id='halal'>%s</b>" % user)
                    else:
                       new_group.append(user)
                output.append("Year %d: %s" % (int(year), ", ".join(new_group)))
            output.append("\n")
        output.append("<b>LEGEND:</b>")
        output.append("<b id='leader'>Team Leader</b>")
        output.append("</pre></html>")
        self.response.out.write("\n".join(output))
        

class OrderReportHandler(webapp2.RequestHandler):

    def get(self):
       #current_user = users.get_current_user()
       #if current_user.email() in ('cghtkh@gmail.com'):
       #   orders = Order.all()
       #   output = ["user,main_course,sides,drink"]
       #   for order in orders:
       #       output.append("%s,%s,%s,%s" % (order.user, order.main_course, order.sides, order.drink))
       #   self.response.out.write("<br>".join(output))
       #else:
       #   self.response.out.write("Invalid User.")

       count = {}
       for item in menu_count:
           count.setdefault(item, 0)
      #orders = Order.all()
       queue  = db.Query(Order).order('date');
       orders = queue.fetch(limit=150)
       #drink,main_course,attempts,user,key,date,sides
       data = {}
       responded = []
       for order in orders:
           info = {}
           user        = order.user
           main_course = order.main_course
           sides       = order.sides
           drink       = order.drink

           responded.append(user)
           result = get_house_and_year(user)
           if result:
              house, year = result
           else:
              house = 'Committee'
              year = 0
           info.setdefault(user, {}).setdefault('main_course', main_course)
           info.setdefault(user, {}).setdefault('sides', sides)
           info.setdefault(user, {}).setdefault('drink', drink)
           data.setdefault(house, {}).setdefault(year, []).append(info)
           count[main_course] +=1
           count[drink]       +=1
           if len(sides):
              for side in sides.split('|'):
                  count[side]    +=1

       total = 0
       cnt = 0
       output = ["""<html><head><style> b#cost {color:green;} b#y1 {color:red;} b#y2 {color:blue;} b#y3 {color:green;} #sly {color:green;} #gry {color:red;} #huf {color:yellow} #rav {color:blue} </style></head><pre>"""]

       table = 1
       if table:
          output.append("<table border=1>")
          output.append("<tr><th>No.</th><th>House</th><th>Year</th><th>User</th><th>Main Course</th><th>Sides</th><th>Drink</th><th>Cost</th></tr>")

       for house in sorted(data.keys()):
           for year in sorted(data[house].keys()):
               for info in data[house][year]:
                   user = info.keys()[0]
                   main_course = info[user]["main_course"]
                   sides       = info[user]["sides"]
                   drink       = info[user]["drink"]
                   cost = menu[main_course] + menu[drink]
                   if table:
                      row = '<tr><td>%d</td>' % (cnt+1)
                      row += '<td><i id="%s">%s</i></td>' % (house[:3].lower(), house)
                      if year!=0:
                         row += '<td><b id="y%d">Year %d</b></td>' % (year, year)
                      else:
                         row += '<td><b>-</b></td>'
                      row += '<td>%s</td>' % user
                      row += '<td>%s</td>' % main_course
                      row += '<td>%s</td>' % ", ".join(sides.split('|'))
                      row += '<td>%s</td>' % drink
                      row += '<td>%.2f</td></td></tr>' % (cost)
                      output.append(row)
                   else:
                      output.append('<b>%s</b>:' % user)
                      output.append("\tMain Course: %s" % main_course)
                      if len(sides):
                         output.append("\tSides      : %s" % ", ".join(sides.split('|')))
                      output.append("\tDrink      : %s" % drink)
                      output.append("\tCost       : <b id='cost'>%.2f</b>\n" % cost)
                  
                   total += cost
                   cnt += 1

       output.append("</table>")

       output.append("\n<b>Total</b>: %.2f [%.2f]\n" % (total, total/cnt))
       output.append("<hr>Total orders by item:")
       for item in menu_count:
           output.append("\t%-25s: %d" % (item, count[item]))

       # People not responded
       all_users = set(get_users()+ministry+helpers)
       not_responded = all_users.difference(set(responded)).difference(set(vegetarian)).difference(set(halal))
       output.append("<hr>Not responded [%d]:" % len(not_responded))
       for user in not_responded:
           output.append("\t%s" % user)
       output.append("</pre></html>")
       self.response.out.write("\n".join(output))

class FeastHandler(webapp2.RequestHandler):

    def get(self):
        template_values = { }
        template = jinja_environment.get_template('templates/feast.htm')
        self.response.out.write(template.render(template_values))

    def post(self):
        username    = self.request.get("username").strip().lower()
        main_course = self.request.get("main_course")
        drink       = self.request.get("drink")
        if re.search("burger", main_course.lower()):
           sides = ""
        else:
           sides = self.request.get("sides").replace(',','|')

        _order = Order.gql('WHERE user = :1', username).get()

        usernames = get_users()

        with open('oct.csv') as csvfile:
             reader = csv.reader(csvfile)
             cnt = 0
             lastname = ""
             for row in reader:
                 if cnt>0:
                    user = row[0].replace('@micron.com','')
                    if user==username:
                       lastname = row[1].split(',')[1].strip()
                       break
                 cnt += 1
        if lastname=="":
           lastname = username

        if username in usernames+ministry+helpers and username not in vegetarian+halal:
           update = False
           if not _order: 
              _order = Order(user=username, main_course=main_course, sides=sides, drink=drink, attempts=1)
              update = True
           else: 
              if username in ministry+helpers:
                 _order.main_course = main_course
                 _order.drink = drink
                 _order.sides = sides
                 _order.attempts += 1
                 _order.date = datetime.datetime.now()
                 update = True
              else:
                 order = "Sorry, you have already submitted your order previously.<br>Please contact the Team Building Committee if you want to make changes."
           if update:
              _order.put()
              if sides=="":
                 order = "Hi %s,<br>Your order is submitted successfully.<br>You have selected %s and %s." % (lastname, main_course, drink)
              else:
                 order = "Hi %s,<br>Your order is submitted successfully.<br>You have selected %s [%s] and %s." % (lastname, main_course, sides.replace('|',', '),  drink)
              send_mail(username, order)
        elif username in vegetarian:
           order = "Hi %s, you have selected Vegetarian for your meal preference." % (lastname)
        elif username in halal:
           order = "Hi %s, you have selected Halal for your meal preference." % (lastname)
        else:
           order = "Sorry! You are not registered for this event.\nPlease approach OCT Team Building Committee if this is a mistake."
        template_values = { "order":order }
        template = jinja_environment.get_template('templates/order.htm')
        self.response.out.write(template.render(template_values))


class HouseHandler(webapp2.RequestHandler):
    def post(self):
        fulllist = map(lambda x:x.lower().strip(), open("oct2.txt").readlines())
        username   = self.request.get("username").strip().lower()
        answers = "Invalid Username."

        with open('oct.csv') as csvfile:
            reader = csv.reader(csvfile)
            cnt = 0
            lastnames = {}
            for row in reader:
                if cnt>0:
                   try:
                      lastnames.setdefault(row[0].replace('@micron.com',''), row[1].split(',')[1])
                   except:
                      logging.info("Error row %s" % row)
                      lastnames.setdefault(row[0].replace('@micron.com',''), row[1].split(',')[1])
                cnt += 1

        not_going = []
        not_going = [ x for x in fulllist if x not in get_users() ]

        ip = self.request.remote_addr
        update = True


        ui = User.gql('WHERE user = :1', username).get()
        result = get_house_and_year(username)
        if result:
           house, year = result
           if not ui:
              ui =  User(user=username, house=house, year=year, attempts=1)
           else:
              house = ui.house
              year  = ui.year
              ui.attempts+=1
        else:
           update = False
          
        if update:
           ui.date = datetime.datetime.now()
           ui.put()
           if username in team_leaders:
              answers = "Hi <b id='lname'>%s</b>,<br>You are the <b id='digit'>Year %d</b> Team Leader of <b id='desc'>%s</b>.<br><img src='/static/images/h%d.jpg' id='batch'>" % (lastnames[username], year, house, HOUSES[house])
           else:
              answers = "Hi <b id='lname'>%s</b>,<br>You are from <b id='digit'>Year %d</b> of <b id='desc'>%s</b>.<br><img src='/static/images/h%d.jpg' id='batch'>" % (lastnames[username], year, house, HOUSES[house])
           logging.info("user [%s] ip [%s]" % (ui.user, ip))

        if username in ministry+helpers:
           answers = "Hi <b id='lname'>%s</b>,<br>you are from <b id='desc'>Ministry of Magic</b>.<br><img src='/static/images/mom.png' id='batch'>" % (lastnames[username])
        elif username in not_going and not ui:
           house = random.randint(1,4)
           year  = random.randint(1,4)
           answers = "Hi <b id='lname'>%s</b>,<br>you are from <b id='digit'>Year %d</b> of <b id='desc'>%s</b>.<br><img src='/static/images/h%d.jpg' id='batch'>" % (lastnames[username], year, HOUSES[house], house)

        time.sleep(2)

        template_values = {
                           "answers":answers
                          }
        template = jinja_environment.get_template('templates/answers.htm')
        self.response.out.write(template.render(template_values))

class SMSHandler(webapp2.RequestHandler):

  def get(self):
    msg = self.request.get("message").lower()
    findhouse = False
    doquiz = False
    if re.search(r'^house', msg):
       username = msg.split()[1]
       logging.info("SMS house %s [%s]" % (username,self.request.get("caller")))
       findhouse = True
    elif re.search(r'^quiz(\d)\s+([a-z]+)\s+(.*)', msg):
       tokens = re.search(r'^quiz(\d)\s+([a-z]+)\s+(.*)', msg).groups()
       quiz = int(tokens[0])
       username = tokens[1]
       answer = tokens[2]
       q = Quiz(quiz= quiz, user=username, answer=answer)
       q.put()
       doquiz = True
    elif re.search(r'whatsapp\s+([sghr])\s*([1-4])', msg):
         tokens = re.search(r'whatsapp\s+([sghr])\s*([1-4])', msg).groups()
         house = tokens[0]
         year  = int(tokens[1])
         caller = self.request.get("caller")
         wa = Whatsapp(user=caller, house=house, year=year)
         wa.put()
         self.response.out.write("Hi Year %ds of %s, this number %s will be added to Photo Challenge Whatapps group." % (year, HOUSES[house], caller))
         return
    elif re.search(r'switch\s+([a-z]+)\s+(\d)', msg):
         func   = msg.split()[1]
         status =  int(msg.split()[2])
         set_switch(func, status)
         return
    elif re.search(r'order\s+([a-z]+)', msg):
         username = msg.split()[1].lower().strip()
         _order = Order.gql('WHERE user = :1', username).get()
         if _order:
            db.delete([_order])
            logging.info("%s is deleted from Order." % username)
            self.response.out.write("%s is deleted from Order." % username)
         return
    else:
       self.response.out.write("0")
       return

    with open('oct.csv') as csvfile:
         reader = csv.reader(csvfile)
         cnt = 0
         lastname = ""
         for row in reader:
             if cnt>0:
                user = row[0].replace('@micron.com','')
                if user==username:
                   lastname = row[1].split(',')[1].strip()
                   break
             cnt += 1

    if findhouse:
       found = get_house_and_year(username)
       if found:
          house, year = found
          logging.info("SMS house %s year %d" % (house, year))

       if username in ministry+helpers:
          self.response.out.write("Hi %s, you are from Ministry of Magic." % (lastname))
       elif found:
          if username in team_leaders:
             response = "Hi %s, you are the Year %d Team Leader of %s." % (lastname, year, house)
            #self.response.out.write("Hi %s, you are the Year %d Team Leader of %s." % (lastname, year, house))
          else:
             response = "Hi %s, you are from Year %d of %s." % (lastname, year, house)
            #self.response.out.write("Hi %s, you are from Year %d of %s." % (lastname, year, house))
          logging.info("SMS %s" % response)
          self.response.out.write(response)
       else:
          self.response.out.write("0")
    elif doquiz:
       self.response.out.write("Hi %s, thanks for your participation." % lastname)
    else:
       self.response.out.write("0")

class MainHandler(webapp2.RequestHandler):
    def get(self):
        template_values = {
                             "username":"",
                            #"hg_image":"hg%d.png" % (1,2,2)[random.randint(0,2)],
                          }
        template = jinja_environment.get_template('templates/index.htm')
        self.response.out.write(template.render(template_values))

app = webapp2.WSGIApplication([
                                ('/getHouse', HouseHandler),
                                ('/sms', SMSHandler),
                                ('/feast', FeastHandler),
                                ('/rules', RulesHandler),
                                ('/photos', PhotosHandler),
                                ('/getOrder', FeastHandler),
                                ('/orderReport', OrderReportHandler),
                                ('/groupReport', GroupHandler),
                                ('/setSwitch', SwitchHandler),
                                ('/sorting', MainHandler),
                                ('/memory', MemoryHandler),
                                ('/.*', PhotosHandler),
                              ], debug=True)
