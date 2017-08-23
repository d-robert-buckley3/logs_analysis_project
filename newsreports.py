#!/usr/bin/python3
# Logs Analysis project
# for Udacity FSND SQL course (nd004)
# Please see the README.md for information about this script's requirements

import psycopg2

class GenerateLogReports():
    """
    This class is used to generate all reports based on the blog's http logs.
    """

    def __init__(self):
        self.report = ""
        self.DBNAME="news"

    def dump_report(self):
        """
        Dump the assembled report to an output file and the screen
        """
        print(self.report)

    def format_results(self, results, message):
        """
        Format query results into a table for reporting
        """
        output = ""
        bar = '=' * len(message)
        output += '\n'.join([bar, message, bar, ''])

        col_width = max([len(str(item)) for sublist in results for item in sublist])

        divider = []
        for i in range(len(results[0])):
            divider.append('-' * col_width)

        results.insert(1, tuple(divider))

        for result in results:
            output += '|'.join(str(item).ljust(col_width) for item in result)
            output += '\n'

        return output

    def query_log(self, query):
        """
        Submit a query to the database and return the results.
        Column headers stored in cursor.description are inserted to the head
        of the results list
        """
        with psycopg2.connect(database=self.DBNAME) as db:
            with db.cursor() as c:
                c.execute(query)
                results = c.fetchall()
                headers = [desc[0] for desc in c.description]

        results.insert(0, headers)
        return results

    def add_report_section(self, query, message):
        """
        Appends a section to the report
        """
        results = self.query_log(query)
        text_results = self.format_results(results, message)
        self.report += text_results
        self.report += '\n\n'

    def add_top3_articles(self):
        """
        Add a section to the report with info about the top 3 articles
        measured according to number of GET requests
        """
        query = """
        select articles.title, top3articles.hits
        from articles, top3articles
        where articles.slug like top3articles.path
        order by hits desc;
        """

        message = "Top 3 Articles by successful hits"

        self.add_report_section(query, message)

    def add_top3_authors(self):
        """
        Add the Top 3 Authors section to the report.  This section shows
        the top 3 authors according to number of GET requests on all written
        articles.
        """

        query = """
        select authors.name, count(*) as hits
        from authors, articles, log
        where log.status = '200 OK'
        and log.path != '/'
        and articles.slug like substring(log.path from 10)
        and articles.author = authors.id
        group by authors.name
        order by hits desc;
        """

        message = "Top 3 Authors by total hits"

        self.add_report_section(query, message)


    def add_high_error_days(self):
        """
        Add the High Error Days section to the report.  This section shows
        all days where the number of requests resulting in
        any status other than '200' (errors) exceed 1 percent of the total
        number of requests for that day.

        This section relies on the view error_counts.
        """

        query = """
        select day, requests, errors,
        round(((errors::numeric / requests::numeric) * 100.0),2) as err_percent
        from error_counts
        where errors > (requests / 100);
        """

        message = "Days with > 1% errors"

        self.add_report_section(query, message)



if __name__ == '__main__':
    logreport = GenerateLogReports()
    logreport.add_top3_authors()
    logreport.add_top3_articles()
    logreport.add_high_error_days()
    logreport.dump_report()
