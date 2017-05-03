import pandas as pd
import sqlite3 as sq
from conf import load_in
settings = load_in()


class DataBaseSearch(object):
    def __init__(self, database):
        """
        Connects to a sqlite database in the DATABASE folder

        :type database: str
        :param database: The name of the database to connect to
        """
        self.database = database
        self.con = sq.connect(database)
        print(self.database)

    def get_DataFrame(self, query):
        """
        Retrieves a pandas dataframe from the custom built SQL query

        :type query: str
        :param query:The query built by the Table Object
        :return: pandas DataFrame
        """
        my_frame = pd.read_sql_query("{}".format(query), self.con)
        return my_frame

    def insert_into(self, table, table_key, hashed):
        """
        Inserts a hashed password into the specified table, at the table key
        :param table: The table to insert the hashed password into
        :param table_key: The table_key to specify the row of the table
        :param hashed: The hashed password
        :return: None
        """
        self.con.execute("INSERT INTO {} VALUES('{}','{}')".format(table, table_key, hashed))
        self.con.commit()


class Table(object):
    def __init__(self, table=None, rows=list(), alias=""):
        """
        :type table: str
        :param table: Table name
        :type rows: list
        :param rows: Table rows to retrieve
        :type alias: str
        :param alias: Table alias
        """
        self.table = str(table)
        self.table_show = str(table)
        self.rows = "{}".format(",".join(rows))
        self.alias = alias
        self.statement_list = []
        self.query = "SELECT {} FROM {} {} ".format(self.rows, self.table, self.alias)

    def __str__(self):
        return 'Current Table: {}'.format(self.table_show)

    def update(self):
        """
        Updates the table query
        :return: None
        """
        self.query = 'SELECT {} FROM {} {} '.format(self.rows, self.table, self.alias)
        for item in self.statement_list:
            self.query += item

    def set_table(self, table):
        """
        Resets the table-name to specified table 
        :param table: New table name
        :return: None
        """
        self.table_show = "{}".format(table)
        self.table = table
        self.update()

    def select_rows(self, rows=list()):
        """
        Sets the rows to retrieve information from in the form of a list

        :type rows: list
        :param rows: The rows to be retrieved from the database
        :return: None
        """
        for item in rows:
            self.rows += "{},".format(item)
        else:
            self.rows = self.rows.strip(',')
        # self.query = "SELECT {} FROM {} {} {}".format(self.rows, self.table, self.alias, self.statement)
        self.update()

    def add_rows(self, rows=list()):
        """
        Adds additonal rows to the selection

        :type rows: list
        :param rows: A list of rows to add to the selection
        :return: None
        """
        for item in rows:
            self.rows += "{}".format(item)

    def set_alias(self, alias):
        """
        Sets the database table alias to alias

        :type alias: str
        :param alias: The alias to be used for the database
        :return: None
        """
        self.alias = "AS {}".format(alias)
        self.update()
        # self.query = "SELECT {} FROM {} {} {}".format(self.rows, self.table, self.alias, self.statement)

    def commit_statement(self, statement):
        """
        Adds the statement to the query
        :param statement: A Statement
        :return: None
        """
        self.query = self.query.strip(';" ') + " "
        self.query += str(statement) + ';'


class Statement(object):
    def __init__(self, choice_type="WHERE", selection="", comparison="LIKE", parameters=""):
        """
        A statement object that allows for custom SQL queries to be built

        :param choice_type: WHERE, AND, OR
        :param selection: row_name
        :param comparison: LIKE
        :param parameters: A string to be inserted into HERE in LIKE %HERE%
        """
        self._choice_type = choice_type
        self._selection = selection
        self._operator = comparison
        self._condition = parameters

    def set_selection(self, selection):
        self._selection = selection

    def set_comparison(self, comparison='LIKE'):
        self._operator = comparison

    def set_parameters(self, parameters="%Stuff%"):
        self._condition = parameters

    def __str__(self):
        return "{} {} {} {}".format(self._choice_type, self._selection, self._operator, self._condition)


        # """
        # Specify which Database to connect to, by default the program will look for the database
        # in a folder titled DATABASE, this can be changed by adding a second parameter to the
        # DataBaseSearch"""
        # con = DataBaseSearch('Model1')
        # """
        # Create a Table object representing a table in the database to be queried, specify the
        # table name as a string, and then a list of the rows that should be retrieved from the table
        # """
        # animals = Table("animals", ['row1', 'row2'])
        # """
        # Specify a conditional statement, the selection represents the row, and the parameters
        # represent the condition."""
        # animals_search = Statement(selection='animal', parameters="'dog'")
        # #Commit the statement into the table
        # animals.commit_statement(animals_search)
        # # Retrieve the dataframe, in this case the following would be performed in Database Model1
        # # SELECT row1, row2 FROM animals WHERE animal LIKE %'dog'%;
        # animals_dataframe = con.get_DataFrame(animals.query)
        #
        # """The reason this was built is because it allows for queries to be built dynamically
        # and it allows multiple tables and queries to be built and accessed when needed"""