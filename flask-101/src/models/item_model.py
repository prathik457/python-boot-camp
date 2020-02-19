from src.models import db

class ItemModel(db.Model):
    __tablename__ = 'items'
    _id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(150), unique=True, nullable=False)
    description = db.Column(db.String(300))
    price = db.Column(db.Float(precision=2), nullable=False)

    def __init__(self, name, description, price):
        self.name = name
        self.description = description
        self.price = price

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get_items(self):
        return self.query.all()
    
    @classmethod
    def get_item_by_name(cls, name):
        item = cls.query.filter_by(name=name).first()
        return item
    
    def json(self):
        return {'name': self.name, 'description': self.description, 'price': self.price}
