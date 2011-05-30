from google.appengine.ext import db

class Vote(db.Model):
    date            = db.DateTimeProperty(auto_now_add=True)
    number          = db.IntegerProperty()          # number chosen, of {1,2,3...10}
    method          = db.StringProperty()           # "input", "select", "slider", "radio"
    pick            = db.IntegerProperty()          # num ms to first choice of num
    submit          = db.IntegerProperty()          # num ms to submit of choice
    showed_random   = db.BooleanProperty()          # True if "random" was said, False if not
    ip              = db.StringProperty()           # ip address of voter
    range           = db.StringProperty()           # number range presented: eg 1-10, 0-9

class Followup(db.Model):
    vote    = db.ReferenceProperty(Vote)
    how     = db.StringProperty()
    # {
    #     '1'         : 'Thought of a number and chose it',
    #     '2'         : 'Used a die, random number generator, or other random process',
    #     '3'         : 'Looked around me for a number',
    #     '4-input'   : 'Mashed the keyboard',
    #     '4-radio'   : 'Moved the mouse back-and-forth quickly then clicked',
    #     '4-select'  : 'Moved the mouse back-and-forth quickly then clicked',
    #     '4-slider'  : 'Moved the slider back-and-forth quickly then released',
    #     ''          : 'Other'
    # }
    why     = db.StringProperty()
    # {
    #         '1'         : 'Yes, it is personally significant'
    #         '2'         : 'Yes, it is culturally significant'
    #         '3'         : 'No, it is arbitrary'
    # }


OPTIONS = ("input","radio","select","slider")
def doVote(number, method, pick, submit, showed_random, ip=None):
    if number and method and pick and submit and showed_random:
        try:
            number = int(number)
            pick = int(pick)
            submit = int(submit)
        except ValueError:
            pass
        else:
            if method in OPTIONS:
                if showed_random == "true":
                    showed_random = True
                elif showed_random == "false":
                    showed_random = False
                vote = Vote()
                vote.number         = number
                vote.method         = method
                vote.pick           = pick
                vote.submit         = submit
                vote.showed_random  = showed_random
                if ip:
                    vote.ip = ip
                else:
                    vote.ip = ""
                vote.put()
                return vote
        return None


def doFollowup(vote_id, how, why):
    if vote_id and how is not None and why is not None:
        try:
            vote = db.get(db.Key(vote_id))
        except:
            pass
        else:
            followup = Followup()
            followup.vote   = vote
            followup.how    = how
            followup.why    = why
            followup.put()
            return followup
    return None        


class VoteStat(db.Model):
    method          = db.StringProperty()
    number          = db.IntegerProperty()
    count           = db.IntegerProperty()
    generated       = db.DateTimeProperty()
    showed_random   = db.BooleanProperty()

class HowStat(db.Model):
    how             = db.StringProperty()
    number          = db.IntegerProperty()
    count           = db.IntegerProperty()
    generated       = db.DateTimeProperty()

class WhyStat(db.Model):
    why             = db.StringProperty()
    number          = db.IntegerProperty()
    count           = db.IntegerProperty()
    generated       = db.DateTimeProperty()
