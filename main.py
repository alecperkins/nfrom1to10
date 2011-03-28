from google.appengine.ext import webapp
from google.appengine.ext.webapp import util

from django.utils import simplejson

from models import Vote, doVote, StatMethod


class MainHandler(webapp.RequestHandler):
    def get(self):
        page = open("index.html")
        self.response.out.write(page.read())
        page.close()

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
        page = open("results.html")
        self.response.out.write(page.read())
        page.close()


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
        for m in result:
            result[m]["data"] = [0,0,0,0,0,0,0,0,0,0]

        stats = StatMethod.all()
        for stat in stats:
            result[stat.method]["data"][stat.number-1] = stat.count
            result[stat.method]["generated"] = "%sZ" % stat.generated.isoformat()

        self.response.headers["Content-Type"] = "application/javascript"
        self.response.out.write(simplejson.dumps(result))

def main():
    application = webapp.WSGIApplication([
                                ('/', MainHandler),
                                ('/results', ResultHandler),
                                ('/results/', ResultHandler),
                                ('/data/', DataHandler),
                                        ],debug=False)
    util.run_wsgi_app(application)

if __name__ == '__main__':
    main()
