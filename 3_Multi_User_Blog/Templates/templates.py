import os
import webapp2

form_html = """
<form>
<h2>Add a Food</h2>
<input type="text" name="food">
<input type="hidden" name="food" value="eggs">
<button>Add</button>
</form>
"""

class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

class MainPage(Handler):
    def get(self):
        self.write(form_html)

app = webapp2.WSGIApplication([
    ('/', MainPage),
], debug=True)
