from controllers.handler import Handler
from models.post import Post
from models.user import User
from models.likes import Likes

from google.appengine.ext import db


class LikePost(Handler):
    def get(self, post_id):
        post_value = post_id.split("/")[0]
        key = db.Key.from_path('Post', int(post_value), parent=blog_key())
        post = db.get(key)
        like_user = Likes.all().filter('post =',
                                       int(post_value)).filter(
                                       'user = ', self.user.name).get()

        if self.user and not like_user:
            like = Likes(post=post.key().id(), user=self.user.name)
            like.put()
            return self.redirect("/blog/%s" % str(post_value))
        else:
            error_msg = "You can only like post once."
            return self.redirect("/blog/%s?like_error=%s" % str(post_value),
                                 error_msg)
