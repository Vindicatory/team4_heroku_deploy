from flask import Flask
from flask_login import LoginManager
from pr.components.auth import get_login_user
from pr.views.hello import HelloView
from pr.views.login import LoginView
from pr.views.logout import LogoutView
from pr.views.sing_up import SingUpView
from pr.views.createcampaign import NewCampaign
from pr.models import db
from pr.models.adresses import Adresses
from pr.models.campaigns import Campaigns
from pr.models.user_campaigns import UserCampaigns
from pr.models.users import Users
from pr.models.campaign_adresses import CampaignAdresses
from pr.views.visit import VisitsView
from flask_bootstrap import Bootstrap
from pr.views.edit_campaign import EditCampaign


def create_app():
    app = Flask(__name__)
    # Подключаем Boostrap
    Bootstrap(app)
    # 1.0 Инициализация и подключение к базе данных

    app.config.update(SECRET_KEY='mysecret')
    with open("keys/key.txt") as f:
        key = f.read()

    app.config['SQLALCHEMY_DATABASE_URI'] = key
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Warning processing
    db.init_app(app)

    # 1.1 Инициализация LoginManager

    login_manager = LoginManager()
    login_manager.init_app(app)

    # 1.3. Подключение лоадера пользователя из файла components/auth.py
    login_manager.user_loader(get_login_user)

    # 1.6. Автоматический редирект на login
    login_manager.login_view = 'login'

    # 1.5. Добавление view к приложению
    app.add_url_rule('/',
                     view_func=HelloView.as_view('main_page'),
                     methods=['GET', 'POST'])
    app.add_url_rule('/login',
                     view_func=LoginView.as_view('login'),
                     methods=['GET', 'POST'])
    app.add_url_rule('/singup',
                     view_func=SingUpView.as_view('singup'),
                     methods=['GET', 'POST'])
    app.add_url_rule('/logout',
                     view_func=LogoutView.as_view('logout'),
                     methods=['GET', 'POST'])
    app.add_url_rule('/newcampaign',
                     view_func=NewCampaign.as_view('newcampaign'),
                     methods=['GET', 'POST'])
    app.add_url_rule('/edit_campaign/<camp_id>',
                     view_func=EditCampaign.as_view('edit_campaign'),
                     methods=['GET', 'POST'])
    app.add_url_rule('/visit/<adress_id>',
                     view_func=VisitsView.as_view('visit'),
                     methods=['GET', 'POST'])

    return app


if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        db.create_all()
    app.run()
