import os
import webapp2
import jinja2

from controllers import Handler, BlogPage, NewPost, PostPage, EditPage, Signup, Welcome
from controllers import DeletePage, Login, Logout, EditComment, LikePost, Register
from models import User, Post, Likes, Comments


# Routes
app = webapp2.WSGIApplication([
    ('/blog/?', BlogPage),
    ('/blog/newpost', NewPost),
    ('/blog/([0-9]+)', PostPage),
    ('/blog/([0-9]+/editpost)', EditPage),
    ('/blog/([0-9]+/deletepost)', DeletePage),
    ('/blog/([0-9]+/likepost)', LikePost),
    ('/blog/([0-9]+)/([0-9]+)/editcomment', EditComment),
    ('/signup', Register),
    ('/welcome', Welcome),
    ('/login', Login),
    ('/logout', Logout),
], debug=True)
