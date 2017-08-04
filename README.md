# Logs Analysis Project
This is the course project for SQL at Udacity (nd004) on log analysis and reporting.  The Python script loads the 'newsdata.sql' database via the psycopg2 module.  The provided database is a simulation of a blog http log.  The script reports on 3 things within the data:

1. What are the most popular 3 articles of all time?
2. Who are the most popular article authors of all time?
3. On which days did more than 1% of requests lead to errors?

This script was designed to be run with the provided database available here:

https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip

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
