import os

from google.appengine.ext import webapp
from google.appengine.ext.webapp import util

from django.utils import simplejson

from models import Vote, doVote, Stat, HourNumberCount

from datetime import datetime
import time

from handler_utils import renderToResponse

class MainHandler(webapp.RequestHandler):
    def get(self):
        renderToResponse(self, 'index.html.django')

    def post(self):
        number          = self.request.get("number", None)
        method          = self.request.get("method", None)
        pick            = self.request.get("pick", None)
        submit          = self.request.get("submit", None)
        showed_random   = self.request.get("random", None)
        
        ip = self.request.remote_addr
        
        result = { "status": "failed" }
        if doVote(number, method, pick, submit, showed_random, ip):
            result = { "status": "success" }

        self.response.headers["Content-Type"] = "application/javascript"
        self.response.out.write(simplejson.dumps(result))

class ResultHandler(webapp.RequestHandler):
    def get(self):
        renderToResponse(self, 'results.html.django')

class RedirectResultHandler(webapp.RequestHandler):
    def get(self):
        self.redirect('/results/')

def main():
    application = webapp.WSGIApplication([
                                ('/',           MainHandler),
                                ('/results',    RedirectResultHandler),
                                ('/results/',   ResultHandler),
                                ],debug=False)
    util.run_wsgi_app(application)

if __name__ == '__main__':
    main()