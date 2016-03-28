#!/usr/bin/python
import os
import random
import time
import postgres_create 
import ad_auth
from flask import Flask, render_template, request, url_for, session, redirect

app = Flask(__name__)
app.secret_key = 'secret'
app.config['DEBUG'] = True

@app.route('/index')
def index():
    if session['logged_in']:
        return render_template('index.html')
    else:
        return redirect(url_for('login'))

@app.route('/login', methods=['GET','POST'])
def login():
    session['logged_in']=False
    if request.method == 'POST':
        username = request.form['username'] + '@fhcrc.org'
        password = request.form['password']

        DCs = ['dc42.fhcrc.org','dc152.fhcrc.org']
        random.shuffle(DCs)
        for DC in DCs:
            auth = ad_auth.fhcrcauth(username,password,DC)
            if auth == 2 or auth == 3:
                continue
            elif auth == 1 or auth == 0:
                 break

        if auth == 1:
            session['logged_in']=True
            return redirect(url_for('index'))

        elif auth == 0:
            return "<h1>Error: Invalid Credentials</h1>"
		
        elif auth == 2:
            return "<h1>Error: Can't contact any domain controllers</h1>"

        else:
            return "<h1>Error: An unknown error occured attempting to validate your credentials</h1>"
    else:
        return render_template('login.html')


@app.route('/logout')
def logout():
	session['logged_in']=False
	return redirect(url_for('login'))

@app.route('/')
def first():
	session['logged_in']=False
	return redirect(url_for('index'))

@app.route('/list/')
def list():
    if session['logged_in']:
        dbs = os.popen('./postgres_list.py').read().strip()
        return render_template('dblist.html', dbs=dbs)
    else:
        return redirect(url_for('login'))

@app.route('/cloudbackups/')
def cloudbackups():
    if session['logged_in']:
        backups = os.popen('aws s3 ls s3://fredhutch-postgres-backups').read().strip()
        return render_template('cloudbackups.html', backups=backups)
    else:
        return redirect(url_for('login'))

@app.route('/create/')
def create_form():
    if session['logged_in']:
        return render_template('create_form.html')
    else:
        return redirect(url_for('login'))

@app.route('/created/', methods=['POST'])
def created():
    if session['logged_in']:
        dbname=request.form['dbname'].replace(';','').replace('&','').strip()
        dbuser=request.form['dbuser'].replace(';','').replace('&','').strip()
        dbuserpass = request.form['dbuserpass'].replace(';','').replace('&','').strip()
        memlimit = request.form['memlimit'].replace(';','').replace('&','').strip()
        owner = request.form['owner'].replace(';','').replace('&','').strip()
        contact = request.form['contact'].replace(';','').replace('&','').strip()
        description = request.form['description'].replace(';','').replace('&','').strip()
        result = postgres_create.createdb(dbname, dbuser, dbuserpass, owner, description, contact, memlimit).strip()
        return render_template('created.html', dbname=dbname, dbuser=dbuser, dbuserpass=dbuserpass, memlimit=memlimit, owner=owner, contact=contact, description=description, result=result)
    else:
        return redirect(url_for('login'))

# Run the app :)
if __name__ == '__main__':
  app.run( 
        host="0.0.0.0",
        port=int("1776"),
        ssl_context='adhoc'
  )
