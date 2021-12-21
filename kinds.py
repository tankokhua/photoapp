from google.appengine.ext import db
#class UserInfo(db.Model):
#      user     = db.StringProperty()
#      ip       = db.StringProperty()
#      attempts = db.IntegerProperty()
#      house    = db.IntegerProperty()
#      date     = db.DateTimeProperty(auto_now_add=True)

class User(db.Model):
      user     = db.StringProperty()
      attempts = db.IntegerProperty()
      house    = db.StringProperty()
      year     = db.IntegerProperty()
      date     = db.DateTimeProperty(auto_now_add=True)

class Quiz(db.Model):
      user     = db.StringProperty()
      quiz     = db.IntegerProperty()
      answer   = db.StringProperty()
      date     = db.DateTimeProperty(auto_now_add=True)

class Order(db.Model):
      user          = db.StringProperty()
      main_course   = db.StringProperty()
      drink         = db.StringProperty()
      sides         = db.StringProperty()
      attempts      = db.IntegerProperty()
      date          = db.DateTimeProperty(auto_now_add=True)

class Whatsapp(db.Model):
      user     = db.StringProperty()
      house    = db.StringProperty()
      year     = db.IntegerProperty()

class Switch(db.Model):
      func     = db.StringProperty()
      status   = db.IntegerProperty()
