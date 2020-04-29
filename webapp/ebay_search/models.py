from webapp.model import db


class Ebay_Categories(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    categoryname = db.Column(db.String(50), nullable=False)
    categorylevel = db.Column(db.Integer, nullable=False)
    categoryid = db.Column(db.Integer, unique=True, nullable=False)
    categoryparentid = db.Column(db.Integer)

    def __repr__(self):
        return '<categoryname={} categoryid={}>'.format(
            self.categoryname, self.categoryid)
