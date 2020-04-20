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
    user = relationship('User', backref='favorite_searches')


    def __repr__(self):
        return '<user_id={} query={} filter_request={}>'.format(self.user_id, self.user_query, self.filter_request)