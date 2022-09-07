from crypt import methods
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.secret_key = "secret key"

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dbsite.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Data(db.Model):
    id    = db.Column(db.Integer, primary_key = True)
    name  = db.Column(db.String(100))
    email = db.Column(db.String(100))
    phone = db.Column(db.String(100))

    def __init__(self, name, email, phone):
        self.name  = name
        self.email = email
        self.phone = phone



@app.route("/")
def index():
    
    all_data = Data.query.all()

    return render_template("index.html", all_data = all_data)


# -----------CREATE-----------
@app.route('/insert', methods=['POST'])
def insert():

    if request.method == 'POST':
        name  = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        
        my_data = Data(name, email, phone)
        db.session.add(my_data)
        db.session.commit()

        flash("Funcionário cadastrado com sucesso!")

        return redirect(url_for('index'))


# ------------READ------------

# -----------UPDATE-----------
@app.route('/update', methods=['GET', 'POST'])
def update():
    
    if request.method == 'POST':
        my_data = Data.query.get(request.form.get('id'))

        my_data.name  = request.form['name']
        my_data.email = request.form['email']
        my_data.phone = request.form['phone']

        db.session.commit()
        flash("Registro atualizado com sucesso!")

        return redirect(url_for('index'))


# -----------DELETE-----------
@app.route('/delete/<id>', methods=['GET', 'POST'])
def delete(id):
    my_data = Data.query.get(id)

    db.session.delete(my_data)
    db.session.commit()     

    flash("Registro deletado com sucesso!")

    return redirect(url_for('index'))



@app.route("/users/<user_name>")
def users(user_name):
    return render_template("users.html", user_name=user_name)





if '__name__' == '__main__':
    app.run()
