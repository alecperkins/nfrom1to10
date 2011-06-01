# /data/overview - summary
# /data/votes?key=KEY

from datetime import datetime
import time

from google.appengine.api import memcache
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util

from models import VoteStat, HourNumberCount
from handler_utils import renderToResponse, jsonResponse
import settings

class ResultsHandler(webapp.RequestHandler):
    def get(self):
        # result = {
        #     method: [count, count, count...]
        # }
        result = {
            "breakdown": {
                "input":{},
                "select":{},
                "slider":{},
                "radio":{},
            },
            "overtime": []
        }

        if settings.CACHE:
            cached_breakdown = memcache.get("%s-results-breakdown" % settings.VERSION)
        else:
            cached_breakdown = None
        if cached_breakdown is not None:
            result["breakdown"] = cached_breakdown
        else:
            for m in result["breakdown"]:
                result["breakdown"][m]["random_specified"] = { "data": [0,0,0,0,0,0,0,0,0,0] }
                result["breakdown"][m]["random_not_specified"] = { "data": [0,0,0,0,0,0,0,0,0,0] }

            stats = VoteStat.all().filter("showed_random !=", None)
            for stat in stats:
                if stat.showed_random:
                    random_text = "random_specified"
                else:
                    random_text = "random_not_specified"
                result["breakdown"][stat.method][random_text]["data"][stat.number-1] = stat.count
                result["breakdown"][stat.method][random_text]["generated"] = "%s UTC" % stat.generated.strftime("%Y-%m-%d %H:%M")
            
            if settings.CACHE:
                memcache.add("%s-results-breakdown" % V, result["breakdown"], 600)

        if settings.CACHE:
            cached_overtime = memcache.get("%s-results-overtime" % V)
        else:
            cached_overtime = None
        if cached_overtime is not None:
            result["overtime"] = cached_overtime
        else:
            result["overtime"] = [ [] for n in range(0,10) ]
            
            hend = datetime(2011,3,28,17,11,56)
            hourcount = HourNumberCount.all().filter("hour_end <", hend)
            for stat in hourcount:
                t = time.mktime(stat.hour_start.timetuple())
                c = stat.count
                result["overtime"][stat.number-1].append( (t,c) )
            if settings.CACHE:
                memcache.add("%s-results-overtime" % settings.VERSION, result["overtime"], 600)
            
        jsonResponse(self, result)

class VotesHandler(webapp.RequestHandler):
    def get(self):
        # result = {
        #     method: [count, count, count...]
        # }
        result = {
            "breakdown": {
                "input":{},
                "select":{},
                "slider":{},
                "radio":{},
            },
            "overtime": []
        }

        if settings.CACHE:
            cached_breakdown = memcache.get("%s-results-breakdown" % settings.VERSION)
        else:
            cached_breakdown = None
        if cached_breakdown is not None:
            result["breakdown"] = cached_breakdown
        else:
            for m in result["breakdown"]:
                result["breakdown"][m]["random_specified"] = { "data": [0,0,0,0,0,0,0,0,0,0] }
                result["breakdown"][m]["random_not_specified"] = { "data": [0,0,0,0,0,0,0,0,0,0] }

            stats = VoteStat.all().filter("showed_random !=", None)
            for stat in stats:
                if stat.showed_random:
                    random_text = "random_specified"
                else:
                    random_text = "random_not_specified"
                result["breakdown"][stat.method][random_text]["data"][stat.number-1] = stat.count
                result["breakdown"][stat.method][random_text]["generated"] = "%s UTC" % stat.generated.strftime("%Y-%m-%d %H:%M")
            
            if settings.CACHE:
                memcache.add("%s-results-breakdown" % V, result["breakdown"], 600)

        if settings.CACHE:
            cached_overtime = memcache.get("%s-results-overtime" % V)
        else:
            cached_overtime = None
        if cached_overtime is not None:
            result["overtime"] = cached_overtime
        else:
            result["overtime"] = [ [] for n in range(0,10) ]
            
            hend = datetime(2011,3,28,17,11,56)
            hourcount = HourNumberCount.all().filter("hour_end <", hend)
            for stat in hourcount:
                t = time.mktime(stat.hour_start.timetuple())
                c = stat.count
                result["overtime"][stat.number-1].append( (t,c) )
            if settings.CACHE:
                memcache.add("%s-results-overtime" % settings.VERSION, result["overtime"], 600)
            
        jsonResponse(self, result)

def main():
    application = webapp.WSGIApplication([
                                ('/data/results',   ResultsHandler),
                                ('/data/votes',     VotesHandler),
                                ],debug=settings.DEBUG)
    util.run_wsgi_app(application)

if __name__ == '__main__':
    main()