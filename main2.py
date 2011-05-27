import os

from google.appengine.api import memcache
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util

from django.utils import simplejson

from models import Vote, doVote, Stat, HourNumberCount

from datetime import datetime
import time
V = os.environ['CURRENT_VERSION_ID']

def getCachedPage(page):
    key = "%s-%s" % (V, page)
    cached_data = memcache.get(key)
    if cached_data is not None:
        p = cached_data
    else:
        f = open(page)
        p = f.read()
        memcache.set(key,p,1800)
        f.close()
    return p

class MainHandler(webapp.RequestHandler):
    def get(self):
        page = getCachedPage("index.html")
        self.response.out.write(page)

    def post(self):
        number = self.request.get("number", None)
        method = self.request.get("method", None)
        pick = self.request.get("pick", None)
        submit = self.request.get("submit", None)
        showed_random = self.request.get("random", None)
        
        ip = self.request.remote_addr
        
        result = { "status": "failed" }
        if doVote(number, method, pick, submit, showed_random, ip):
            result = { "status": "success" }

        self.response.headers["Content-Type"] = "application/javascript"
        self.response.out.write(simplejson.dumps(result))


class ResultHandler(webapp.RequestHandler):
    def get(self):
        page = getCachedPage("results.html")
        self.response.out.write(page)


class DataHandler(webapp.RequestHandler):
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


        cached_breakdown = memcache.get("%s-results-breakdown" % V)
        if cached_breakdown is not None:
            result["breakdown"] = cached_breakdown
        else:
            for m in result["breakdown"]:
                result["breakdown"][m]["random_specified"] = { "data": [0,0,0,0,0,0,0,0,0,0] }
                result["breakdown"][m]["random_not_specified"] = { "data": [0,0,0,0,0,0,0,0,0,0] }

            stats = Stat.all().filter("showed_random !=", None)
            for stat in stats:
                if stat.showed_random:
                    random_text = "random_specified"
                else:
                    random_text = "random_not_specified"
                result["breakdown"][stat.method][random_text]["data"][stat.number-1] = stat.count
                result["breakdown"][stat.method][random_text]["generated"] = "%s UTC" % stat.generated.strftime("%Y-%m-%d %H:%M")
            
            memcache.add("%s-results-breakdown" % V, result["breakdown"], 600)


        cached_overtime = memcache.get("%s-results-overtime" % V)
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
            memcache.add("%s-results-overtime" % V, result["overtime"], 600)
            
        self.response.headers["Content-Type"] = "application/javascript"
        self.response.out.write(simplejson.dumps(result))

class RedirectResultHandler(webapp.RequestHandler):
    def get(self):
        self.redirect('/results/')

def main():
    application = webapp.WSGIApplication([
                                ('/',           MainHandler),
                                ('/results',    RedirectResultHandler),
                                ('/results/',   ResultHandler),
                                ('/data/',      DataHandler),
                                ],debug=False)
    util.run_wsgi_app(application)

if __name__ == '__main__':
    main()
