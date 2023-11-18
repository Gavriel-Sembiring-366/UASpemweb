from main import app, Inputs
from main import db
import datetime

# with app.app_context():
#     db.drop_all()

# app.app_context().push()
# db.create_all()

with app.app_context():
     kerusakan = Inputs("idedacsdaswd", "jenis", "bagaian", datetime.date(2015,3,12), datetime.time(9,10,23))
     db.session.add(kerusakan)

     equipments = Inputs.query.all()
     print(equipments)