from google.appengine.ext import webapp
from google.appengine.ext.webapp import util

from models import doVote, doFollowup
from handler_utils import renderToResponse, jsonResponse
import settings

class MainHandler(webapp.RequestHandler):
    def get(self):
        renderToResponse(self, 'index.html.django')

class VoteHandler(webapp.RequestHandler):
    def post(self):
        number          = self.request.get('number', None)
        method          = self.request.get('method', None)
        pick            = self.request.get('pick', None)
        submit          = self.request.get('submit', None)
        showed_random   = self.request.get('random', None)
        
        ip = self.request.remote_addr
        
        result = { 'status': 'failed' }
        vote = doVote(number, method, pick, submit, showed_random, ip)
        if vote:
            result = {
                'status'    : 'success',
                'vote_id'   : str(vote.key())
            }

        jsonResponse(self, result)

class FollowupHandler(webapp.RequestHandler):
    def post(self):
        vote_id         = self.request.get('vote_id', None)
        how             = self.request.get('how', None)
        why             = self.request.get('why', None)
        
        result = { 'status': 'failed' }
        followup = doFollowup(vote_id, how, why)
        if followup:
            result = {
                'status'    : 'success',
            }

        jsonResponse(self, result)

class ResultHandler(webapp.RequestHandler):
    def get(self):
        renderToResponse(self, 'results.html.django')

class RedirectResultHandler(webapp.RequestHandler):
    def get(self):
        self.redirect('/results/')

def main():
    application = webapp.WSGIApplication([
                                ('/',           MainHandler),
                                ('/vote/',      VoteHandler),
                                ('/followup/',  FollowupHandler),
                                ('/results',    RedirectResultHandler),
                                ('/results/',   ResultHandler),
                                ],debug=settings.DEBUG)
    util.run_wsgi_app(application)

if __name__ == '__main__':
    main()