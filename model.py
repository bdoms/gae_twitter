
from google.appengine.ext import db


# standard model objects
class TwitterPost(db.Model):

    body = db.StringProperty(required=True)
    timestamp = db.DateTimeProperty(required=True)


# misc functions
def refresh(model_instance):
    # refeshes an instance in case things were updated since the last reference to this object (used in testing)
    return db.get(model_instance.key())

def getPost():
    return TwitterPost.all().get()

