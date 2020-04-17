from webapp.model import db


class Favorite_searches(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    user_query = db.Column(db.String(100), nullable=False)
    chosen_categoryid = db.Column(db.Integer, nullable=False)
    categoryid = db.Column(db.Integer, unique=True, nullable=False)
    filter_request = db.Column(db.String(200), nullable=False)
    date_of_creation = db.Column(db.DateTime, nullable=False)


    def __repr__(self):
        return '<user_id={} query={} filter_request={}>'.format(self.user_id, self.query, self.filter_request)