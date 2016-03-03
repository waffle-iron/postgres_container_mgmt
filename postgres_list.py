#!/usr/bin/python
import os
import optparse
import sys

docker = '/usr/bin/docker'

def main():
    dbs = []
    try:
        res = os.popen("%s ps -a -q" % docker).readlines()
        print("%-15s %-15s %-10s %-7s %-15s %-25s %s" % ("container_name", "db_name", "username", "port", "owner", "contact", "status"))
        for con in res:
            con = con.strip()
            env = os.popen("%s inspect --format '{{ index (index .Config.Env) }}' %s" % (docker, con)).read()
            labels = os.popen("%s inspect --format '{{.Config.Labels}}' %s" % (docker, con)).read()
            if 'DBaaS:true' in labels:
                port = os.popen("%s inspect --format '{{ index (index .NetworkSettings.Ports \"5432/tcp\") 0 }}' %s" % (docker, con)).read()
                port = port.replace('HostIp:0.0.0.0','').replace('map[','').replace(']','').replace('HostPort:','').strip()
                name = [name for name in env.split() if 'POSTGRES_DB' in name][0].split('=')[1]
                user = [user for user in env.split() if 'POSTGRES_USER' in user][0].split('=')[1]
                owner = [owner for owner in labels.split() if 'OWNER' in owner][0].split(':')[1].replace("]","")
                contact = [contact for contact in labels.split() if 'CONTACT' in contact][0].split(':')[1].replace(']','')
                status = os.popen("%s ps --format '{{.Status}}' --filter \"name=%s\"" % (docker, name)).read().strip()
                print("%-15s %-15s %-10s %-7s %-15s %-25s %s" % (name, name, user, port, owner, contact, status))
    except Exception, e:
        print("An errort occured: %s" % e)

if __name__ == "__main__":    
    main()
