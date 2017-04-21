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

    def post(self, post_id):
        key = db.Key.from_path('Post', int(post_id), parent=blog_key())
        post = db.get(key)

        if not post:
            self.error(404)
            return

        comments = Comments.by_post(post)

        if self.user:
            if self.request.get("save_comment"):
                content = self.request.get("comment_content")
                user = User.by_name(self.user.name)

                if content:
                    newComment = Comments(user=user,
                                          post=post, comment=content)
                    newComment.put()
                    return self.redirect("/blog/%s" % str(post.key().id()))
                else:
                    comment_error = "Please enter text in comment box."
                    self.render("permalink.html", post=post,
                                comment_error=comment_error)

            if self.request.get("delete_comment"):
                comment_id = self.request.get("comment_id")
                comment = Comments.get_by_id(int(comment_id))
                if comment.user.name == self.user.name:
                    db.delete(comment)
                    return self.redirect("/blog/%s" % str(post.key().id()))
                else:
                    delete_error = "Failed to delete comment"
                    self.render("permalink.html", post=post,
                                delete_error=delete_error)
        else:
            return self.redirect("/blog")
