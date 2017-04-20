from controllers.handler import Handler
from models.user import User


class Login(Handler):
    def get(self):
        self.render('login-form.html')

    def post(self):
        username = self.request.get('username')
        password = self.request.get('password')

        u = User.login(username, password)
        if u:
            self.login(u)
            return self.redirect('/welcome')
        else:
            msg = 'Invalid login'
            self.render('login-form.html', error=msg)
