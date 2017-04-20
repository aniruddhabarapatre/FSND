from google.appengine.ext import db
from user import User
from post import Post


class Comments(db.Model):
    user = db.ReferenceProperty(User, required=True)
    post = db.ReferenceProperty(Post, required=True)
    comment = db.TextProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)

    def render(self):
        self._render_text = self.content.replace('\n', '<br>')
        return render_str("comments.html", comments=self)

    @classmethod
    def by_post(cls, cid):
        comments = Comments.all().filter("post =", id).order('created')
        return comments

    @classmethod
    def by_id(cls, cid):
        comment = Comments.all().filter("ID =", cid)
        return comment
