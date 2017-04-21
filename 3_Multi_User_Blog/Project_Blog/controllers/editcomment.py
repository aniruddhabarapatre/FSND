from controllers.handler import Handler
from models.post import Post
from models.user import User
from models.comments import Comments

from google.appengine.ext import db


def blog_key(name='default'):
    return db.Key.from_path('blogs', name)


class EditComment(Handler):
    def get(self, post_id, comment_id):
        key = db.Key.from_path('Post', int(post_id), parent=blog_key())
        post = db.get(key)

        comment = Comments.get_by_id(int(comment_id))
        if self.user and comment:
            if comment.user.name == self.user.name:
                self.render("editcomment.html", comment=comment)
            else:
                return self.redirect("/blog/%s" % str(post.key().id()))

    def post(self, post_id, comment_id):
        key = db.Key.from_path('Post', int(post_id), parent=blog_key())
        post = db.get(key)

        if self.request.get("save"):
            comment = Comments.get_by_id(int(comment_id))
            if self.user and comment:
                if comment.user.name == self.user.name:
                    comment.comment = self.request.get("comment")
                    comment.put()
                    return self.redirect("/blog/%s" % str(post.key().id()))
                else:
                    save_error = \
                        "Only the author of the comment can make changes."
                    self.render("editcomment.html", comment=comment,
                                error=save_error)

        if self.request.get("cancel"):
            return self.redirect("/blog/%s" % str(post.key().id()))
