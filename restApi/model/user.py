from restApi import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    password_hash = db.Column(db.String(64))
    email = db.Column(db.String(64),unique=True)

    def as_dict(self):
        return {c.name:getattr(self,c.name) for c in self.__table__.columns}