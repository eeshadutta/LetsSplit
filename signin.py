from flask import Flask, render_template, request, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug import secure_filename
from wtforms import StringField
from wtforms.validators import DataRequired
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
app.config['SECRET_KEY'] = "random string"
app.config['UPLOAD_FOLDER'] = "./profile_pics"

SQLALCHEMY_TRACK_MODIFICATIONS = False

DB = SQLAlchemy(app)

class users(DB.Model):
    __searchable__ = ['name']
    id = DB.Column('user_id', DB.Integer, primary_key = True)
    email = DB.Column(DB.String(100))
    username = DB.Column(DB.String(50))
    password = DB.Column(DB.String(200))
    DOB = DB.Column(DB.String(10))
    profile_pic = DB.Column(DB.String(100))
    name = DB.Column(DB.String(100))
    bio = DB.Column(DB.String(200))

    def __init__(self, email, username, password, DOB ,profile_pic_url, name, bio):
        self.email = email
        self.username = username
        self.password = password
        self.DOB = DOB
        self.profile_pic = profile_pic_url
        self.name = name
        self.bio = bio

class friends(DB.Model):
    id = DB.Column('user_id', DB.Integer, primary_key = True)
    username = DB.Column(DB.String(50))
    friends = DB.Column(DB.String(8000))
    
    def __init__(self, username, friends=''):
        self.username = username
        self.friend = ''
        

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
                    img = request.files['profile_pic']
                    img.save(secure_filename(img.filename))
                    #os.makedirs("./profile_pics", exist_ok=True)
                    os.system("mv " + secure_filename(img.filename) + " ./static/")
                    user = users(email = request.form['email'], username = request.form['username'], password = request.form['password'], DOB = request.form['DOB'], profile_pic_url = secure_filename(img.filename), name = request.form['name'], bio = request.form['bio'])
                    user_friends = friends(username=request.form['username'])
                    DB.session.add(user)
                    DB.session.add(user_friends)
                    DB.session.commit()
                    return redirect(url_for('profile_page', username=request.form['username']))
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


@app.route('/<username>/search/<query>', methods=['GET', 'POST'])
def search_results(username, query, message=None):
    url_dict = {}
    results = users.query.filter(users.username.startswith(query)).all()
    for x in results:
        url_dict[x.username] = x.profile_pic
    if not results:
        message = "Oops... No results found"
    if request.method == 'POST':
        if 'search' in request.form:
            return redirect(url_for('search_results', username=username, query=request.form['search_name']))
        if 'logout' in request.form:
            return redirect(url_for('sign_up'))
        if 'add_friends' in request.form:
            x = friends.query.filter_by(username=username).first()
            print(request.form['friend_to_be_added'])
            z = x.friend
            x.friend = z + request.form['friend_to_be_added'] + ','
            DB.session.commit()

    return render_template('search_results.html', username=username, results=results, message=message, profile_pic_dict=url_dict)


@app.route('/<username>', methods=['GET', 'POST'])
def profile_page(username):
    print(username)
    user = users.query.filter_by(username=username).first()
    #print(user.profile_pic)
    if request.method == 'POST':

        if 'search' in request.form:
            return redirect(url_for('search_results', username=username, query=request.form['search_name']))
        if 'logout' in request.form:
            return redirect(url_for('sign_up'))
        

    return render_template('profile_page.html', username=username, user=user)

if __name__ == '__main__':
    DB.create_all()
    app.run(debug=True)
