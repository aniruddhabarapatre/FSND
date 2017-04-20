from handler import Handler
from models import Post

from google.appengine.ext import db


def blog_key(name='default'):
    return db.Key.from_path('blogs', name)


class BlogPage(Handler):
    def get(self):
        posts = db.GqlQuery("Select * From Post Order by created DESC")
        self.render("blog.html", posts=posts)
