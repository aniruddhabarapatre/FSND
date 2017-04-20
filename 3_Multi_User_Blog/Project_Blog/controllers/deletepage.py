from controllers.handler import Handler
from models.post import Post

from google.appengine.ext import db


class DeletePage(Handler):
    def get(self, post_id):
        post_value = post_id.split("/")[0]
        key = db.Key.from_path('Post', int(post_value), parent=blog_key())
        post = db.get(key)

        if not post:
            self.error(404)
            return

        if self.user:
            post.delete()
            return self.redirect("/blog")
