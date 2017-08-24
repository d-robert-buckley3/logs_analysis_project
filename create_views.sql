create view error_counts as
select time::date as day, count(*) as requests,
count(case when status != '200 OK' then 1 end) as errors
from log
group by day;

create view top_articles as (
select path, count(*) as hits from log
where status = '200 OK' and path != '/'
group by path
order by hits desc);
