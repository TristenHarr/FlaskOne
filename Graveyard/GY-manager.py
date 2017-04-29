import os
primary_folder = "PycharmProjects/FlaskOne/USERS/{}"
data_source_path = primary_folder+"/_data_sources.txt"
data_tables_path = primary_folder+"/_data_tables.txt"
models_path = primary_folder+"/_models.txt"
charts_path = primary_folder+"/_charts.txt"
projects_path = primary_folder+"/_projects.txt"
control_dict = {"data_source": data_source_path, "data_table": data_tables_path, "model": models_path,
                "chart": charts_path, "project": projects_path}

def file_handler(username):
    os.mkdir(primary_folder.format(username))
    first = open(data_source_path.format(username), 'a')
    first.close()
    first = open(data_tables_path.format(username), 'a')
    first.close()
    first = open(models_path.format(username), 'a')
    first.close()
    first = open(charts_path.format(username), 'a')
    first.close()
    first = open(projects_path.format(username), 'a')
    first.close()


def make_item(username, item, path_name, fetch=False):
    primary_folder = "PycharmProjects/FlaskOne/USERS/{}"
    data_source_path = primary_folder + "/_data_sources.txt"
    data_tables_path = primary_folder + "/_data_tables.txt"
    models_path = primary_folder + "/_models.txt"
    charts_path = primary_folder + "/_charts.txt"
    projects_path = primary_folder + "/_projects.txt"
    control_dict = {"data_source": data_source_path, "data_table": data_tables_path, "model": models_path,
                    "chart": charts_path, "project": projects_path}
    data = open(control_dict[path_name].format(username), 'r')
    my_items = []
    for line in data:
        my_items.append(line.strip())
    data.close()
    if fetch:
        return my_items
    if item not in my_items:
        data = open(control_dict[path_name].format(username), 'a')
        data.write(item + '\n')
        data.close()

def delete_item(username, item, path_name):
    primary_folder = "PycharmProjects/FlaskOne/USERS/{}"
    data_source_path = primary_folder + "/_data_sources.txt"
    data_tables_path = primary_folder + "/_data_tables.txt"
    models_path = primary_folder + "/_models.txt"
    charts_path = primary_folder + "/_charts.txt"
    projects_path = primary_folder + "/_projects.txt"
    control_dict = {"data_source": data_source_path, "data_table": data_tables_path, "model": models_path,
                    "chart": charts_path, "project": projects_path}
    data = open(control_dict[path_name].format(username), 'r')
    my_items = []
    for line in data:
        my_items.append(line.strip())
    data.close()
    if item in my_items:
        my_items.remove(item)
        data = open(control_dict[path_name].format(username), 'w')
        for line in my_items:
            data.write(line + '\n')
        data.close()