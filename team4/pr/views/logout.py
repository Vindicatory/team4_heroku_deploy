from flask.views import View
from flask_login import logout_user
from flask import redirect, url_for


# Класс, отвечающий за разлогин пользователя


class LogoutView(View):
    def dispatch_request(self):
        logout_user()
        return redirect(url_for('main_page'))
