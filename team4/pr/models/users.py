from pr.models import db
from werkzeug.security import generate_password_hash, check_password_hash
import datetime


class Users(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.Text, nullable=False, unique=True)
    password_hash = db.Column(db.Text, nullable=False)
    first_name = db.Column(db.Text)
    second_name = db.Column(db.Text)
    email = db.Column(db.Text, nullable=False)
    phone = db.Column(db.Text)
    updated_on = db.Column(db.DateTime(),
                           default=datetime.datetime.utcnow,
                           onupdate=datetime.datetime.utcnow)

    __table_args__ = {'sqlite_autoincrement': True}

    @classmethod
    def add_user(cls, username, password, first_name, second_name, email, phone):
        """
        Добавление пользователей.

        Parameters
        ----------
        kwargs

        Returns
        -------

        """
        user = cls(username=username,
                   first_name=first_name,
                   second_name=second_name,
                   email=email,
                   phone=phone)
        user.set_password(password)
        print(user)
        try:
            db.session.add(user)
            db.session.commit()
            print('Add user')
        except Exception:
            db.session.rollback()
            print('Mistake')

    @staticmethod
    # Проверка пароля по бд
    def check_password(username, password):
        database = Users.query.filter(Users.username == username)
        fact_db = [(row.id, row.password_hash) for row in database]
        print(fact_db)
        if fact_db:
            return database[0].check_pass(password), 0
        else:
            print(f'Пользователь {username} отсутствует в базе данных')
            return False, 1

    @staticmethod
    # Проверка уникальности имени,
    # имейла и телефона при регистрации (доделать проверку по email и phone)
    def check_unique(username, email, phone):
        database = Users.query.filter(Users.username == username)
        fact_db = [row.id for row in database]
        if fact_db:
            return False
        else:
            return True  # Пользователь уникален

    def __repr__(self):
        return f"<{self.id}:{self.username}>"

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_pass(self, password):
        return check_password_hash(self.password_hash, password)
