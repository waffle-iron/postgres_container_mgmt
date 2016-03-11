#!/usr/bin/python
import os
import optparse
import sys
import time

docker = '/usr/bin/docker'
backups = '/var/db-backups/'
aws = '/usr/local/bin/aws'
bucket = "s3://fredhutch-postgres-backups"

t = time.localtime()
ts = "%s-%02d-%02d_%02d-%02d-%02d" % (t[0], t[1], t[2], t[3], t[4], t[5]) 

def main():
    print("\nDBaaS Backups for %s" % time.asctime())
    print("-" * 50)
    dbs = []
    try:
        res = os.popen("%s ps -q" % docker).readlines()
        for con in res:
            con = con.strip()
            env = os.popen("%s inspect --format '{{ index (index .Config.Env) }}' %s" % (docker, con)).read()
            labels = os.popen("%s inspect --format '{{.Config.Labels}}' %s" % (docker, con)).read()
            if 'DBaaS:true' in labels:
                name = [name for name in env.split() if 'POSTGRES_DB' in name][0].split('=')[1]
                user = [user for user in env.split() if 'POSTGRES_USER' in user][0].split('=')[1]
                try:
                    os.popen("%s exec -ti %s pg_dump --dbname %s --username %s --clean --create > %s/%s_%s.sql" % \
                             (docker, name, name, user, backups, name, ts))
                except Exception, e:
                    print("Error: problem backuping up %s: message: %s" % (name, e))

                print("Dumping  %s DB (%s/%s_%s.sql)" % (name, backups, name, ts))
    except Exception, e:
        print("An errort occured: %s" % e)
        sys.exit(99)

    # send the DB dumps offsite
    offsite_backup()



def offsite_backup():
    """Sends the DB Dumps to an S3 bucket"""
    print("\nSending backups to the Cloud (%s)" % bucket)
    print("-" * 50)
    try:
        out = os.popen("\n%s s3 sync %s %s" % (aws, backups, bucket)).readlines()
        for log in out:
            log = log.split("../../..")[1].replace('to', '-->').strip()
            print(log)
    except Exception, e:
        print("Error: problem sending backups to the cloud: %s" % e)
        sys.exit(100)

if __name__ == "__main__":    
    main()
