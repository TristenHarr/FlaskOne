import os
"""alt_manager.py - a streamlined manager which minimizes repetitious code

   Improvements:
   -target parameters for single make_, delete_, and fetch_ methods
   -data populates using "with open" blocks and list comprehension for readability
   -PEP8 compliance and comments provided
   
   Overall, reduces code block by more than 50 lines
"""

__author__ = "J. Conrad"
__version__ = "0.1"
_valid_target = ["data_source", "data_tables", "models", "charts", "projects"]
_valid_fetch = ["data_source", "data_tables"]


def file_handler(username):
    """Creates or verifies user directory and required files
    
    EXIT CODE:
        0   Fail (not sure this will happen with this setup
        1   Success
    
    :param username: target location for user directory
    :return: Exit code
    """
    try:
        os.mkdir("PycharmProjects/FlaskOne/USERS/{}".format(username))
    except OSError:
        pass  # print("User directory exists")
    for target in _valid_target:
        with open("PycharmProjects/FlaskOne/USERS/{0}/_{1}.txt".format(username, target), 'a'):
            pass
    return 1


def make_target(user, target, input_stream):
    """Updates target file in directory with input
    
    EXIT CODE:
        0   Fail
    
    :param user: username directory
    :param target: file to update
    :param input_stream: data element to add
    :return: None
    """
    if target not in _valid_target:
        return 0
    with open('PycharmProjects/FlaskOne/USERS/{0}/_{1}.txt'.format(user, target), 'r') as data:
        my_items = [line.strip() for line in data]
    if input_stream not in my_items:
        with open('PycharmProjects/FlaskOne/USERS/{0}/_{1}.txt'.format(user, target), 'a') as data:
            data.write(input_stream + '\n')


def fetch_target(user, fetch):
    """Retrieves data from target file in directory 
    
    EXIT CODE:
        0  Fail
    
    :param user: username directory
    :param fetch: target file to retrieve data
    :return: contents of target file
    """
    if fetch not in _valid_fetch:
        return 0
    with open('PycharmProjects/FlaskOne/USERS/{0}/_{1}.txt'.format(user, fetch), 'r') as data:
        my_items = [line.strip() for line in data]
    return my_items


def delete_target(user, target, input_stream):
    """Deletes data from target file in directory
    
    EXIT CODE:
        0   Fail
        1   Success
    
    :param user: username directory
    :param target: file to update
    :param input_stream: data element to add
    :return: exit code indicating success or failure
    """
    if target not in _valid_target:
        return 0
    with open('PycharmProjects/FlaskOne/USERS/{0}/_{1}.txt'.format(user, target), 'r') as data:
        my_items = [line.strip() for line in data]
    if input_stream in my_items:
        my_items.remove(input_stream)
        with open('PycharmProjects/FlaskOne/USERS/{0}/_{1}.txt'.format(user, target), 'w') as data:
            for line in my_items:
                data.write(line + '\n')
    return 1
