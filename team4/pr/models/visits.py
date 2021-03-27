from pr.models import db
import datetime

class Visits(db.Model):
    __tablename__ = 'visits'

    visit_id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    user_id = db.Column(db.Integer, primary_key=True)
    camp_id = db.Column(db.Integer, primary_key=True)
    adress_id = db.Column(db.Integer, primary_key=True)
    entrance_number = db.Column(db.Integer)
    flat_number = db.Column(db.Integer)
    door_open = db.Column(db.Integer)
    visit_time = db.Column(db.DateTime(),
                           default=datetime.datetime.utcnow,
                           onupdate=datetime.datetime.utcnow)
    reaction = db.Column(db.Text)
    info = db.Column(db.Text)

    __table_args__ = {'sqlite_autoincrement': True}
    __table_args__ = (db.ForeignKeyConstraint(['adress_id'],
                                              ['adresses.adress_id'],
                                              name='Visits__adress_id_fk'),
                      db.ForeignKeyConstraint(['camp_id'],
                                              ['campaigns.camp_id'],
                                              name='Visits__camp_id_fk'),
                      db.ForeignKeyConstraint(['user_id'],
                                              ['users.id'],
                                              name='Visits__user_id_fk'),
                      )

    @classmethod
    def add_visit(cls,
                  user_id,
                  camp_id,
                  adress_id,
                  entrance_number,
                  flat_number,
                  door_open,
                  visit_time,
                  reaction,
                  info):
        """
        Добавление посещения квартиры.
        """
        visit = cls(user_id=user_id,
                    camp_id=camp_id,
                    adress_id=adress_id,
                    entrance_number=entrance_number,
                    flat_number=flat_number,
                    door_open=door_open,
                    visit_time=visit_time,
                    reaction=reaction,
                    info=info)

        try:
            db.session.add(visit)
            db.session.commit()
            print('Added visit')
        except Exception:
            db.session.rollback()
            print('Mistake in visit addition')

    class CurrentAddress():
        adress_id = 0
