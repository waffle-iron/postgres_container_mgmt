## PostgresSQL Container Mangement for DBaaS

### Command Line Documentation

#### Creating New Databases

To create a new database container use the postgres_create.py script as follows:

```
 ./postgres_create.py --help
Usage: postgres_create.py --name=<container/dbname> --dbuser=<username> --password=<password> --owner=<owner> --description='<description>' [--memlimit=<num><m/g> (optional)]

Options:
  --version             show program's version number and exit
  -h, --help            show this help message and exit
  -n NAME, --name=NAME  Set the name of the container and database
  -u DBUSER, --dbuser=DBUSER
                        Set the database username
  -p PASSWD, --password=PASSWD
                        Set the dbuser's password
  -o OWNER, --owner=OWNER
                        Set the owner of the container/db
  -c CONTACT, --contact=CONTACT
                        Set database contact (email)
  -d DESCRIPTION, --description=DESCRIPTION
                        Set the descriptoin of the container/db
  -m MEMLIMIT, --memlimit=MEMLIMIT
                        Set the maximum RAM that the containter can use.
                        Specify "m" for MB and "g" for GB - ex: 512m, 2g
                        (optional) - defaults to 2g if no limit provided

```

For example, to create a PostgresSQL 9.5 database container with the following attributes:

- **Container name / DB Name:**  scicomp_demo
- **DB username:** scicomp
- **DB password:** demopassword01
- **Owner:** ad/scicomp
- **Contact:** rmcdermo@fredhutch.org
- **Description:** "Demo DB for scicomp"
- **Mem limit:** 768MB of RAM

You would use the following command:

```
./postgres_create.py --name scicomp_demo \
                     --dbuser scicomp \
                     --password demopassword01 \
                     --owner ad/scicomp \
                     --contact rmcdermo@fredhutch.org \
                     --description "Demo DB for SciComp" \
                     --memlimit 768m
```

The output of the command confirming that the DB was created would look like the following:

```
CONTAINER ID        NAMES               PORTS                     STATUS
288453e3c82a        scicomp_demo        0.0.0.0:32792->5432/tcp   Up Less than a second
```
The above output means that the database container was sucessfully created and is listing on TCP port 32792 on the DBaaS host for client connections.

#### Listing the DBaaS Containers

To see a list of all the DBaaS containers running with the details of the containers, run the following command:

```
./postgres_list.py
```

The output of the above command should look something like the following:

```
container_name  container_id  db_name         username   port   mem_limit size       owner           contact                   status
maxquant4       9b6e30304b28  maxquant4       maxquant   32812  2048MB    2.5MB      vi/paulovich_a  clin@fredhutch.org        Up 3 hours
maxquant3       24ed1a9200e7  maxquant3       maxquant   32811  2048MB    600KB      vi/paulovich_a  clin@fredhutch.org        Up 3 hours
maxquant2       32922e049ce5  maxquant2       maxquant   32810  768MB     63MB       vi/paulovich_a  clin@fredhutch.org        Up 4 hours
maxquant        389a1941130f  maxquant        maxquant   32804  768MB     1.3MB      vi/paulovich_a  clin@fredhutch.org        Up 4 hours
jimmy           87795f7b365d  jimmy           maxquant   32803  768MB     117.4MB    vi/paulovich_a  clin@fredhutch.org        Up 4 hours
scicomp_demo    288453e3c82a  scicomp_demo    scicomp    32792  None      5.33GB     ad/scicomp      rmcdermo@fredhutch.org    Up 28 hours
demodb01        18d67e487b68  demodb01        demouser   32791  None      63GB       None            demo@fredhutch.org        Up 29 hours
trump_db        18eb91dfc2de  trump_db        trump      32790  None      17.75MB    tt/trump        trump@trump.com           Up 29 hours
turdblossom     a3bc3dadbf6c  turdblossom     turd       32789  None      254.54MB   cr/turd         turd@fredhutch.com        Up 29 hours
cpas            6a706cbec97b  cpas            cpas       32787  None      563MB      sr/proteomics   gafking@fredhutch.org     Up 30 hours
it_budget       1ce047c36987  it_budget       budget     32786  None      639MB      ad/finance      mrmoney@fredhutch.org     Up 30 hours
genomic_stuff   d65b81b75e37  genomic_stuff   genoics    32785  None      989KB      sr/genomic      jdelrow@fredhutch.org     Up 30 hours
oncoscape_brain 58972326c5c6  oncoscape_brain oncoscape  32784  None      777KB      hb/sttr         rmcdermo@fredhutch.org    Up 30 hours
testlabel       01940f0c27e6  testlabel       test       32783  None      17.55MB    ad/scicomp      rmcdermo@fredhutch.org    Up 30 hours
```

#### Database Backups

To backup all running DBaaS postgres database containers and send the backups to the cloud (S3 bucket), run the following command on your DBaaS host:

```
./postgres_backup.py
```

The above command will perform a DB dump of all running database containers and place the backups in '/var/db-backups'. In addition to local backups, this will also send the backups to and AWS S3 stoage bucket at s3://fredhutch-postgres-backups. The output of this command will look like this:

```
DBaaS Backups for Thu Mar  3 16:28:32 2016
--------------------------------------------------
Dumping  scicomp_demo DB (/var/db-backups//scicomp_demo_2016-03-03_16-28-32.sql)
Dumping  demodb01 DB (/var/db-backups//demodb01_2016-03-03_16-28-32.sql)
Dumping  trump_db DB (/var/db-backups//trump_db_2016-03-03_16-28-32.sql)
Dumping  turdblossom DB (/var/db-backups//turdblossom_2016-03-03_16-28-32.sql)
Dumping  cpas DB (/var/db-backups//cpas_2016-03-03_16-28-32.sql)
Dumping  it_budget DB (/var/db-backups//it_budget_2016-03-03_16-28-32.sql)
Dumping  genomic_stuff DB (/var/db-backups//genomic_stuff_2016-03-03_16-28-32.sql)
Dumping  oncoscape_brain DB (/var/db-backups//oncoscape_brain_2016-03-03_16-28-32.sql)
Dumping  testlabel DB (/var/db-backups//testlabel_2016-03-03_16-28-32.sql)

Sending backups to the Cloud (s3://fredhutch-postgres-backups)
--------------------------------------------------
/var/db-backups/trump_db_2016-03-03_16-28-32.sql --> s3://fredhutch-postgres-backups/trump_db_2016-03-03_16-28-32.sql
/var/db-backups/testlabel_2016-03-03_16-28-32.sql --> s3://fredhutch-postgres-backups/testlabel_2016-03-03_16-28-32.sql
/var/db-backups/turdblossom_2016-03-03_16-28-32.sql --> s3://fredhutch-postgres-backups/turdblossom_2016-03-03_16-28-32.sql
/var/db-backups/scicomp_demo_2016-03-03_16-28-32.sql --> s3://fredhutch-postgres-backups/scicomp_demo_2016-03-03_16-28-32.sql
/var/db-backups/it_budget_2016-03-03_16-28-32.sql --> s3://fredhutch-postgres-backups/it_budget_2016-03-03_16-28-32.sql
/var/db-backups/cpas_2016-03-03_16-28-32.sql --> s3://fredhutch-postgres-backups/cpas_2016-03-03_16-28-32.sql
/var/db-backups/genomic_stuff_2016-03-03_16-28-32.sql --> s3://fredhutch-postgres-backups/genomic_stuff_2016-03-03_16-28-32.sql
/var/db-backups/oncoscape_brain_2016-03-03_16-28-32.sql --> s3://fredhutch-postgres-backups/oncoscape_brain_2016-03-03_16-28-32.sql
/var/db-backups/demodb01_2016-03-03_16-28-32.sql --> s3://fredhutch-postgres-backups/demodb01_2016-03-03_16-28-32.sql
```

### Web Interface

A very basic web console if provided. To run it you'll need Python 2.7 and Flask installed (apt-get install -y python-flask). To run the web console just execute the "webui.py" script and point a web browser at "http://servername:1776" (replace "servername" with the name of the system were you are running the script.

If everything is working, you'll be presended with the following web page:

![index](../roberts_branch/images/index.png?raw=true)

To get a list of the current database conatiners running on the system, click on the "List Database Containers" link, which should result in something similar to the following:

![list](../roberts_branch/images/list.png?raw=true)

To create a new database container, click on the "Create a Database Container" link, which will present you with a form similar to the following:

![create](../roberts_branch/images/create.png?raw=true)

Fill out the form **completely** and click "Submit" which will result in a page similar to the following being displayed:

![created](../roberts_branch/images/created.png?raw=true)

To view an inventory of database backup archives that are currently backed up to Amazon S3, click on the "List Database Backup Archives" link. This will provide you will a backup inventory similar to the page shown below:

![backups](../roberts_branch/images/backups.png?raw=true)
