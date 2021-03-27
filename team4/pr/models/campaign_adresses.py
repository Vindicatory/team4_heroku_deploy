from pr.models import db
import datetime


class CampaignAdresses(db.Model):
    __tablename__ = 'campaign_adresses'

    camp_id = db.Column(db.Integer, primary_key=True)
    adress_id = db.Column(db.Integer, primary_key=True)

    __table_args__ = (db.ForeignKeyConstraint(['camp_id'],
                                              ['campaigns.camp_id'],
                                              name='CampaignAdresses__camp_id_fk'),
                      db.ForeignKeyConstraint(['adress_id'],
                                              ['adresses.adress_id'],
                                              name='CampaignAdresses__adress_id_fk'),
                      )
