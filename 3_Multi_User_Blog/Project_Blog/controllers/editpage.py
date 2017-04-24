from controllers.handler import Handler
from models.post import Post
from models.user import User

from google.appengine.ext import db


def blog_key(name='default'):
    return db.Key.from_path('blogs', name)


class EditPage(Handler):
    def get(self, post_id):
        post_value = post_id.split("/")[0]
        key = db.Key.from_path('Post', int(post_value), parent=blog_key())
        post = db.get(key)

        if not post:
            self.error(404)
            return

        if self.user:
            self.render("editpost.html", post=post)
        else:
            error_msg = 'You can only edit your own post.'
            return self.redirect("/blog", error=error_msg)

    def post(self, post_id):
        if not self.user:
            return self.redirect('/blog')

        post_value = post_id.split("/")[0]
        key = db.Key.from_path('Post', int(post_value), parent=blog_key())
        post = db.get(key)

        if not post:
            self.error(404)
            return

        if self.request.get("save"):
            subject = self.request.get("subject")
            content = self.request.get("content")

            if post.user.key().id() == User.by_name(self.user.name).key().id():
                if subject and content:
                    post.subject = subject
                    post.content = content
                    post.put()
                    return self.redirect("/blog/%s" % str(post.key().id()))
                else:
                    error = "We need both subject and content."
                    self.render("editpost.html", subject=subject,
                                content=content, error=error)
        elif self.request.get("cancel"):
            return self.redirect("/blog/%s" % str(post_value))
