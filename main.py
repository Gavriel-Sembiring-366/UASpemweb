import os
from flask import *
from flask_sqlalchemy import SQLAlchemy
# from flask_migrate import Migrate

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Inputs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nama_mesin = db.Column(db.Text(200), nullable=False)
    jenis_rusak = db.Column(db.Text(200), nullable=False)

    def __init__(self,nama_mesin,jenis_rusak):
        self.nama_mesin = nama_mesin
        self.jenis_rusak = jenis_rusak

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
    if request.method == "POST":

        mesin = request.form.get('mesin')
        jenis = request.form.get('jenis')

        kerusakan = Inputs(mesin, jenis)
        all_kerusakan = Inputs.query.all()
        print(all_kerusakan)
        
        try:
            db.session.add_all(kerusakan)
            db.session.commit()
            return redirect("dashboard")
        except:
            return "There Is an issue adding it"
    else:
        tasks = Inputs.query.order_by(Inputs.id).all()
        return render_template('dashboard.html', tasks=tasks)


if __name__ == '__main__':
    app.run()
