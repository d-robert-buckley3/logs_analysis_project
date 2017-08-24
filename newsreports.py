#!/usr/bin/python3
"""
Logs Analysis project
for Udacity FSND SQL course (nd004)
Please see the README.md for information about this script's requirements
"""

from newsdb import GenerateLogReports

report_sections = [
    {
        'query': """
            select articles.title, top_articles.hits
            from articles, top_articles
            where '/article/' || articles.slug like top_articles.path
            order by hits desc
            limit 3;
        """,
        'message': "Top 3 Articles by successful hits"
    },
    {
        'query': """
            select authors.name, count(*) as hits
            from authors, articles, log
            where log.status = '200 OK'
            and log.path != '/'
            and '/article/' || articles.slug like log.path
            and articles.author = authors.id
            group by authors.name
            order by hits desc;
        """,
        'message': "Top Authors by total hits"
    },
    {
        'query': """
            select day, requests, errors,
            round(((errors::numeric / requests::numeric) * 100.0),2)
                as err_percent
            from error_counts
            where errors > (requests / 100);
        """,
        'message': "Days with > 1% errors"
    }
]

if __name__ == '__main__':
    logreport = GenerateLogReports()
    for section in report_sections:
        logreport.add_report_section(section['query'], section['message'])
    logreport.dump_report()
