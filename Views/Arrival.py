from wtforms import Form, PasswordField, validators, StringField, BooleanField, RadioField, TextAreaField, IntegerField


class RegistrationForm(Form):
    username = StringField('Username', [validators.Length(min=4, max=25), validators.InputRequired()])
    email = StringField("Email Address", [validators.Email(), validators.InputRequired()])
    password = PasswordField("Password", [validators.InputRequired(),validators.EqualTo('confirm', message="Passwords must match")])
    confirm = PasswordField('Confirm Password', [validators.InputRequired()])
    accept_tos = BooleanField('I accept the Terms and Conditions', [validators.DataRequired()])

class LoginForm(Form):
    username = StringField('Username', [validators.InputRequired()])
    password = PasswordField('Password', [validators.InputRequired()])

class TwitterForm(Form):
    access_token = StringField('Access Token', [validators.InputRequired()])
    access_token_secret = StringField('Access Token Secret', [validators.InputRequired()])
    consumer_key = StringField('Consumer Key', [validators.InputRequired()])
    consumer_secret = StringField('Consumer Secret', [validators.InputRequired()])

class ScrapeKeywordsForm(Form):
    limit = IntegerField("Limit", [validators.InputRequired(), validators.NumberRange(min=1, max=1000, message="To collect more than 1000 tweets at a time upgrade today!")])
    limit_type = RadioField("Limit Type", [validators.InputRequired()], choices=[("TIME", "Seconds"), ("COUNT", "Tweets")])
    keywords = TextAreaField("Keywords, separated by a comma", [validators.InputRequired()])
    table = StringField("Table Name", [validators.InputRequired(),validators.Length(min=1, max=25)])
    password = PasswordField("Confirm Password", [validators.InputRequired()])