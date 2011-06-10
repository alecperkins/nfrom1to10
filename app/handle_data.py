from datetime import datetime, timedelta
import time

from django.utils import simplejson

from google.appengine.api import memcache
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util

from models import VoteStat, HourNumberCount, Vote
from handler_utils import renderToResponse, jsonResponse, RedirectSlashHandler
import settings

OPTIONS = ("input","radio","select","slider")



def assembleData(json=False):
    if settings.CACHE:
        ui_breakdown    = memcache.get("%s-results-ui_breakdown" % settings.VERSION)
        overtime        = memcache.get("%s-results-overtime" % settings.VERSION)
    else:
        ui_breakdown    = None
        overtime        = None

    if ui_breakdown is None:
        ui_breakdown = {
            "input"     :{},
            "select"    :{},
            "slider"    :{},
            "radio"     :{},
        }

        for m in ui_breakdown:
            ui_breakdown[m]["random_specified"] = { "data": [0,0,0,0,0,0,0,0,0,0] }
            ui_breakdown[m]["random_not_specified"] = { "data": [0,0,0,0,0,0,0,0,0,0] }

        stats = VoteStat.all().filter("showed_random !=", None)
        for stat in stats:
            if stat.showed_random:
                random_text = "random_specified"
            else:
                random_text = "random_not_specified"
            ui_breakdown[stat.method][random_text]["data"][stat.number-1] = stat.count
            ui_breakdown[stat.method][random_text]["generated"] = "%s UTC" % stat.generated.strftime("%Y-%m-%d %H:%M")

    if overtime is None:
        overtime = [ [] for n in range(0,10) ]

        hend = datetime(2011,3,28,17,11,56)

        hourcount = HourNumberCount.all().filter("hour_end <", hend)

        for stat in hourcount:
            t = time.mktime(stat.hour_start.timetuple())
            c = stat.count
            overtime[stat.number-1].append( (t,c) )

    if settings.CACHE:
        memcache.add("%s-results-ui_breakdown" % settings.VERSION, ui_breakdown, settings.CACHE_LIFE)
        memcache.add("%s-results-overtime" % settings.VERSION, overtime, settings.CACHE_LIFE)    

    result = {
        "ui_breakdown"  : ui_breakdown,
        "over_time"     : overtime,
    }
    if json:
        return simplejson.dumps(result)
    else:
        return result



class OverviewHandler(webapp.RequestHandler):
    def get(self):
        jsonResponse(self, assembleData())



class VotesHandler(webapp.RequestHandler):
    def get(self):

        skeleton_key = self.request.get("skeleton", None)

        if settings.THROTTLE_API and skeleton_key != settings.SKELETON_KEY:
            ip = str(self.request.remote_addr)
            throttle = memcache.get(ip)
            if throttle:
                throttle = throttle - datetime.now()
                jsonResponse(self, {
                    'status': 'throttled',
                    'remaining': throttle.seconds
                })
                return
            else:
                throttle = datetime.now() + timedelta(seconds=settings.THROTTLE_LIFE)
                memcache.set(ip, throttle, settings.THROTTLE_LIFE)

        method          = self.request.get("method", None)
        number          = self.request.get("number", None)
        random_text     = self.request.get("random_text", None)

        cursor = self.request.get("cursor", None)

        showed_random = None
        if random_text:
            if random_text == 'visible':
                showed_random = True
            elif random_text == 'hidden':
                showed_random = False
            else:
                self.error(400)
                return

        q = Vote.all()

        if method:
            if method in OPTIONS:
                q.filter("method =", method)
            else:
                self.error(400)
                return
        
        if number is not None:
            try:
                number = int(number)
            except:
                self.error(400)
                return
            else:
                q.filter("number =", number)
        
        if showed_random is not None:
            q.filter("showed_random =", showed_random)

        if cursor:
            try:
                q.with_cursor(cursor)
            except:
                self.error(400)
                return
        
        data = None
        cached_data = None
        LIMIT = 1000

        key = "%s-%s-%s-%s-%s" % (settings.VERSION, method, number, random_text, cursor)

        if settings.CACHE:
            cached_data = memcache.get(key)
        
        if not cached_data:
            data = q.fetch(LIMIT)
            next_cursor = q.cursor() if len(data) == LIMIT else None

            result = {
                "objects"       : [vote.toJSON(full=(skeleton_key is not None)) for vote in data],
                "next_cursor"   : next_cursor
            }
            if settings.CACHE and not skeleton_key:
                memcache.set(key, result, settings.CACHE_LIFE)
        else:
            result = cached_data

        jsonResponse(self, result)



def main():
    application = webapp.WSGIApplication([
                                ('/data/overview/', OverviewHandler),
                                ('/data/votes/',    VotesHandler),
                                ('/data/overview',  RedirectSlashHandler),
                                ('/data/votes',     RedirectSlashHandler),
                                ],debug=settings.DEBUG)
    util.run_wsgi_app(application)

if __name__ == '__main__':
    main()