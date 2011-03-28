from google.appengine.api import memcache
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util

from django.utils import simplejson

from models import Vote, doVote, Stat


def getCachedPage(key):
    cached_data = memcache.get(key)
    if cached_data is not None:
        page = cached_data
    else:
        f = open(key)
        page = f.read()
        memcache.set(key,page,1800)
        f.close()
    return page

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
            "input":{},
            "select":{},
            "slider":{},
            "radio":{},
        }
        cached_data = memcache.get("results-data")
        if cached_data is not None:
            result = cached_data
        else:
            for m in result:
                result[m]["random_specified"] = { "data": [0,0,0,0,0,0,0,0,0,0] }
                result[m]["random_not_specified"] = { "data": [0,0,0,0,0,0,0,0,0,0] }
        
            stats = Stat.all().filter("showed_random !=", None)
            for stat in stats:
                if stat.showed_random:
                    random_text = "random_specified"
                else:
                    random_text = "random_not_specified"
                result[stat.method][random_text]["data"][stat.number-1] = stat.count
                result[stat.method][random_text]["generated"] = "%s UTC" % stat.generated.strftime("%Y-%m-%d %H:%M")
            memcache.add("results-data", result, 1800)
        self.response.headers["Content-Type"] = "application/javascript"
        self.response.out.write(simplejson.dumps(result))

class RedirectResultHandler(webapp.RequestHandler):
    def get(self):
        self.redirect('/results/')

def main():
    application = webapp.WSGIApplication([
                                ('/', MainHandler),
                                ('/results', RedirectResultHandler),
                                ('/results/', ResultHandler),
                                ('/data/', DataHandler),
                                        ],debug=False)
    util.run_wsgi_app(application)

if __name__ == '__main__':
    main()
