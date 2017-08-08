# Logs Analysis project
# for Udacity FSND SQL course (nd004)
# Please see the README.md for information about this script's requirements

import psycopg2

class GenerateLogReports():
    """
    This class is used to generate all reports based the blog's http logs.
    """

    def __init__(self):
        self.report = ""
        self.DBNAME="news"

    def dump_report(self):
        """
        Dump the assembled report to an output file and the screen
        """
        print(self.report)

    def format_results(self, results, headers):
        """
        Format query results into a table for reporting
        """
        col_width = max([len(str(item)) for item in results[0]])
        divider = []
        for i in range(len(results[0])):
            divider.append('-' * col_width)

        results.insert(0, tuple(divider))
        results.insert(0, tuple(headers))

        output = ""
        for result in results:
            output += '|'.join(str(item).ljust(col_width) for item in result)
            output += '\n'

        return output

    def add_top3_articles(self):
        """
        Add a section to the report with info about the top 3 articles
        measured according to number of GET requests
        """
        pass

    def add_top3_authors(self):
        """
        Add the Top 3 Authors section to the report.  This section shows
        the top 3 authors according to number of GET requests on all written
        articles.
        """
        pass

    def add_high_error_days(self):
        """
        Add the High Error Days section to the report.  This section shows
        all days within the month where the number of requests resulting in
        any status other than '200' (errors) exceed 1 percent of the total
        number of requests for that day.
        """

        query = """
        select day, requests, errors,
        round(((errors::numeric / requests::numeric) * 100.0),2) as err_percent
        from error_counts
        where errors > (requests / 100);
        """

        self.report += "Days with > 1% errors\n"

        with psycopg2.connect(database=self.DBNAME) as db:
            with db.cursor() as c:
                c.execute(query)
                results = c.fetchall()
                headers = [desc[0] for desc in c.description]

        output = self.format_results(results, headers)
        self.report += output
        self.report += '\n\n'



if __name__ == '__main__':
    logreport = GenerateLogReports()
    logreport.add_high_error_days()
    logreport.dump_report()
