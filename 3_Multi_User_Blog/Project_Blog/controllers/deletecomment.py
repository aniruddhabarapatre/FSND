from controllers.handler import Handler
from models.post import Post
from models.user import User
from models.comments import Comments

from google.appengine.ext import db


def blog_key(name='default'):
    return db.Key.from_path('blogs', name)


class DeleteComment(Handler):
    def post(self):
        post_id = self.request.get("post_id")
        comment_id = self.request.get("comment_id")
        key = db.Key.from_path('Post', int(post_id), parent=blog_key())
        post = db.get(key)

        if not post:
            self.error(404)
            return

        if self.user:
            comment = Comments.get_by_id(int(comment_id))
            if comment is not None and comment.user.name == self.user.name:
                db.delete(comment)
                return self.redirect("/blog/%s" % str(post.key().id()))
            else:
                delete_error = "Failed to delete comment"
                self.render("permalink.html", post=post,
                            delete_error=delete_error)
        else:
            return self.redirect("/blog")
