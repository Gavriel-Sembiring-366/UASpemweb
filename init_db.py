from main import db, app, Mesin, SukuCadang, Kerusakan

# with app.app_context():
#      db.drop_all()

#app.app_context().push()
#db.create_all()

# with app.app_context():

#     sucads = Kerusakan.query.all()
#     for sukad in sucads:
#         print(sukad)


with app.app_context():
    for i in range(1,16):
        asu = SukuCadang("ID SUCAD " + str(i), "Sucad " + str(i) , "minimum " + str(i), "aktual " + str(i))
        db.session.add(asu)
        db.session.commit()