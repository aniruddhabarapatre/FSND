import os

import jinja2
import webapp2

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape = True)

class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

class MainPage(Handler):
    def get(self):
        self.response.out.write("Hello World!!!")

class Rot13(Handler):
    def get(self):
        self.render("rot13.html")

    def post(self):
        input_text = self.request.get_all('input_text')
        output_text = self.rotate_by_13(input_text)
        self.render("rot13.html", input_text = output_text)

    def rotate_by_13(self, text):
        translated_text = ''
        for ch in text:
            if ch.isaplha():
                num = ord(ch) + 13

                if ch.isupper():
                    if num > ord('Z'):
                        num -= 26
                    elif num < ord('A'):
                        num += 26
                elif ch.islower():
                     if num > ord('z'):
                        num -= 26
                     elif num < ord('a'):
                        num += 26

                translated_text += chr(num)
            else:
                translated_text += ch
        return translated_text

app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/rot13', Rot13),
], debug=True)
