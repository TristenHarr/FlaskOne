from Analysis.DataPuller import DataBaseSearch, Table, Statement
from conf import load_in
from nltk import FreqDist

settings = load_in()

from flask import session
def wc(table, row):
    my_string = """"""
    thing = DataBaseSearch(settings['USERS_DB'].format(session['username']))
    x = thing.get_DataFrame("SELECT {} FROM '{}'".format(row, table))
    for item in x.as_matrix():
        my_string += " "+item[0]
    my_list = my_string.split(' ')
    my_words = FreqDist(my_list).most_common(500)
    return my_words