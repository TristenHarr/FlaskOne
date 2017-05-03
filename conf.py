import os

config = "/home/tristen/PycharmProjects/FlaskOne/CONFIG.txt"

class Config:
    def __init__(self):
        self.home_path = os.getcwd()
        self.user_defaults = None
        self.main_db = None
        self.users_db = None
        self.tests = None
        self.forms = None

    def setup_main_db(self, main_db_folder="DATABASE", main_db="data", main_db_extension='.db'):
        db = main_db + main_db_extension
        self.main_db = os.path.join(self.home_path, main_db_folder, db)
        file = open(os.getcwd()+"/CONFIG.txt", 'r')
        my_setup = {}
        for line in file:
            splitted = line.strip().split(':')
            my_setup[splitted[0]] = splitted[1]
        file.close()
        if "MAIN_DB" in my_setup.keys():
            raise IsADirectoryError("Configuration has already been set, to change use function edit_conf(current_conf_name, new)")
        else:
            file = open(os.getcwd()+"/CONFIG.txt", 'a')
            file.write("MAIN_DB:{}\n".format(self.main_db))
            file.close()

    def set_users_db(self, users_folder="USERS", users_db='data1', users_db_extenstion='.db'):
        file = open(os.getcwd()+"/CONFIG.txt", 'r')
        my_setup = {}
        for line in file:
            splitted = line.strip().split(':')
            my_setup[splitted[0]] = splitted[1]
        file.close()
        if "USERS_DB" in my_setup.keys():
            raise IsADirectoryError(
                "Configuration has already been set, to change use function edit_conf(current_conf_name, new)")
        else:
            userdb = os.getcwd()+"/{}".format(users_folder)+"/{}/"+users_db+users_db_extenstion
            file = open(os.getcwd()+"/CONFIG.txt", 'a')
            file.write("USERS_DB:{}\n".format(userdb))
            file.close()

    # def setup(self, admin_username, admin_email, admin_password):
    #     conn = sqlite3.connect(main_database())
    #     conn.execute("CREATE TABLE IF NOT EXISTS {tn} (id INTEGER,"
    #                  "email TEXT,"
    #                  "email_verified INTEGER,"
    #                  "username TEXT,"
    #                  "password TEXT,"
    #                  "data_tables TEXT,"
    #                  "logged_in INTEGER, "
    #                  "subscribed INTEGER,"
    #                  "charts TEXT,"
    #                  "models TEXT,"
    #                  "groups TEXT,"
    #                  "first_name TEXT,"
    #                  "last_name TEXT,"
    #                  "friends TEXT,"
    #                  "active INTEGER,"
    #                  "reset_request INTEGER,"
    #                  "data_sources TEXT,"
    #                  "projects TEXT,"
    #                  "is_authenticated INTEGER,"
    #                  "PRIMARY KEY (username))".format(tn='users'))
    #     conn.commit()
    #     conn.execute("""INSERT INTO users VALUES ('{id}',
    #                           '{email}',
    #                           '{email_verified}',
    #                           '{username}',
    #                           '{password}',
    #                           '{data_tables}',
    #                            {logged_in},
    #                            {subscribed},
    #                            '{charts}',
    #                            '{models}',
    #                            '{groups}',
    #                            '{first_name}',
    #                            '{last_name}',
    #                            '{friends}',
    #                            {active},
    #                            {reset_request},
    #                            '{data_sources}',
    #                            '{projects}',
    #                            {is_authenticated})""".format(
    #         id=1,
    #         email='admin@admin.com',
    #         email_verified=1,
    #         username='Admin',
    #         password=make_password('password'),
    #         data_tables='',
    #         logged_in=1,
    #         subscribed=0,
    #         charts="",
    #         models="",
    #         groups="",
    #         first_name="",
    #         last_name="",
    #         friends="",
    #         active=1,
    #         reset_request=0,
    #         data_sources="",
    #         projects="",
    #         is_authenticated=0))
    #     conn.commit()
    #     conn.close()
    #     FileController().file_handler("Admin")

def load_in():
    file = open(config, 'r')
    my_setup = {}
    for line in file:
        splitted = line.strip().split(':')
        my_setup[splitted[0]] = splitted[1]
    file.close()
    return my_setup

