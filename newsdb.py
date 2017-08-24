# class for handling connections and queries from the News database

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

        col_widths = self.get_col_widths(results)

        divider = []
        for col_width in col_widths:
            divider.append('-' * col_width)

        results.insert(1, tuple(divider))

        row_format = ""
        for col_width in col_widths:
            row_format += "{:%s}|" % col_width
        if row_format.endswith('|'):
            row_format = row_format[:-1]

        for result in results:
            output += row_format.format(
                *[item if (isinstance(item, int))
                    else str(item) for item in result]
                )
            output += '\n'

        return output

    def get_col_widths(self, results):
        """
        Calculate the desired column width for each column based on largest
        item in that column

        Return list of column widths, one width for each column
        """
        col_widths = []
        columns = len(results[0])

        for column in range(columns):
            col_widths.append(max([len(str(item[column])) for item in results]))

        return col_widths

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
