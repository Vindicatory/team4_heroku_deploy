from flask.views import View
from flask import request, render_template, redirect, url_for
from flask_login import login_user
from pr.components.auth import LoginUser, get_login_user
from pr.models.users import Users


# --- 1.4. SingUpView
# Регистрация нового пользователя


class SingUpView(View):
    def dispatch_request(self):
        error = None
        if request.method == 'POST':
            if request.form['submit_button'] == 'Войти в аккаунт':
                return redirect(url_for('login'))
            else:
                username = request.form.get('username')
                name = request.form.get('name')
                surname = request.form.get('surname')
                email = request.form.get('email')
                password = request.form.get('password')
                phone = request.form.get('phone')
                if Users.check_unique(username, email, phone):
                    Users.add_user(username, password, name, surname, email, phone)
                    return redirect(url_for('login'))
                else:
                    error = 'Аккаунт с такими данными уже создан'
        return render_template('sing_up.html',
                               error=error)
