from pr.models import db
import datetime


class UserCampaigns(db.Model):
    __tablename__ = 'user_campaigns'

    user_id = db.Column(db.Integer, primary_key=True)
    camp_id = db.Column(db.Integer, primary_key=True)
    status_id = db.Column(db.Integer)
    updated_on = db.Column(db.DateTime(),
                           default=datetime.datetime.utcnow,
                           onupdate=datetime.datetime.utcnow)

    __table_args__ = (db.ForeignKeyConstraint(['user_id'],
                                              ['users.id'],
                                              name='UserCampaigns__user_id_fk'),
                      db.ForeignKeyConstraint(['camp_id'],
                                              ['campaigns.camp_id'],
                                              name='UserCampaigns__camp_id_fk')
                      )

    @classmethod
    def add_user_campaigns(cls, user_id, camp_id, status_id):
        user_campaign = cls(user_id=user_id, camp_id=camp_id, status_id=status_id)

        try:
            db.session.add(user_campaign)
            db.session.commit()
            print('Added user_campaign')
        except Exception:
            db.session.rollback()
            print('Mistake in user_campaign addition')
