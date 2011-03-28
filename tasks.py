from google.appengine.ext import db
from google.appengine.api.labs import taskqueue

from models import Vote, Stat
OPTIONS = ("input","radio","select","slider")

from google.appengine.ext import webapp
from google.appengine.ext.webapp import util

from datetime import datetime

class TaskHandler(webapp.RequestHandler):
    def get(self):
        self.response.out.write("%s<br><br>" % datetime.now())
        for method in OPTIONS:
            for number in range(1,11):
                for random_text in ["random",""]:
                    number = int(number)
                    params = {
                        "number": number,
                        "method": method,
                        "refresh": True,
                        "random_text": random_text,
                    }
                    taskqueue.add(url="/tasks", params=params)
                    self.response.out.write("%s-%s-%s<br>" % (number, method, random_text))

    def post(self):
        method = self.request.get("method", None)
        number = self.request.get("number", None)
        cursor = self.request.get("cursor", None)
        refresh = self.request.get("refresh", None)
        random_text = self.request.get("random_text", "")
        
        try:
            number = int(number)
        except:
            number = None
        
        if random_text == "random":
            showed_random = True
        else:
            showed_random = False
        
        
        if method and number and method in OPTIONS:
            # key_name = "%s-%s" % (method, number)
            key_name = "%s-%s-%s" % (method, number, showed_random)
            stat = Stat.get_or_insert(key_name)
            
            q = Vote.all()
            q.filter("method =", method)
            q.filter("number =", number)
            q.filter("showed_random =", showed_random)

            if cursor:
                q.with_cursor(cursor)
            count = q.count()
            next_cursor = q.cursor() if count == 1000 else None
            if refresh or not stat.count:
                stat.count = 0
            stat.count = stat.count + count
            stat.method = method
            stat.number = number
            stat.showed_random = showed_random
            stat.generated = datetime.now()
            stat.put()

            if next_cursor:
                params = {
                    "number": number,
                    "method": method,
                    "cursor": next_cursor,
                    "random_text": random_text,
                }
                taskqueue.add(url="/tasks", params=params)


def main():
    application = webapp.WSGIApplication([
                                ('/tasks', TaskHandler),
                                        ],debug=True)
    util.run_wsgi_app(application)

if __name__ == '__main__':
    main()
