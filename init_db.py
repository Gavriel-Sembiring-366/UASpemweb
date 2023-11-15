
from main import app, Inputs
from main import db

app.app_context().push()
db.create_all()

mesi12 = Inputs("ASUUUUU", "M")

db.session.add(mesi12)
db.session.commit()

print(mesi12.id)

all_mesin = Inputs.query.all()

print(all_mesin[40].nama_mesin)
