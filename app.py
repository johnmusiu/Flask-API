"""import classes required"""
from functools import wraps
from flask import Flask, render_template, redirect, url_for, request, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.secret_key = "my precious"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flaskAPI.db'

#create SQLAlchemy OBJ
db = SQLAlchemy(app)


#import db tables(models)
from models import *

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash("You need to login to access page!")
        return wrap

@app.route('/')
@login_required
def home():
    ''' '''
    # if session.get('logged_in'):
    return "Hello, world"
    # else:
    # return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    ''' '''
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = "Invalid credentials, please try again!"
        else:
            session['logged_in'] = True
            flash("Login success!")
            return redirect(url_for('home'))
    return render_template('login.html', error=error)

@app.route('/logout')
@login_required
def logout():
    ''' Logs user out, deletes session data'''
    session.pop('logged_in', None)
    flash("Logged out successfully!")
    return redirect(url_for('home'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    ''' '''
    

if __name__ == '__main__':
    app.run(debug=True)