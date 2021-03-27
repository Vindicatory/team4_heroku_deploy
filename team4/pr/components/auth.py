from flask_login import UserMixin
from pr.models.users import Users


# --- 1.2. Определение класса пользователя

class LoginUser(UserMixin):

    def __init__(self, user_dict):
        self.id = user_dict.id
        self.name = user_dict.username
        self.password = user_dict.password_hash

    def get_id(self):
        return str(self.name)


def get_login_user(user_name: str):
    """
    Функция для проверки корректности ввода пользователя.

    :param user_name: login_of_user
    :return:
    """
    db = Users.query.filter(Users.username == user_name).first()
    if db is not None:
        return LoginUser(db)
