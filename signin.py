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
def sign_up(message=None):
    if request.method == 'POST':
        if 'SignUp' in request.form:
            print(request.form)
            if not request.form['email'] or not request.form['username'] or not request.form['password'] or not request.form['DOB']:
                flash('Please enter all the fields', 'error')
            else:
                x = users.query.filter_by(username=request.form['username']).first()
                print(x)
                if x is None:
                    user = users(email = request.form['email'], username = request.form['username'], password = request.form['password'], DOB = request.form['DOB'])
                    db.session.add(user)
                    db.session.commit()
                    #print("HAHA")
                else:
                    message = 'Username already taken'

        elif 'SignIn' in request.form:
            print(request.form)
            if request.form['username'] is '':
                message = "Please Enter Username"
            elif not request.form['password']:
                message = "Please Enter Password"
            else : 
                x = users.query.filter_by(username=request.form['username']).first()
                if x is None:
                    message = "Incorrect Username"
                elif request.form['password'] is None:
                    message = 'Please Enter Password'            
                elif str(x.password) == str(request.form['password']) and x is not None:
                    print("Yay! Logged In")
                elif str(x.password) != str(request.form['password']):
                    message = "Incorrect Password"
                
    return render_template('home.html', message=message)

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)