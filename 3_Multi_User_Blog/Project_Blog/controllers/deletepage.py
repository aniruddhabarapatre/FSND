from controllers.handler import Handler
from models.post import Post
from models.user import User

from google.appengine.ext import db


def blog_key(name='default'):
    return db.Key.from_path('blogs', name)


class DeletePage(Handler):
    def get(self, post_id):
        post_value = post_id.split("/")[0]
        key = db.Key.from_path('Post', int(post_value), parent=blog_key())
        post = db.get(key)

        if not post:
            self.error(404)
            return

        if post.user.key().id() == User.by_name(self.user.name).key().id():
            post.delete()
            return self.redirect("/blog")
        else:
            delete_error = "Failed to delete post."
            self.render("permalink.html", post=post, error=delete_error)
