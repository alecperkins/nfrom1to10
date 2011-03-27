from google.appengine.ext import webapp
from google.appengine.ext.webapp import util

from django.utils import simplejson

from models import Vote, incrementVote


class MainHandler(webapp.RequestHandler):
    def get(self):
        page = open("index.html")
        self.response.out.write(page.read())
        page.close()

    def post(self):
        number = self.request.get("number", None)
        method = self.request.get("method", None)
        result = { "status": "failed" }
        if number and method:
            try:
                number = int(number)
            except:
                pass
            else:
                options = ("input","slider","select","radio")
                if number in range(1,10) and method in options:
                    incrementVote(number, method)
                    result = { "status": "success" }

        self.response.headers["Content-Type"] = "application/javascript"
        self.response.out.write(simplejson.dumps(result))



def main():
    application = webapp.WSGIApplication([('/', MainHandler)],
                                         debug=True)
    util.run_wsgi_app(application)

if __name__ == '__main__':
    main()
