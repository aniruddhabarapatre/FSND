from controllers.handler import Handler


class Logout(Handler):
    def get(self):
        self.logout()
        return self.redirect('/blog')
