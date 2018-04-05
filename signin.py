from flask import Flask, render_template, request, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
app.config['SECRET_KEY'] = "random string"
SQLALCHEMY_TRACK_MODIFICATIONS = False

DB = SQLAlchemy(app)

class users(DB.Model):
    id = DB.Column('user_id', DB.Integer, primary_key = True)
    email = DB.Column(DB.String(100))
    username = DB.Column(DB.String(50))
    password = DB.Column(DB.String(200))
    DOB = DB.Column(DB.String(10))

    def __init__(self, email, username, password, DOB):
        self.email = email
        self.username = username
        self.password = password
        self.DOB = DOB

@app.route('/', methods = ['GET', 'POST'])
def sign_up(message=None):
    if request.method == 'POST':
        if 'SignUp' in request.form:
            if not request.form['email'] or not request.form['username'] or not request.form['password'] or not request.form['DOB'] or not request.form['passwordconfirm']:
                flash('Please enter all the fields', 'error')
            else:
                x = users.query.filter_by(username=request.form['username']).first()
                if request.form['password'] != request.form['passwordconfirm']:
                    message = 'Passwords Don\'t Match'
                if x is None:
                    user = users(email = request.form['email'], username = request.form['username'], password = request.form['password'], DOB = request.form['DOB'])
                    DB.session.add(user)
                    DB.session.commit()
                else:
                    message = 'Username already taken'

        elif 'SignIn' in request.form:
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
                    return redirect(url_for('profile_page', username=request.form['username']))
                elif str(x.password) != str(request.form['password']):
                    message = "Incorrect Password"

    return render_template('home.html', message=message)


@app.route('/<username>', methods=['GET', 'POST'])
def profile_page(username):
    if request.method == 'POST':
        if 'logout' in request.form:
            return redirect(url_for('sign_up'))
            
    return render_template('profile_page.html', username=username)
    
if __name__ == '__main__':
    DB.create_all()
    app.run(debug=True)
