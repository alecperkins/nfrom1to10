from google.appengine.ext import db

class Vote(db.Model):
    number = db.IntegerProperty()
    date = db.DateTimeProperty(auto_now_add=True)
    method = db.StringProperty() # "input", "select", "slider", "radio"


def incrementVote(number, method):
    pass