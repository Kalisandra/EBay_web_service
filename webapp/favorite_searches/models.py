from sqlalchemy import ForeignKey

from webapp.model import db


class Favorite_searches(db.Model):
    query_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey('user.id'), nullable=False)
    query_name = db.Column(db.String(50), nullable=False)
    user_query = db.Column(db.String(100), nullable=False)
    chosen_categoryid = db.Column(db.Integer, nullable=False)
    filter_request = db.Column(db.String(200), nullable=False)
    date_of_creation = db.Column(db.DateTime, nullable=False)


    def __repr__(self):
        return '<user_id={} query={} filter_request={}>'.format(self.user_id, self.query, self.filter_request)