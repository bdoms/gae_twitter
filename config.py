# this is the place for all the application configuration constants


# dynamically determine whether we're serving on development or production (error on the side of production)
if os.environ.get('SERVER_SOFTWARE', '').startswith('Development'):
    DEBUG = True
else:
    DEBUG = False


# twitter configuration
TWITTER_USER = 'twitterapi' # the user to grab updates from


# url routes
TWITTER_URL = '/twitter'

from controllers import index

ROUTES = [(TWITTER_URL, index.IndexController)]
