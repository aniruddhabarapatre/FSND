from controllers.handler import Handler
from models.post import Post
from models.user import User
from models.comments import Comments

from google.appengine.ext import db


def blog_key(name='default'):
    return db.Key.from_path('blogs', name)


class SaveComment(Handler):
    def post(self):
        post_id = self.request.get("post_id")
        key = db.Key.from_path('Post', int(post_id), parent=blog_key())
        post = db.get(key)

        if not post:
            self.error(404)
            return

        if self.user:
            comment = self.request.get("comment_content")
            user = User.by_name(self.user.name)

            if comment:
                newComment = Comments(user=user,
                                      post=post, comment=comment)
                newComment.put()
                return self.redirect("/blog/%s" % str(post.key().id()))
            else:
                comment_error = "Please enter text in comment box."
                self.render("permalink.html", post=post,
                            comment_error=comment_error)
        else:
            return self.redirect("/blog")
