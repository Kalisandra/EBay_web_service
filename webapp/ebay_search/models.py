from webapp.model import db


class EbayCategories(db.Model):
    __tablename__ = 'ebay_categories'
    id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column('categoryname', db.String(50), nullable=False)
    category_level = db.Column('categorylevel', db.Integer, nullable=False)
    category_id = db.Column(
        'categoryid', db.Integer, unique=True, nullable=False)
    categoryparent_id = db.Column('categoryparentid', db.Integer)

    def __repr__(self):
        return '<category_name={} category_id={}>'.format(
            self.category_name, self.category_id)
