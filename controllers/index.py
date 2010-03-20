from urllib import urlencode
from datetime import datetime

from google.appengine.ext import webapp
from google.appengine.api import urlfetch
from django.utils import simplejson

from gaetwitter.config import DEBUG
from gaetwitter import model


class IndexController(webapp.RequestHandler):
    """ handles request from a cron job for updating a twitter status """
    def get(self):

        if not DEBUG and self.request.headers.get("X-AppEngine-Cron") != "true":
            # this request was not made by the task engine or during development, so don't do it
            return

        screen_name = self.request.get("screen_name")
        if screen_name:
            # retrieve the data
            url = "http://api.twitter.com/statuses/user_timeline.json?"
            params = urlencode({"screen_name": screen_name})
            response = urlfetch.fetch(url + params, method=urlfetch.GET)

            if response.status_code == 200:
                # parse it
                statuses = simplejson.loads(response.content)

                # we get a list of statuses to go through
                if statuses:
                    # get data from the most recent one
                    status = statuses[0]
                    body = status["text"]
                    timestamp = status["created_at"]
                    timestamp = datetime.strptime(timestamp, "%a %b %d %H:%M:%S +0000 %Y")

                    # save it to the database - override any there already
                    twitter_post = model.TwitterPost.all().get()
                    if twitter_post:
                        twitter_post.body = body
                        twitter_post.timestamp = timestamp
                    else:
                        twitter_post = model.TwitterPost(body=body, timestamp=timestamp)
                    twitter_post.put()

        return

