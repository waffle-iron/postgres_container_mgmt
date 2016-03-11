#!/usr/bin/python
import os
import time
from flask import Flask, render_template, request, url_for

app = Flask(__name__)
app.config['DEBUG'] = True

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/list/')
def list():
    dbs = os.popen('./postgres_list.py').read().strip()
    return render_template('dblist.html', dbs=dbs)

@app.route('/cloudbackups/')
def cloudbackups():
    backups = os.popen('aws s3 ls s3://fredhutch-postgres-backups').read().strip()
    return render_template('cloudbackups.html', backups=backups)

@app.route('/create/')
def create_form():
    return render_template('create_form.html')

@app.route('/created/', methods=['POST'])
def created():
    dbname=request.form['dbname'].replace(';','').replace('&','').strip()
    dbuser=request.form['dbuser'].replace(';','').replace('&','').strip()
    dbuserpass = request.form['dbuserpass'].replace(';','').replace('&','').strip()
    memlimit = request.form['memlimit'].replace(';','').replace('&','').strip()
    owner = request.form['owner'].replace(';','').replace('&','').strip()
    contact = request.form['contact'].replace(';','').replace('&','').strip()
    description = request.form['description'].replace(';','').replace('&','').strip()
    result = createdb(dbname, dbuser, dbuserpass, owner, description, contact, memlimit).strip()
    return render_template('created.html', dbname=dbname, dbuser=dbuser, dbuserpass=dbuserpass, memlimit=memlimit, owner=owner, contact=contact, description=description, result=result)

def createdb(name, dbuser, passwd, owner, description, contact, memlimit):
    docker = '/usr/bin/docker'
    image = 'fredhutch/postgres:9.5'
    try:
        os.popen("%s run -d -P --name %s --restart on-failure -e POSTGRES_USER=%s \
                 -e POSTGRES_DB=%s -e POSTGRES_PASS=%s -l OWNER=%s -l DESCRIPTION=\"%s\" \
                 -l DBaaS=true -l CONTACT=%s -m=%s  %s 2>/dev/null" % \
                 (docker, name, dbuser, name, passwd, owner, description, contact, memlimit, image))
        time.sleep(2)
        res = os.popen("%s ps -l --format 'table {{.ID}}\t{{.Names}}\t{{.Ports}}\t{{.Status}}'" % docker).read()
        return res 
    except Exception, e:
        return "An errort occured: %s" % e

# Run the app :)
if __name__ == '__main__':
  app.run( 
        host="0.0.0.0",
        port=int("1776")
  )
