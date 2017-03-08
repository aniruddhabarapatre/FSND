import os
import webapp2

class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

class MainPage(webapp2.RequestHandler):
    def get(self):
        self.write("Hello Udacity")

app = webapp2.WSGIApplication([('/', MainPage)],
                               debug=true)
