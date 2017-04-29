import random
import sqlite3
import pandas as pd

from cryptography.fernet import Fernet, MultiFernet
from flask import Flask, session, redirect, request, Response
from flask import render_template, stream_with_context

from Functions.Arrival import CreateUser, User
from USERS.manager import FileController
from Views.Arrival import RegistrationForm, LoginForm, TwitterForm, ScrapeKeywordsForm
from USERS.TwitterScraper import Scraper
from conf import load_in
settings = load_in()
app = Flask(__name__)
app.secret_key = bytes(random.getrandbits(16))


def login_required():
    if session['counter'] < 2:
        session.clear()
        return True


def form_maker(keys, datatypes):
    my_list = []
    for item in zip(keys, datatypes):
        my_list.append([item[0], item[1]])
    return my_list


def sumsessioncounter():
    try:
        session['counter'] += 1
    except KeyError:
        session['counter'] = 1


@app.route('/', methods=['POST', 'GET'])
def arrival():
    return redirect('/login')


@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm(request.form)
    data_dict = {}
    sumsessioncounter()
    if request.method == 'POST' and form.validate():
        data_dict['username'] = form.username.data
        data_dict['password'] = form.password.data
        print(data_dict)
        user = User(data_dict['username'])
        if user.login_user(data_dict['password']):
            the_dict = user.load_user()
            the_dict['data_sources'] = user.fetch_data_list()
            the_dict['data_tables'] = user.fetch_table_list()
            for items in the_dict.items():
                session[items[0]] = items[1]
            return redirect("/home")
    return render_template('Arrival/login.html', form=form)


@app.route('/register', methods=["GET", "POST"])
def register():
    form = RegistrationForm(request.form)
    data_dict = {}
    if request.method == 'POST' and form.validate():
        data_dict['email'] = form.email.data
        data_dict['username'] = form.username.data
        data_dict['password'] = form.password.data
        data_dict['email'] = form.email.data
        user = CreateUser(data_dict)
        success = user.make_account()
        if not success:
            return render_template('Arrival/signup.html', form=form, nameerror="That username is taken")
        else:
            FileController().file_handler(data_dict['username'])
            return redirect("login")
    return render_template('Arrival/signup.html', form=form)


@app.route('/logout')
def logout():
    session.clear()
    return redirect("/login")


@app.route('/home')
def homepage():
    sumsessioncounter()
    if login_required():
        return redirect("/login")
    return render_template('User/base.html')


@app.route('/datasources', methods=["POST", "GET"])
def datasources():
    sumsessioncounter()
    if login_required():
        return redirect("/login")
    form = TwitterForm(request.form)
    if request.method == 'POST' and form.validate():
        m1 = form.access_token.data
        m2 = form.access_token_secret.data
        m3 = form.consumer_key.data
        m4 = form.consumer_secret.data
        my_list = [bytes(m1, 'utf-8'), bytes(m2, 'utf-8'), bytes(m3, 'utf-8'), bytes(m4, 'utf-8')]
        first = Fernet.generate_key()
        second = Fernet.generate_key()
        key1 = Fernet(first)
        key2 = Fernet(second)
        x = MultiFernet([key1, key2])
        token1 = x.encrypt(my_list[0])
        token2 = x.encrypt(my_list[1])
        token3 = x.encrypt(my_list[2])
        token4 = x.encrypt(my_list[3])
        con = sqlite3.connect(settings['MAIN_DB'])
        con.execute("""CREATE TABLE IF NOT EXISTS {tn} (username TEXT,
                               key1 BLOB,
                               key2 BLOB, PRIMARY KEY (username))""".format(tn="secret_keys"))
        con.execute("""INSERT INTO secret_keys VALUES (?,?,?)""", (session['username'], first, second))
        con.execute("""CREATE TABLE IF NOT EXISTS {tn} (username TEXT,
                       access_token BLOB,
                       access_token_secret BLOB,
                       consumer_key BLOB,
                       consumer_secret BLOB, PRIMARY KEY (username))""".format(tn="secrets"))
        con.execute("""INSERT INTO secrets VALUES (?,?,?,?,?)""", (session['username'], token1, token2, token3, token4))
        con.commit()
        con.close()
        User(session['username']).create_data_source("Twitter")
        session['data_sources'] = User(session['username']).fetch_data_list()
        sources = User(session['username']).fetch_data_list()
        return render_template('User/datasources.html', form=form, sources=sources)
    else:
        sources = User(session['username']).fetch_data_list()
        return render_template('User/datasources.html', form=form, sources=sources)


@app.route('/datasets', methods=["POST", "GET"])
def datasets():
    sumsessioncounter()
    if login_required():
        return redirect("/login")
    form = ScrapeKeywordsForm(request.form)
    if request.method == 'POST' and form.validate():
        limit = form.limit.data
        limit_type = form.limit_type.data
        keywords = form.keywords.data
        table = form.table.data
        password = form.password.data
        con = sqlite3.connect(settings['MAIN_DB'])
        con.execute("""CREATE TABLE IF NOT EXISTS {tn} (username TEXT,
                                       table_name TEXT,
                                       keywords TEXT,
                                       PRIMARY KEY (username, table_name))""".format(tn="KeywordTable"))
        con.execute("""INSERT INTO KeywordTable VALUES (?,?,?)""", (session['username'], table, keywords))
        con.commit()
        con.close()
        my_list = list(map(lambda x: x.strip(), keywords.split(',')))
        User(session['username']).make_data(table)

        def load_stuff(lim_type, lim, mylist, the_table, current_session):
            if User(current_session['username']).login_user(password):
                thing = Scraper('track')
                thing.set_limit(lim_type, lim)
                thing.set_languages(['en'])
                thing.search_configure(mylist)
                thing.database_config(current_session['username'], the_table)
                thing.set_keys(User(current_session['username']).load_in_keys())
                current_session['data_tables'] = User(current_session['username']).fetch_table_list()
                yield render_template('User/datasets.html',
                                      form=form,
                                      session=current_session,
                                      loading={"table": the_table, "limit_t": lim_type, "limit": lim})
                thing.scrape()
                return render_template('User/datasets.html', form=form, session=current_session)
        session['data_tables'] = User(session['username']).fetch_table_list()
        return Response(stream_with_context(load_stuff(limit_type, limit, my_list, table, session)))
    else:
        session['data_tables'] = User(session['username']).fetch_table_list()
        return render_template("User/datasets.html", form=form, session=session)


@app.route('/charts')
def charts():
    sumsessioncounter()
    if login_required():
        return redirect("/login")
    return render_template("User/charts.html")


@app.route('/models')
def models():
    sumsessioncounter()
    if login_required():
        return redirect("/login")
    return render_template("User/models.html")


@app.route('/projects')
def projects():
    sumsessioncounter()
    if login_required():
        return redirect("/login")
    return render_template("User/projects.html")


@app.route('/groups')
def groups():
    sumsessioncounter()
    if login_required():
        return redirect("/login")
    return render_template("User/groups.html")


@app.route('/datasources/edit/<item>')
def edit_datasource(item):
    print(item)
    return "<h1>Needs Built</h1>"


@app.route('/datasources/delete/<item>')
def delete_datasource(item):
    sumsessioncounter()
    User(session['username']).delete_source(item)
    session['data_sources'] = User(session['username']).fetch_data_list()
    con = sqlite3.connect(settings['MAIN_DB'])
    con.execute("DELETE FROM secrets WHERE username='{}'".format(session['username']))
    con.execute("DELETE FROM secret_keys WHERE username='{}'".format(session['username']))
    con.commit()
    con.close()
    return redirect("/datasources")


@app.route('/datasets/delete/<item>')
def delete_table(item):
    sumsessioncounter()
    User(session['username']).delete_data(item)
    session['data_tables'] = User(session['username']).fetch_table_list()
    con = sqlite3.connect(settings['MAIN_DB'])
    con.execute("DELETE FROM KeywordTable  WHERE username=? AND table_name=?", (session['username'], item))
    con.commit()
    con.close()
    con = sqlite3.connect(settings['USERS_DB'].format(session['username']))
    con.execute("DROP TABLE IF EXISTS {}".format(item))
    con.commit()
    con.close()
    return redirect("/datasets")


@app.route('/datasets/export/<item>/<export>')
def export_table(item, export):
    sumsessioncounter()
    con = sqlite3.connect(settings['USERS_DB'].format(session['username']))
    my_frame = pd.read_sql_query("SELECT * FROM '{}'".format(item), con)
    print(my_frame, export)
    return redirect("/datasets")


@app.route('/datasets/view/<table>')
def view_table(table):
    sumsessioncounter()
    con = sqlite3.connect(settings['USERS_DB'].format(session['username']))
    my_frame = pd.read_sql_query("SELECT * FROM '{}'".format(table), con)
    x = my_frame.to_html()
    print(x, table)
    return "{}".format(x)

if __name__ == '__main__':
    app.run()
