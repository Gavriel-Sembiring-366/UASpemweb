
from main import app, Inputs
from main import db

app.app_context().push()
db.create_all()
