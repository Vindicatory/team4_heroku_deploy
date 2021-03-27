from pr.models import db
from pr.models.campaign_adresses import CampaignAdresses
import logging


class Adresses(db.Model):
    __tablename__ = 'adresses'

    adress_id = db.Column(db.Integer, unique=True, primary_key=True, autoincrement=True)
    town = db.Column(db.Text)
    street = db.Column(db.Text)
    house_number = db.Column(db.Text)
    amount_of_entrance_number = db.Column(db.Integer)
    amount_of_flats = db.Column(db.Integer)

    __table_args__ = {'sqlite_autoincrement': True}

    @staticmethod
    def query_get_last_adress_id():
        """
        Последний adress_id

        :use:
            :: pr.views.edit_campaign
        :return: adress_id
        """
        return db.session.execute(
            f"select MAX(adress_id) as max from adresses").first()

    @classmethod
    def add_address(cls,
                    town,
                    street,
                    house_number,
                    amount_of_entrance_number,
                    amount_of_flats,
                    camp_id):
        """
        Добавление адреса.
        """
        address = cls(town=town,
                      street=street,
                      house_number=house_number,
                      amount_of_entrance_number=amount_of_entrance_number,
                      amount_of_flats=amount_of_flats)

        try:
            db.session.add(address)
            db.session.commit()
            print('Added address')
        except Exception:
            db.session.rollback()
            print('Mistake in address addition')

        adress_id = Adresses.query_get_last_adress_id()
        logging.info(adress_id[0])
        campaign_address = CampaignAdresses(camp_id=camp_id, adress_id=adress_id[0])

        try:
            db.session.add(campaign_address)
            db.session.commit()
            print('Added campaign_address')
        except Exception:
            db.session.rollback()
            print('Mistake in campaign_address addition')
