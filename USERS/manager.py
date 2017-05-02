import os


def file_handler(username):
    os.mkdir("PycharmProjects/FlaskOne/USERS/{}".format(username))
    first = open("PycharmProjects/FlaskOne/USERS/{}/_data_sources.txt".format(username), 'a')
    first.close()
    first = open("PycharmProjects/FlaskOne/USERS/{}/_data_tables.txt".format(username), 'a')
    first.close()
    first = open("PycharmProjects/FlaskOne/USERS/{}/_models.txt".format(username), 'a')
    first.close()
    first = open("PycharmProjects/FlaskOne/USERS/{}/_charts.txt".format(username), 'a')
    first.close()
    first = open("PycharmProjects/FlaskOne/USERS/{}/_projects.txt".format(username), 'a')
    first.close()


def make_data_source(user, data_source, fetch=False):
    data = open('PycharmProjects/FlaskOne/USERS/{}/_data_sources.txt'.format(user), 'r')
    my_items = []
    for line in data:
        my_items.append(line.strip())
    data.close()
    if fetch:
        return my_items
    if data_source not in my_items:
        data = open('PycharmProjects/FlaskOne/USERS/{}/_data_sources.txt'.format(user), 'a')
        data.write(data_source + '\n')
        data.close()


def make_data_table(user, data_table, fetch=False):
    data = open('PycharmProjects/FlaskOne/USERS/{}/_data_tables.txt'.format(user), 'r')
    my_items = []
    for line in data:
        my_items.append(line.strip())
    data.close()
    if fetch:
        return my_items
    if data_table not in my_items:
        data = open('PycharmProjects/FlaskOne/USERS/{}/_data_tables.txt'.format(user), 'a')
        data.write(data_table + '\n')
        data.close()


def make_model(user, model):
    data = open('PycharmProjects/FlaskOne/USERS/{}/_models.txt'.format(user), 'r')
    my_items = []
    for line in data:
        my_items.append(line.strip())
    data.close()
    if model not in my_items:
        data = open('PycharmProjects/FlaskOne/USERS/{}/_models.txt'.format(user), 'a')
        data.write(model + '\n')
        data.close()


def make_chart(user, chart):
    data = open('PycharmProjects/FlaskOne/USERS/{}/_charts.txt'.format(user), 'r')
    my_items = []
    for line in data:
        my_items.append(line.strip())
    data.close()
    if chart not in my_items:
        data = open('PycharmProjects/FlaskOne/USERS/{}/_charts.txt'.format(user), 'a')
        data.write(chart + '\n')
        data.close()


def make_project(user, project):
    data = open('PycharmProjects/FlaskOne/USERS/{}/_projects.txt'.format(user), 'r')
    my_items = []
    for line in data:
        my_items.append(line.strip())
    data.close()
    if project not in my_items:
        data = open('PycharmProjects/FlaskOne/USERS/{}/_projects.txt'.format(user), 'a')
        data.write(project + '\n')
        data.close()


def delete_data_source(user, data_source):
    data = open('PycharmProjects/FlaskOne/USERS/{}/_data_sources.txt'.format(user), 'r')
    my_items = []
    for line in data:
        my_items.append(line.strip())
    data.close()
    if data_source in my_items:
        my_items.remove(data_source)
        data = open('PycharmProjects/FlaskOne/USERS/{}/_data_sources.txt'.format(user), 'w')
        for line in my_items:
            data.write(line + '\n')
        data.close()


def delete_data_table(user, table):
    data = open('PycharmProjects/FlaskOne/USERS/{}/_data_tables.txt'.format(user), 'r')
    my_items = []
    for line in data:
        my_items.append(line.strip())
    data.close()
    if table in my_items:
        my_items.remove(table)
        data = open('PycharmProjects/FlaskOne/USERS/{}/_data_tables.txt'.format(user), 'w')
        for line in my_items:
            data.write(line + '\n')
        data.close()


def delete_chart(user, chart):
    data = open('PycharmProjects/FlaskOne/USERS/{}/_charts.txt'.format(user), 'r')
    my_items = []
    for line in data:
        my_items.append(line.strip())
    data.close()
    if chart in my_items:
        my_items.remove(chart)
        data = open('PycharmProjects/FlaskOne/USERS/{}/_charts.txt'.format(user), 'w')
        for line in my_items:
            data.write(line + '\n')
        data.close()


def delete_model(user, model):
    data = open('PycharmProjects/FlaskOne/USERS/{}/_models.txt'.format(user), 'r')
    my_items = []
    for line in data:
        my_items.append(line.strip())
    data.close()
    if model in my_items:
        my_items.remove(model)
        data = open('PycharmProjects/FlaskOne/USERS/{}/_models.txt'.format(user), 'w')
        for line in my_items:
            data.write(line + '\n')
        data.close()


def delete_project(user, project):
    data = open('PycharmProjects/FlaskOne/USERS/{}/_projects.txt'.format(user), 'r')
    my_items = []
    for line in data:
        my_items.append(line.strip())
    data.close()
    if project in my_items:
        my_items.remove(project)
        data = open('PycharmProjects/FlaskOne/USERS/{}/_projects.txt'.format(user), 'w')
        for line in my_items:
            data.write(line + '\n')
        data.close()
