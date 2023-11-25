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

mesin_sucad = db.Table(
    'mesin_sucad',
    db.Column('mesin_id', db.String(50), db.ForeignKey('Mesin.id_mesin'), primary_key=True),
    db.Column('sucad_id', db.String(50), db.ForeignKey('SukuCadang.id_SukuCadang'), primary_key=True)
)

class Mesin(db.Model):
    __tablename__ = 'Mesin'
    id_mesin = db.Column(db.String(50), nullable=False, unique=True, primary_key=True, autoincrement=False)
    nama_mesin = db.Column(db.String(255), nullable=False)
    periode_cek_mesin = db.Column(db.String(50), nullable=False)
    sucad = db.relationship('SukuCadang', secondary=mesin_sucad, backref = 'suku_cadang')

    # Define the relationship with SukuCadang

    def __init__(self, id_mesin, periode_cek_mesin, nama_mesin):
        self.id_mesin = id_mesin
        self.nama_mesin = nama_mesin
        self.periode_cek_mesin = periode_cek_mesin

class SukuCadang(db.Model):
    __tablename__ = 'SukuCadang'
    id_SukuCadang = db.Column(db.String(50), nullable=False, unique=True, primary_key=True, autoincrement=False)
    nama_SukuCadang = db.Column(db.String(255), nullable=False)
    stok_minimum_SukuCadang = db.Column(db.String(50), nullable=False)
    stok_aktual_SukuCadang = db.Column(db.String(50), nullable=False)

    # Define the relationship with Mesin

    def __init__(self, id_SukuCadang, nama_SukuCadang, stok_minimum_SukuCadang, stok_aktual_SukuCadang):
        self.id_SukuCadang = id_SukuCadang
        self.nama_SukuCadang = nama_SukuCadang
        self.stok_minimum_SukuCadang = stok_minimum_SukuCadang
        self.stok_aktual_SukuCadang = stok_aktual_SukuCadang

class Kerusakan(db.Model):
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

# this for sending database info when rendering the html - DO NOT DELETE
@app.route('/dashboard')
def dashboard():
    equipments = Kerusakan.query.all()
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
    kerusakan = Kerusakan(id_mesin, jenis_pekerjaan, bagian, tanggal, jam)

    try:
        with app.app_context():
            db.session.add(kerusakan)
            db.session.commit()

        equipments = Kerusakan.query.all()

        render_template('dashboard.html', equipments=equipments)
        return redirect(url_for("dashboard"))

    except:
        return "There Is an issue adding it"


@app.route('/daftar_sucad')
def daftar_sucad_redirect():
    sucads = SukuCadang.query.all()
    return render_template('daftar_sucad.html', sucads=sucads)

@app.route('/daftar_sucad', methods=['GET', 'POST'])
def input_daftar_sucad():
    sucad_id = request.form.get('sucad_id')
    sucad_nama = request.form.get('sucad_nama')
    sucad_min_stok = request.form.get('sucad_min_stok')
    sucad_aktual_stok = request.form.get('sucad_aktual_stok')
    
    existed = SukuCadang.query.filter_by(id_SukuCadang=sucad_id).first()
    if existed:
        return 'Sucad ID already exists in the database'
    else:
        sucad = SukuCadang(sucad_id,sucad_nama,sucad_min_stok,sucad_aktual_stok)

        try:
            with app.app_context():
                db.session.add(sucad)
                db.session.commit()
        
            sucads = SukuCadang.query.all()
        
            render_template('daftar_sucad.html', sucads=sucads)
            return redirect(url_for("daftar_sucad_redirect"))
    
        except:
            return 'There is issue'



if __name__ == '__main__':
    app.run(debug=True)
