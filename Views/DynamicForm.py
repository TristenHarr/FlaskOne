from wtforms import Form, PasswordField, validators, StringField, SelectMultipleField, RadioField, TextAreaField, SelectField, IntegerField
from flask import session
from conf import load_in
settings = load_in()
import sqlite3





class ModelForm(Form):
    table = SelectField('Table', [validators.InputRequired()], choices=[(table, table) for table in session['data_tables']])
    model_type = RadioField("Model Template",[validators.InputRequired()], choices=[('wc', "Word Count")])
    rows = SelectField('Table Rows To Use', [validators.InputRequired()],
                       choices=[('plain_text', 'Tweet'), ('plain_desc', 'User Description')])

class ExportForm(Form):
    table = SelectField("Table Name", [validators.InputRequired()],  choices=[(table, table) for table in session['data_tables']])
    choice = RadioField("Export As", [validators.InputRequired()],
                           choices=[('csv','CSV'),
                                    ('json', "JSON"),
                                    ("excel", "Excel"),
                                    ("html", "html"),
                                    ("LaTeX", "LaTeX")])