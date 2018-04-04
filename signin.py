from flask import Flask, render_template, request, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
app.config['SECRET_KEY'] = "random string"
SQLALCHEMY_TRACK_MODIFICATIONS = False

db = SQLAlchemy(app)

class users(db.Model):
    id = db.Column('user_id', db.Integer, primary_key = True)
    email = db.Column(db.String(100))
    username = db.Column(db.String(50))
    password = db.Column(db.String(200)) 
    DOB = db.Column(db.String(10))

def __init__(self, email, username, password, DOB):
   self.email = email
   self.username = username
   self.password = password
   self.DOB = DOB

@app.route('/', methods = ['GET', 'POST'])
def sign_up():
    print(request.method)
    if request.method == 'POST':
        if not request.form['email'] or not request.form['username'] or not request.form['password'] or not request.form['DOB']:
            flash('Please enter all the fields', 'error')
        else:
            user = users(email = request.form['email'], username = request.form['username'], password = request.form['password'], DOB = request.form['DOB'])
            db.session.add(user)
            db.session.commit()
    return render_template('home.html')

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)