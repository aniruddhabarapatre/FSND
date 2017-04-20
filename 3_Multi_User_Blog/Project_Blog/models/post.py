from google.appengine.ext import db
from user import User


class Post(db.Model):
    subject = db.StringProperty(required=True)
    content = db.TextProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)
    last_modified = db.DateTimeProperty(auto_now_add=True)
    user = db.ReferenceProperty(User, collection_name="user_posts")

    def render(self):
        self._render_text = self.content.replace('\n', '<br>')
        return render_str("post.html", p=self)

    @property
    def likes(self):
        likes = Likes.all().filter('post =', int(self.key().id()))
        return likes.count()
