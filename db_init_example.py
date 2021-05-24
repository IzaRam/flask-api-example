from api import db
from api.models import User, PersonalInfo, Address

db.drop_all()
db.create_all()

user_example = User(username='maria', email='maria@email.com')
db.session.add(user_example)
db.session.commit()

personal_infos_example = PersonalInfo(first_name='Maria', last_name='Silva', birth_date='1990-03-21', user_id=user_example.id)
db.session.add(personal_infos_example)

address_example = Address(address="Rua A", city="Rio de Janeiro", state='RJ', country='Brazil', postal_code='32415', user_id=user_example.id)
db.session.add(address_example)

db.session.commit()
