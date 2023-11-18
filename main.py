import os
from flask import *
from flask_sqlalchemy import SQLAlchemy
import datetime
# from flask_migrate import Migrate

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(
    basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)

class Inputs(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    id_mesin = db.Column(db.Text(200), nullable=False)
    jenis_pekerjaan = db.Column(db.Text(200), nullable=False)
    bagian = db.Column(db.Text(200), nullable=False)
    tanggal_lapor = db.Column(db.Date, nullable=False)
    jam_lapor = db.Column(db.Time, nullable=False)

    def __init__(self, id_mesin, jenis_pekerjaan, bagian, tanggal_lapor, jam_lapor):
        self.id_mesin = id_mesin
        self.jenis_pekerjaan = jenis_pekerjaan
        self.bagian = bagian
        self.tanggal_lapor = tanggal_lapor
        self.jam_lapor = jam_lapor

    def __repr__(self):
        return f"Task added Succesfullys {self.nama_mesin}"


@app.route('/')
def login():
    return render_template('login.html')


@app.route('/', methods=['GET', 'POST'])
def welcome():
    username = request.form.get('username')
    password = request.form.get('password')

    if username == 'user' and password == 'password':
        return redirect(url_for("dashboard"))
    else:
        return render_template('login.html')


@app.route('/dashboard')
def dashboard():
    equipments = Inputs.query.all()
    return render_template('dashboard.html', equipments=equipments)


@app.route('/dashboard', methods=['GET', 'POST'])
def masuk():

    id_mesin = request.form.get('id_mesin')
    jenis_pekerjaan = request.form.get('jenis_pekerjaan')
    bagian = request.form.get('bagian')
    tanggal_lapor = request.form.get('tanggal_lapor')
    jam_lapor = request.form.get('jam_lapor')

    tanggal = datetime.datetime.strptime(tanggal_lapor, '%Y-%m-%d').date()
    jam = datetime.datetime.strptime(jam_lapor, '%H:%M').time()
    kerusakan = Inputs(id_mesin, jenis_pekerjaan, bagian, tanggal, jam)

    try:
        with app.app_context():
            db.session.add(kerusakan)
            db.session.commit()

        equipments = Inputs.query.all()

        return render_template('dashboard.html', equipments=equipments)

    except:
        return "There Is an issue adding it"


if __name__ == '__main__':
    app.run(debug=True)
