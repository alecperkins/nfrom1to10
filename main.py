from google.appengine.ext import webapp
from google.appengine.ext.webapp import util

from django.utils import simplejson

from models import Vote, doVote


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
        result = { "status": "failed" }
        if doVote(number, method, pick, submit, showed_random):
            result = { "status": "success" }

        self.response.headers["Content-Type"] = "application/javascript"
        self.response.out.write(simplejson.dumps(result))



def main():
    application = webapp.WSGIApplication([('/', MainHandler)],
                                         debug=False)
    util.run_wsgi_app(application)

if __name__ == '__main__':
    main()
