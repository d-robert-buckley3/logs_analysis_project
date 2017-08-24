# Logs Analysis Project
This is the course project for SQL at Udacity (nd004) on log analysis and reporting.  The Python script queries the 'news' database via the psycopg2 module and generates table style reports based on the results of that query.  The provided database is a simulation of a blog and includes authors, articles and an http log.  Three queries have been provided as examples (and to satisfy the assignment) within the main script:

1. What are the most popular 3 articles of all time?
2. Who are the most popular article authors of all time?
3. On which days did more than 1% of requests lead to errors?

## Installing the database

The main script was designed to be run with the provided database available here:

https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip

This database can be installed manually from the zip archive linked above.  To install the database, extract the contents of the .zip file into a folder and execute the .sql script provided using the 'psql' command line tool like so:

~~~~
psql -d news -f news_data.sql
~~~~

The system will need to have PostgreSQL installed and the daemon running.

## Installing the VM and Vagrant

Alternatively, a VM can be installed and launched via the Vagrant tool from VirtualBox.  Instructions on its installation can be found here:

https://classroom.udacity.com/nanodegrees/nd004/parts/8d3e23e1-9ab6-47eb-b4f3-d5dc7ef27bf0/modules/bc51d967-cb21-46f4-90ea-caf73439dc59/lessons/5475ecd6-cfdb-4418-85a2-f2583074c08d/concepts/14c72fe3-e3fe-4959-9c4b-467cf5b7c3a0

Be aware, I had some difficulty getting this method to work in my Ubuntu 16.04 system.  My system dual boots with Windows 10 and has SecureBoot enabled in UEFI.  This creates a signature problem for the keys used with the driver installed by VirtualBox.  I found a solution here:

https://askubuntu.com/questions/900118/vboxdrv-sh-failed-modprobe-vboxdrv-failed-please-use-dmesg-to-find-out-why

I created the keys and script described in the article linked above.  Any time VirtualBox complains that it cannot load the driver ('modprobe vboxdrv' fails) I reboot, switch to root access and run the script.  That would fix the problem.

Also, don't forget to enable Virtualization in your system's BIOS/UEFI firmware (like I did!).

I'm considering making my own Docker image to run the database.  We shall see.

## Running the script

To run this script and generate the report:

~~~~shell
python3 newsreports.py
~~~~

The script creates a log generator object which is used to add sections to a report.  Each section is created by providing it with a valid query for the 'news' database and a message to display as a title for the section.  The generator object will then query the database, format the results into a nice looking table, and append it to the running report text.  The script then calls the .dump_report() function to print the output to the console.

## Views

The script makes use of the following views.  Below are their names and the 'create view' statements used to create them. The CREATE VIEW statements can be executed in the psql tool manually.  However, it's easiest to install them using the provided script with the psql tool like so:

~~~~shell
psql -d news -f create_views.sql
~~~~

### error_counts

~~~~sql
create view error_counts as
select time::date as day, count(*) as requests,
count(case when status != '200 OK' then 1 end) as errors
from log
group by day;
~~~~

### top_3_articles

~~~~sql
create view top_articles as (
select path, count(*) as hits from log
where status = '200 OK' and path != '/'
group by path
order by hits desc;
~~~~
