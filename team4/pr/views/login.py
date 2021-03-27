from flask.views import View
from flask import request, render_template, redirect, url_for, flash
from flask_login import login_user
from pr.components.auth import LoginUser, get_login_user
from pr.models.users import Users
from flask_wtf import FlaskForm
from wtforms.fields import StringField


# --- 1.4. LoginView
# Пользователь логинится


class LoginView(View):
    def dispatch_request(self):
        error = None
        if request.method == 'POST':
            if request.form['submit_button'] == 'Завести аккаунт':
                return redirect(url_for('singup'))
            else:
                username = request.form.get('username')
                password = request.form.get('password')
                is_correct, error_code = Users.check_password(username, password)
                if is_correct:
                    user = get_login_user(username)
                    login_user(user)  # сохраняем данные о пользователе в сессии
                    return redirect(url_for('main_page'))
                else:
                    error = 'Пароль/логин неверный'
        return render_template('sing_in.html',
                               error=error)
