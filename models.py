from google.appengine.ext import db

class Vote(db.Model):
    date = db.DateTimeProperty(auto_now_add=True)
    number = db.IntegerProperty()           # number chosen, of {1,2,3...10}
    method = db.StringProperty()            # "input", "select", "slider", "radio"
    pick = db.IntegerProperty()             # num ms to first choice of num
    submit = db.IntegerProperty()           # num ms to submit of choice
    showed_random = db.BooleanProperty()    # True if "random" was said, False if not
    ip = db.StringProperty()                # ip address of voter

OPTIONS = ("input","radio","select","slider")
def doVote(number, method, pick, submit, showed_random, ip=None):
    if number and method and pick and submit and showed_random:
        try:
            number = int(number)
            pick = int(pick)
            submit = int(submit)
        except:
            pass
        else:
            if method in OPTIONS:
                if showed_random == "true":
                    showed_random = True
                elif showed_random == "false":
                    showed_random = False
                vote = Vote()
                vote.number = number
                vote.method = method
                vote.pick = pick
                vote.submit = submit
                vote.showed_random = showed_random
                if ip:
                    vote.ip = ip
                else:
                    vote.ip = ""
                vote.put()
                return vote
        return None


class StatMethod(db.Model):
    method = db.StringProperty()
    number = db.IntegerProperty()
    count = db.IntegerProperty()
    generated = db.DateTimeProperty()

class Stat(db.Model):
    method = db.StringProperty()
    number = db.IntegerProperty()
    count = db.IntegerProperty()
    generated = db.DateTimeProperty()
    showed_random = db.BooleanProperty()
