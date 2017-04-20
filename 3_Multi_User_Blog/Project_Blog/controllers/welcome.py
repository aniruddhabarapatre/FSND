from controllers.handler import Handler
from controllers.signup import *


class Welcome(Handler):
    def get(self):
        if self.user:
            self.render('welcome.html', username=self.user.name)
        else:
            return self.redirect('/signup')

