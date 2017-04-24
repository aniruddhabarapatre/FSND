from controllers.handler import Handler
from models.post import Post
from models.user import User

from google.appengine.ext import db


def blog_key(name='default'):
    return db.Key.from_path('blogs', name)


class NewPost(Handler):
    def render_newpost(self, subject="", content="", error=""):
        self.render("newpost.html", subject=subject,
                    content=content, error=error)

    def get(self):
        if self.user:
            self.render_newpost()
        else:
            return self.redirect("/login")

    def post(self):
        if not self.user:
            return self.redirect('/blog')

        subject = self.request.get("subject")
        content = self.request.get("content")
        user = User.by_name(self.user.name)

        if subject and content:
            post = Post(parent=blog_key(), subject=subject,
                        content=content, user=user)
            post.put()
            return self.redirect("/blog/%s" % str(post.key().id()))
        else:
            error = "We need both subject and content."
            self.render_newpost(subject, content, error)
