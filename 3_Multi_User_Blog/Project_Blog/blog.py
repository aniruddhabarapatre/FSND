import os
import re
from string import letters

import jinja2
import webapp2

from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                                autoescape = True)

def render_str(template, **params):
    t = jinja_env.get_template(template)
    return t.render(params)

class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        return render_str(template, **params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

def blog_key(name = 'default'):
    return db.Key.from_path('blogs', name)

class BlogPage(Handler):
    def get(self):
        posts = db.GqlQuery("Select * From Post Order by created DESC limit 10")
        self.render("blog.html", posts=posts)

class Newpost(Handler):
    def render_newpost(self, subject="", content="", error=""):
        self.render("newpost.html", subject=subject, content=content, error=error)

    def get(self):
        self.render_newpost()

    def post(self):
        subject = self.request.get("subject")
        content = self.request.get("content")

        if subject and content:
            post = Post(parent=blog_key(), subject = subject, content = content)
            post.put()
            self.redirect("/blog/%s" % str(post.key().id()))
        else:
            error = "We need both subject and content."
            self.render_newpost(subject, content, error)

# Routes
app = webapp2.WSGIApplication([
    ('/blog', BlogPage),
    ('/blog/newpost', Newpost),
    ('/blog/([0-9]+)', PostPage),
], debug=True)
