import sqlite3

from cryptography.fernet import Fernet, MultiFernet
from passlib.hash import pbkdf2_sha256

from USERS.manager import FileController
from conf import load_in
settings = load_in()

# TODO: IMPORTANT! Clean up SQL to protect against injections


def make_password(password):
    # TODO: Rewrite this, increase security, look into some kind of database-row rotations
    hashed = pbkdf2_sha256.encrypt(password, rounds=200000, salt_size=16)
    return hashed


def check_password(password, hashed):
    return pbkdf2_sha256.verify(password, hashed)


def setup():
    conn = sqlite3.connect(settings['MAIN_DB'])
    conn.execute("CREATE TABLE IF NOT EXISTS {tn} (id INTEGER,"
                 "email TEXT,"
                 "email_verified INTEGER,"
                 "username TEXT,"
                 "password TEXT,"
                 "data_tables TEXT,"
                 "logged_in INTEGER, "
                 "subscribed INTEGER,"
                 "charts TEXT,"
                 "models TEXT,"
                 "groups TEXT,"
                 "first_name TEXT,"
                 "last_name TEXT,"
                 "friends TEXT,"
                 "active INTEGER,"
                 "reset_request INTEGER,"
                 "data_sources TEXT,"
                 "projects TEXT,"
                 "is_authenticated INTEGER,"
                 "PRIMARY KEY (username))".format(tn='users'))
    conn.commit()
    conn.execute("""INSERT INTO users VALUES ('{id}',
                          '{email}', 
                          '{email_verified}', 
                          '{username}',
                          '{password}', 
                          '{data_tables}',
                           {logged_in},
                           {subscribed},
                           '{charts}',
                           '{models}',
                           '{groups}',
                           '{first_name}',
                           '{last_name}',
                           '{friends}',
                           {active},
                           {reset_request},
                           '{data_sources}',
                           '{projects}',
                           {is_authenticated})""".format(
        id=1,
        email='admin@admin.com',
        email_verified=1,
        username='Admin',
        password=make_password('password'),
        data_tables='',
        logged_in=1,
        subscribed=0,
        charts="",
        models="",
        groups="",
        first_name="",
        last_name="",
        friends="",
        active=1,
        reset_request=0,
        data_sources="",
        projects="",
        is_authenticated=0))
    conn.commit()
    conn.close()
    FileController().file_handler("Admin")


class CreateUser:

    def __init__(self, data):
        self.email = data['email']
        self.username = data['username']
        self.password = data['password']
        self.user_active = 1
        self.user_groups = []
        self.user_password_reset_request = False
        self.user_id = None
        self.con = sqlite3.connect(settings['MAIN_DB'])
        self.c = self.con.cursor()

    def user_exists(self):
        valid = self.c.execute("SELECT COUNT(*) from users WHERE username = '{}'".format(self.username)).fetchone()[0]
        return valid

    def get_id(self):
        return self.c.execute("SELECT MAX(id) FROM users").fetchone()[0]+1

    def make_account(self):
        self.user_id = self.get_id()
        valid = self.user_exists()
        if valid:
            return False
        else:
            self.con.execute("""INSERT INTO users VALUES ('{id}',
                          '{email}', 
                          '{email_verified}', 
                          '{username}',
                          '{password}', 
                          '{data_tables}',
                           {logged_in},
                           {subscribed},
                           '{charts}',
                           '{models}',
                           '{groups}',
                           '{first_name}',
                           '{last_name}',
                           '{friends}',
                           {active},
                           {reset_request},
                           '{data_sources}',
                           '{projects}',
                           {is_authenticated})""".format(
                            id=self.user_id,
                            email=self.email,
                            email_verified=0,
                            username=self.username,
                            password=make_password(self.password),
                            data_tables='',
                            logged_in=0,
                            subscribed=0,
                            charts="",
                            models="",
                            groups="",
                            first_name="",
                            last_name="",
                            friends="",
                            active=1,
                            reset_request=0,
                            data_sources="",
                            projects="",
                            is_authenticated=0))
            self.con.commit()
            self.con.close()
            return True


class User:

    def __init__(self, username):
        self.con = sqlite3.connect(settings['MAIN_DB'])
        self.c = self.con.cursor()
        self.user_items = None
        self.user_dict = None
        self.keys = None
        if self.user_exists(username):
            self.username = username
            self.password = self.c.execute("SELECT password FROM"
                                           " users WHERE username='{}'".format(username)).fetchone()[0]

    def load_user(self):
        self.user_items = self.c.execute("""SELECT id, email, email_verified, username, is_authenticated, data_tables,
                                            logged_in, subscribed, charts, models, groups, first_name, last_name,
                                            friends, active, reset_request, data_sources, projects
                                            FROM users WHERE username='{}'""".format(self.username)).fetchall()[0]
        self.user_dict = {'id': self.user_items[0], 'email': self.user_items[1], 'email_verified': self.user_items[2],
                          'username': self.user_items[3], 'is_authenticated': self.user_items[4],
                          'data_tables': self.fetch_table_list(), 'logged_in': self.user_items[6],
                          'subscribed': self.user_items[7], 'charts': self.user_items[8], 'models': self.user_items[9],
                          'groups': self.user_items[10], 'first_name': self.user_items[11],
                          'last_name': self.user_items[12], 'friends': self.user_items[13],
                          'active': self.user_items[14], 'reset_request': self.user_items[15],
                          'data_sources': self.fetch_data_list(), 'projects': self.user_items[17],
                          'table_count_keywords': list(zip(self.fetch_table_list(),
                                                           self.fetch_table_counts(),
                                                           self.fetch_keywords_list()))}
        return self.user_dict

    def user_exists(self, username):
        valid = self.c.execute("SELECT EXISTS(SELECT username "
                               "FROM users WHERE username = '{}')".format(username)).fetchone()[0]
        return valid

    def login_user(self, password):
        return check_password(password, self.password)

    def get_id(self):
        return self.user_dict['username']

    def is_authenticated(self):
        return self.user_dict['is_authenticated']

    def is_active(self):
        return self.user_dict['is_active']

    def create_data_source(self, datasource):
        FileController().make_item(self.username, datasource, 'data_source')

    def delete_source(self, datasource):
        FileController().delete_item(self.username, datasource, 'data_source')

    def fetch_data_list(self):
        return FileController().make_item(self.username, item=None, path_name='data_source', fetch=True)

    def fetch_table_counts(self):
        con = sqlite3.connect(settings['USERS_DB'].format(self.username))
        tables = self.fetch_table_list()
        my_list = []
        for table in tables:
            my_list.append(con.execute("SELECT Count(*) FROM '{}'".format(table)).fetchone()[0])
        return my_list

    def make_data(self, table_name):
        FileController().make_item(self.username, table_name, 'data_table')

    def fetch_table_list(self):
        return FileController().make_item(self.username, item=None, path_name='data_table', fetch=True)

    def fetch_keywords_list(self):
        con = sqlite3.connect(settings['MAIN_DB'])
        tables = self.fetch_table_list()
        my_list = []
        for table in tables:
            my_list.append(con.execute("SELECT keywords FROM KeywordTable"
                                       " WHERE username='{}' "
                                       "AND table_name='{}'".format(self.username, table)).fetchone()[0])
        return my_list

    def delete_data(self, table_name):
        FileController().delete_item(self.username, table_name, 'data_table')

    def load_in_keys(self):
        try:
            keys = self.c.execute("SELECT * FROM secrets WHERE username = '{}'".format(self.username)).fetchall()[0]
            ul = self.c.execute("SELECT * FROM secret_keys WHERE username = '{}'".format(self.username)).fetchall()[0]
            key1 = Fernet(ul[1])
            key2 = Fernet(ul[2])
            x = MultiFernet([key1, key2])
            access_token = x.decrypt(keys[1]).decode()
            access_token_secret = x.decrypt(keys[2]).decode()
            consumer_key = x.decrypt(keys[3]).decode()
            consumer_secret = x.decrypt(keys[4]).decode()
            token_dict = {"access_token": access_token, "access_token_secret": access_token_secret,
                          "consumer_key": consumer_key, "consumer_secret": consumer_secret}
            return token_dict

            # return token_dict
        except AttributeError:
            return None
