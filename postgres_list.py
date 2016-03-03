#!/usr/bin/python
import os
import optparse
import sys

docker = '/usr/bin/docker'

def main():
    dbs = []
    try:
        res = os.popen("%s ps -a -q" % docker).readlines()
        print("container_name, db_name, username, port, owner, contact")
        for con in res:
            con = con.strip()
            env = os.popen("%s inspect --format '{{ index (index .Config.Env) }}' %s" % (docker, con)).read()
            if 'DBaaS=true' in env:
                port = os.popen("%s inspect --format '{{ index (index .NetworkSettings.Ports \"5432/tcp\") 0 }}' %s" % (docker, con)).read()
                port = port.split(':')[2].replace(']','').strip()
                name = [name for name in env.split() if 'POSTGRES_DB' in name][0].split('=')[1]
                user = [user for user in env.split() if 'POSTGRES_USER' in user][0].split('=')[1]
                owner = [owner for owner in env.split() if 'OWNER' in owner][0].split('=')[1]
                contact = [contact for contact in env.split() if 'CONTACT' in contact][0].split('=')[1]
                print("%s, %s, %s, %s, %s, %s" % (name, name, user, port, owner, contact))
    except Exception, e:
        print("An errort occured: %s" % e)

if __name__ == "__main__":    
    main()
