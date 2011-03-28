from google.appengine.ext import db
from google.appengine.api.labs import taskqueue

from models import Vote, StatMethod
OPTIONS = ("input","radio","select","slider")

from google.appengine.ext import webapp
from google.appengine.ext.webapp import util

from datetime import datetime

class TaskHandler(webapp.RequestHandler):
    def get(self):
        for method in OPTIONS:
            for number in range(1,11):
                if number and method:
                    number = int(number)
                    params = {
                        "number": number,
                        "method": method,
                        "refresh": True,
                    }
                    taskqueue.add(url="/tasks", params=params)
                    self.response.out.write("%s-%s<br>x" % (number, method))
                else:
                    self.response.out.write("no params")

    def post(self):
        method = self.request.get("method", None)
        number = self.request.get("number", None)
        cursor = self.request.get("cursor", None)
        refresh = self.request.get("refresh", None)
        
        try:
            number = int(number)
        except:
            number = None
        
        if method and number and method in OPTIONS:
            key_name = "%s-%s" % (method, number)
            stat = StatMethod.get_or_insert(key_name)
            import logging
            logging.info(method)
            logging.info(number)
            
            q = Vote.all()
            q.filter("method =", method)
            q.filter("number =", number)

            if cursor:
                q.with_cursor(cursor)
            count = q.count()
            next_cursor = q.cursor() if count == 1000 else None
            if refresh or not stat.count:
                stat.count = 0
            stat.count = stat.count + count
            stat.method = method
            stat.number = number
            stat.generated = datetime.now()
            stat.put()
            logging.error(stat.method)
            logging.error(stat.number)
            logging.error(stat.count)
            if next_cursor:
                params = {
                    "number": number,
                    "method": method,
                    "cursor": next_cursor,
                }
                taskqueue.add(url="/tasks", params=params)


def main():
    application = webapp.WSGIApplication([
                                ('/tasks', TaskHandler),
                                        ],debug=True)
    util.run_wsgi_app(application)

if __name__ == '__main__':
    main()
