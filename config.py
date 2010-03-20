# this is the place for all the application configuration constants


# dynamically determine whether we're serving on development or production (error on the side of production)
import os

if os.environ.get('SERVER_SOFTWARE', '').startswith('Development'):
    DEBUG = True
else:
    DEBUG = False


# url routes
TWITTER_URL = '/twitter'

from controllers import index

ROUTES = [(TWITTER_URL, index.IndexController)]
