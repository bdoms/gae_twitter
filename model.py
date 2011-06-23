import re
from time import mktime

from google.appengine.ext import db


# standard model objects
class TwitterPost(db.Model):

    body = db.StringProperty(required=True)
    url = db.StringProperty(required=True)
    timestamp = db.DateTimeProperty(required=True)

    @property
    def secondsSinceEpoch(self):
        return mktime(self.timestamp.timetuple())


# misc functions
def refresh(model_instance):
    # refeshes an instance in case things were updated since the last reference to this object (used in testing)
    return db.get(model_instance.key())

def getPost():
    return TwitterPost.all().get()

# based on formencode.validators.URL.url_re, with slight modifications
URL_RE = re.compile(r'''
        ((http|https)://
        (?:[%:\w]*@)?                                               # authenticator
        (?P<domain>[a-z0-9][a-z0-9\-]{1,62}\.)*                     # (sub)domain - alpha followed by 62max chars (63 total)
        (?P<tld>[a-z]{2,})                                          # TLD
        (?::[0-9]+)?                                                # port
        (?P<path>/[a-z0-9\-\._~:/\?#\[\]@!%\$&\'\(\)\*\+,;=]*)?)    # files/delims/etc
    ''', re.I | re.VERBOSE)

def linkURLs(string):
    match = re.search(URL_RE, string)
    if match:
        url = match.group(1)
        # fix to remove a trailing parenthesis if one precedes the url
        if string[string.index(url) - 1] == "(" and url.endswith(")"):
            url = url[:-1]
        string = string.replace(url, '<a href="' + url + '" target="_blank" rel="nofollow">' + url + '</a>')
    return string

AT_RE = re.compile(r'@([\w_]+)')

def linkAts(string):
    return AT_RE.sub(r'@<a href="http://twitter.com/\1" target="_blank" rel="nofollow">\1</a>', string)

HASH_RE = re.compile(r'#([\w_]+)')

def linkHashes(string):
    return HASH_RE.sub(r'<a href="http://twitter.com/search?q=%23\1" target="_blank" rel="nofollow">#\1</a>', string)

