#!/usr/bin/python
import os
import optparse
import sys

docker = '/usr/bin/docker'
image = 'fredhutch/postgres'
backup_dir = '/var/db_backups'

def createdb(name, dbuser, passwd, owner, description, contact):
    try:
        os.popen("%s run -d -P --name %s --restart on-failure -e POSTGRES_USER=%s \
                 -e POSTGRES_DB=%s -e POSTGRES_PASS=%s -l OWNER=%s -l DESCRIPTION=\"%s\" \
                 -l DBaaS=true -l CONTACT=%s %s 2>/dev/null" % \
                 (docker, name, dbuser, name, passwd, owner, description, contact, image)) 
        res = os.popen("%s ps -l" % docker).read()
        print(res)
    except Exception, e:
        print("An errort occured: %s" % e)

def main():
    p = optparse.OptionParser(usage="usage: %prog --name=<container/dbname> --dbuser=<username> --password=<password> --owner=<owner> --description='<description>'", version="%prog 1.0")
    p.add_option('-n', '--name',  action='store', type='string', dest='name', help='Set the name of the container and database')
    p.add_option('-u', '--dbuser',  action='store', type='string', dest='dbuser', help='Set the database username')
    p.add_option('-p', '--password',  action='store', type='string', dest='passwd', help='Set the dbuser\'s password')
    p.add_option('-o', '--owner',  action='store', type='string', dest='owner', help='Set the owner of the container/db')
    p.add_option('-c', '--contact',  action='store', type='string', dest='contact', help='Set database contact (email)')
    p.add_option('-d', '--description',  action='store', type='string', dest='description', help='Set the descriptoin of the container/db')
    opt, args = p.parse_args()

    if len(sys.argv) < 5:
        p.error('use --help for usage information.')
    createdb(opt.name, opt.dbuser, opt.passwd, opt.owner, opt.description, opt.contact)


if __name__ == "__main__":    
    main()
