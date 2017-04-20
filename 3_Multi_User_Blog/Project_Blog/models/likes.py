from google.appengine.ext import db


class Likes(db.Model):
    post = db.IntegerProperty(required=True)
    user = db.StringProperty(required=True)
