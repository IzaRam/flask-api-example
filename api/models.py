from api import db


class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    person_id = db.Column(db.Integer, db.ForeignKey('PersonalInfo.person_id'))
    person = db.relationship("PersonalInfo", back_populates="User")
    address_id = db.Column(db.Integer, db.ForeignKey('Address.address_id'))
    address = db.relationship("Address", back_populates="User")

    def __repr__(self):
        return '<User %r>' % self.username


class PersonalInfo(db.Model):
    person_id = db.Column(db.Integer, primary_key=True)
    fist_name = db.Column(db.String(120), nullable=False)
    last_name = db.Column(db.String(120), nullable=False)
    birth_date = db.Column(db.String(50), nullable=False)
    user = db.relationship("User", back_populates="PersonalInfo", uselist=False)

    def __repr__(self):
        name = self.fist_name + " " + self.last_name
        return '<Name %r>' % name

class Address(db.Model):
    address_id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(255), nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    country= db.Column(db.String(120), nullable=False)
    postal_code = db.Column(db.String(120), nullable=False)
    user = db.relationship("User", back_populates="Address", uselist=False)
