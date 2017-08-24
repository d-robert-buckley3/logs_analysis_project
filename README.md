# Logs Analysis Project
This is the course project for SQL at Udacity (nd004) on log analysis and reporting.  The Python script queries the 'news' database via the psycopg2 module and generates table style reports based on the results of that query.  The provided database is a simulation of a blog http log.  Three queries have been provided as examples (and to satisfy the assignment) within the main script:

1. What are the most popular 3 articles of all time?
2. Who are the most popular article authors of all time?
3. On which days did more than 1% of requests lead to errors?

This script was designed to be run with the provided database available here:

https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip

To run this script and generate the report:

~~~~
python3 newsreports.py
~~~~

The script creates a log generator object which is used to add sections to a report.  Each section is created by providing it with a valid query for the 'news' database and a message to display as a title for the section.  The generator object will then query the database, format the results into a nice looking table, and append it to the running report text.  The script then calls the .dump_report() function to print the output to the console.

## Views

The script makes use of the following views.  Here are their names and the 'create view' statements used to create them.

### error_counts

~~~~
create view error_counts as
select time::date as day, count(*) as requests,
count(case when status != '200 OK' then 1 end) as errors
from log
group by day;
~~~~

### top_3_articles

~~~~
create view top3articles as (
select substring(path from 10) as path, count(*) as hits from log
where status = '200 OK' and path != '/'
group by path
order by hits desc
limit 3);
~~~~
