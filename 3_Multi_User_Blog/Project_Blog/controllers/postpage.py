from controllers.handler import Handler
from models.post import Post
from models.user import User
from models.likes import Likes
from models.comments import Comments

from google.appengine.ext import db


def blog_key(name='default'):
    return db.Key.from_path('blogs', name)


class PostPage(Handler):
    def get(self, post_id):
        key = db.Key.from_path('Post', int(post_id), parent=blog_key())
        post = db.get(key)
        comments = Comments.all().filter("post = ", post)

        if not post:
            self.error(404)
            return

        self.render("permalink.html", post=post, comments=comments)
