from pr.models import db
import datetime


class Campaigns(db.Model):
    __tablename__ = 'campaigns'

    camp_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    camp_title = db.Column(db.Text, nullable=False, unique=True)
    camp_description = db.Column(db.Text)
    camp_updated_on = db.Column(db.DateTime(),
                                default=datetime.datetime.utcnow,
                                onupdate=datetime.datetime.utcnow)
    camp_status = db.Column(db.Boolean,
                            server_default='f',
                            nullable=False,
                            default=False)

    __table_args__ = {'sqlite_autoincrement': True}

    @classmethod
    def add_campaign(cls, camp_title, camp_description, camp_status):
        """
        Добавление Кампании.
        """
        campaign = cls(camp_title=camp_title,
                       camp_description=camp_description,
                       camp_status=camp_status)

        try:
            db.session.add(campaign)
            db.session.commit()
            print('Added campaign')
        except Exception:
            db.session.rollback()
            print('Mistake in campaign addition')

    @staticmethod
    # Проверка уникальности кампании
    def check_unique_campaign(camp_title):
        database = Campaigns.query.filter(Campaigns.camp_title == camp_title).first()
        if database is not None:
            return False
        else:
            return True
