
from google.appengine.ext import webapp
from google.appengine.api import urlfetch
from django.utils import simplejson

from gaetwitter.config import DEBUG, TWITTER_USER
from gaetwitter import model


class IndexController(webapp.RequestHandler):
    """ handles request from a cron job for updating a twitter status """
    def get(self):

        if not DEBUG and self.request.headers.get("X-AppEngine-Cron") != "true":
            # this request was not made by the task engine or during development, so don't do it
            return

        # retrieve the data
        url = "http://api.twitter.com/statuses/user_timeline.json"
        payload = urllib.urlencode({"screen_name": TWITTER_USER})
        result = urlfetch.fetch(url, payload=payload, method=urlfetch.GET)

        # parse it
        statuses = simplejson.loads(result)

        # we get a list of statuses to go through
        if statuses:
            # get data from the most recent one
            status = statuses[0]
            body = status.text
            timestamp = status.created_at

            # save it to the database
            print body, timestamp
            twitter_post = model.TwitterPost(body=body, timestamp=timestamp)
            twitter_post.put()

        return

