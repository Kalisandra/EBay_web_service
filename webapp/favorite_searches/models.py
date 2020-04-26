from datetime import datetime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from webapp.model import db


class Favorite_searches(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('user.id', ondelete='CASCADE'),
        index=True
    )
    query_name = db.Column(db.String(50), nullable=False)
    user_query = db.Column(db.String(100), nullable=False)
    chosen_categoryid = db.Column(db.Integer, nullable=False)
    filter_request = db.Column(db.Text, nullable=False)
    date_of_creation = db.Column(db.DateTime, nullable=False, default=datetime.now())
    statistic_status = db.Column(db.Boolean, nullable=True)
    statistic_start_date = db.Column(db.DateTime, nullable=True)
    user = relationship('User', backref='favorite_searches')


    def __repr__(self):
        return '<user_id={} query={} filter_request={}>'.format(self.user_id, self.user_query, self.filter_request)


class Statistic_items(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    query_id = db.Column(
        db.Integer,
        db.ForeignKey('favorite_searches.id', ondelete='CASCADE'),
        index=True,
        nullable=False,
    )
    item_id = db.Column(db.String(50), nullable=False)
    item_name = db.Column(db.String(200), nullable=True)
    item_current_price = db.Column(db.String(10), nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    final_price = db.Column(db.String(10), nullable=True)
    item_url = db.Column(db.String(200), nullable=False)
    favorite_searches = relationship('Favorite_searches', backref='statistic_items')


    def __repr__(self):
        return '<query_id={} end_time={} final_price={}>'.format(self.query_id, self.end_time, self.final_price)
