import os
import re
import random
import hashlib
import hmac
from string import letters

import webapp2
import jinja2

from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                                autoescape = True)

secret = "Udacity"

def render_str(template, **params):
    t = jinja_env.get_template(template)
    return t.render(params)

def make_secure_val(val):
    return '%s|%s' % (val, hmac.new(secret, val).hexdigest())

def check_secure_val(secure_val):
    val = secure_val.split('|')[0]
    if secure_val == make_secure_val(val):
        return val

def make_salt(length = 5):
    return ''.join(random.choice(letters) for x in xrange(length))

def make_pw_hash(name, pw, salt = None):
    if not salt:
        salt = make_salt()
    h = hashlib.sha256(name + pw + salt).hexdigest()
    return '%s,%s' % (salt, h)

def valid_pw(name, password, h):
    salt = h.split(',')[0]
    return h == make_pw_hash(name, password, salt)

class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        params['user'] = self.user
        return render_str(template, **params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

    def set_secure_cookie(self, name, val):
        cookie_val = make_secure_val(val)
        self.response.headers.add_header(
            'Set-Cookie',
            '%s=%s; Path=/' % (name, cookie_val))

    def read_secure_cookie(self, name):
        cookie_val = self.request.cookies.get(name)
        return cookie_val and check_secure_val(cookie_val)

    def login(self, user):
        self.set_secure_cookie('user_id', str(user.key().id()))

    def logout(self):
        self.response.headers.add_header('Set-Cookie', 'user_id=; Path=/')

    def initialize(self, *a, **kw):
        webapp2.RequestHandler.initialize(self, *a, **kw)
        uid = self.read_secure_cookie('user_id')
        self.user = uid and User.by_id(int(uid))

# Step 1: Basic Blog
def blog_key(name = 'default'):
    return db.Key.from_path('blogs', name)

# moved here from Step 2 for ReferenceProperty
def users_key(group = 'default'):
    return db.Key.from_path('users', group)

class User(db.Model):
    name = db.StringProperty(required = True)
    pw_hash = db.StringProperty(required = True)
    email = db.StringProperty()

    @classmethod
    def by_id(cls, uid):
        return User.get_by_id(uid, parent = users_key())

    @classmethod
    def by_name(cls, name):
        u = User.all().filter('name =', name).get()
        return u

    @classmethod
    def register(cls, name, pw, email = None):
        pw_hash = make_pw_hash(name, pw)
        return User(parent = users_key(),
                    name = name,
                    pw_hash = pw_hash,
                    email = email)

    @classmethod
    def login(cls, name, pw):
        u = cls.by_name(name)
        if u and valid_pw(name, pw, u.pw_hash):
            return u

class Post(db.Model):
    subject = db.StringProperty(required = True)
    content = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)
    last_modified = db.DateTimeProperty(auto_now_add = True)
    user = db.ReferenceProperty(User, collection_name = "user_posts")

    def render(self):
        self._render_text = self.content.replace('\n', '<br>')
        return render_str("post.html", p = self)

    @property
    def likes(self):
        likes = Likes.all().filter('post =', int(self.key().id()))
        return likes.count()

class BlogPage(Handler):
    def get(self):
        posts = db.GqlQuery("Select * From Post Order by created DESC limit 10")
        self.render("blog.html", posts=posts)

class Newpost(Handler):
    def render_newpost(self, subject="", content="", error=""):
        self.render("newpost.html", subject=subject, content=content, error=error)

    def get(self):
        if self.user:
            self.render_newpost()
        else:
            self.redirect("/login")

    def post(self):
        if not self.user:
            self.redirect('/blog')

        subject = self.request.get("subject")
        content = self.request.get("content")
        user = User.by_name(self.user.name)

        if subject and content:
            post = Post(parent=blog_key(), subject = subject, content = content, user = user)
            post.put()
            self.redirect("/blog/%s" % str(post.key().id()))
        else:
            error = "We need both subject and content."
            self.render_newpost(subject, content, error)

class PostPage(Handler):
    def get(self, post_id):
        key = db.Key.from_path('Post', int(post_id), parent=blog_key())
        post = db.get(key)
        comments = Comments.all().filter("post = ", post)

        if not post:
            self.error(404)
            return

        self.render("permalink.html", post=post, comments = comments)

    def post(self, post_id):
        key = db.Key.from_path('Post', int(post_id), parent = blog_key())
        post = db.get(key)

        comments = Comments.by_id(post)

        if self.request.get("save_comment"):
            content = self.request.get("comment_content")
            user = User.by_name(self.user.name)

            if content:
                newComment = Comments(user = user, post = post, comment = content)
                newComment.put()
                self.redirect("/blog/%s" % str(post.key().id()))
            else:
                comment_error = "Please enter text in comment box."
                self.render("permalink.html", post = post, comment_error = comment_error)

# Step 5: Additional Action Items
class EditPage(Handler):
    def get(self, post_id):
        post_value = post_id.split("/")[0]
        key = db.Key.from_path('Post', int(post_value), parent=blog_key())
        post = db.get(key)

        if not post:
            self.error(404)
            return

        if self.user:
            self.render("editpost.html", post = post)
        else:
            error_msg = 'You can only edit your own post.'
            self.redirect("/blog", error = error_msg)

    def post(self, post_id):
        post_value = post_id.split("/")[0]
        key = db.Key.from_path('Post', int(post_value), parent=blog_key())
        post = db.get(key)

        if not post:
            self.error(404)
            return

        if self.request.get("save"):
            subject = self.request.get("subject")
            content = self.request.get("content")

            if subject and content:
                post.subject = subject
                post.content = content
                post.put()
                self.redirect("/blog/%s" % str(post.key().id()))
            else:
                error = "We need both subject and content."
                self.render("editpost.html", subject = subject, content = content, error = error)
        elif self.request.get("cancel"):
            self.redirect("/blog/%s" % str(post_value))

class DeletePage(Handler):
    def get(self, post_id):
        post_value = post_id.split("/")[0]
        key = db.Key.from_path('Post', int(post_value), parent=blog_key())
        post = db.get(key)

        if not post:
            self.error(404)
            return

        if self.user:
            post.delete()
            self.redirect("/blog")

class Likes(db.Model):
    post = db.IntegerProperty(required = True)
    user = db.StringProperty(required = True)

class LikePost(Handler):
    def get(self, post_id):
        post_value = post_id.split("/")[0]
        key = db.Key.from_path('Post', int(post_value), parent=blog_key())
        post = db.get(key)
        like_user = Likes.all().filter('post =', int(post_value)).filter('user = ', self.user.name).get()

        if self.user and not like_user:
            like = Likes(post = post.key().id(), user = self.user.name)
            like.put()
            self.redirect("/blog/%s" % str(post_value))
        else:
            error_msg = "You can only like post once."
            self.redirect("/blog/%s?like_error=%s" % str(post_value), error_msg)

class Comments(db.Model):
    user = db.ReferenceProperty(User, required = True)
    post = db.ReferenceProperty(Post, required = True)
    comment = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)

    def render(self):
        self._render_text = self.content.replace('\n', '<br>')
        return render_str("comments.html", comments = self)

    @classmethod
    def by_id(cls, cid):
        comments = Comments.all().filter("post =", id).order('created')
        return comments

class EditComment(Handler):
    def post(self, post_id):
        post_value = post_id.split("/")[0]
        key = db.Key.from_path('Post', int(post_value), parent=blog_key())
        post = db.get(key)

        # if self.request.get("save_comment"):
        #     content = self.request.get("comment_content")
        #     user = User.by_name(self.user.name)

        #     if user and content:
        #         post = Post(parent=blog_key(), subject = subject, content = content, user = user)
        #         post.put()
        #         self.redirect("/blog/%s" % str(post.key().id()))
        #     else:
        #         error = "We need both subject and content."
        #         self.render_newpost(subject, content, error)

# Step 2: User Registration

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
    return username and USER_RE.match(username)

PASS_RE = re.compile(r"^.{3,20}$")
def valid_password(password):
    return password and PASS_RE.match(password)

EMAIL_RE  = re.compile(r'^[\S]+@[\S]+\.[\S]+$')
def valid_email(email):
    return not email or EMAIL_RE.match(email)

class Signup(Handler):
    def get(self):
        self.render("signup-form.html")

    def post(self):
        have_error = False
        self.username = self.request.get('username')
        self.password = self.request.get('password')
        self.verify = self.request.get('verify')
        self.email = self.request.get('email')

        params = dict(username = self.username,
                      email = self.email)

        if not valid_username(self.username):
            params['error_username'] = "That's not a valid username."
            have_error = True

        if not valid_password(self.password):
            params['error_password'] = "That wasn't a valid password."
            have_error = True
        elif self.password != self.verify:
            params['error_verify'] = "Your passwords didn't match."
            have_error = True

        if not valid_email(self.email):
            params['error_email'] = "That's not a valid email."
            have_error = True

        if have_error:
            self.render('signup-form.html', **params)
        else:
            self.done()

    def done(self, *a, **kw):
        raise NotImplementedError

class Register(Signup):
    def done(self):
        #make sure the user doesn't already exist
        u = User.by_name(self.username)
        if u:
            msg = 'That user already exists.'
            self.render('signup-form.html', error_username = msg)
        else:
            u = User.register(self.username, self.password, self.email)
            u.put()

            self.login(u)
            self.redirect('/welcome')

class Welcome(Handler):
    def get(self):
        if self.user:
            self.render('welcome.html', username = self.user.name)
        else:
            self.redirect('/signup')

# Step 3: Login
class Login(Handler):
    def get(self):
        self.render('login-form.html')

    def post(self):
        username = self.request.get('username')
        password = self.request.get('password')

        u = User.login(username, password)
        if u:
            self.login(u)
            self.redirect('/welcome')
        else:
            msg = 'Invalid login'
            self.render('login-form.html', error = msg)

# Step 4: Logout
class Logout(Handler):
    def get(self):
        self.logout()
        self.redirect('/blog')

# Routes
app = webapp2.WSGIApplication([
    ('/blog/?', BlogPage),
    ('/blog/newpost', Newpost),
    ('/blog/([0-9]+)', PostPage),
    ('/blog/([0-9]+/editpost)', EditPage),
    ('/blog/([0-9]+/deletepost)', DeletePage),
    ('/blog/([0-9]+/likepost)', LikePost),
    ('/blog/([0-9]+/comment)', EditComment),
    ('/signup', Register),
    ('/welcome', Welcome),
    ('/login', Login),
    ('/logout', Logout),
], debug=True)
