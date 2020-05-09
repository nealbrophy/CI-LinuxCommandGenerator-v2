import os
from flask import Flask, render_template, redirect, request, url_for, abort, flash
from flask_pymongo import PyMongo
from flask_wtf import FlaskForm, RecaptchaField, CSRFProtect
from wtforms import (StringField,SubmitField,
                         DateTimeField, RadioField,
                         SelectField,TextAreaField, DateField)
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired

csrf = CSRFProtect()

app = Flask(__name__)
# mongodb
app.config["MONGO_DBNAME"] = 'linuxCmdGen'
app.config["MONGO_URI"] = os.environ.get('MONGO_URI')
mongo = PyMongo(app)

# generate distro list
distros_for_form = {}
distros_for_form.update({'select distro':''})
for distro in mongo.db.distros.find():
  distros_for_form.update({distro['distro_name']:distro['distro_name']})



# ========
# WTForms
# ========
class AddCommandForm(FlaskForm):
    recaptcha = RecaptchaField()
    form_name = StringField('app_name', validators=[DataRequired()])
    form_distro = SelectField('app_distro', validators=[DataRequired()], choices=[distro for distro in distros_for_form])
    form_selected_distro = StringField('selected_distro')
    form_url = StringField('app_url')
    form_instruction = StringField('app_instruction', validators=[DataRequired()])
    form_command = StringField('app_command', validators=[DataRequired()])
    form_submit = SubmitField('Submit')

class DeleteForm(FlaskForm):
    recaptcha = RecaptchaField()
    form_name = StringField('app_name', validators=[DataRequired()])
    form_selected_distro = StringField('selected_distro')
    form_url = StringField('app_url')
    form_instruction = StringField('app_instruction', validators=[DataRequired()])
    form_command = StringField('app_command', validators=[DataRequired()])
    form_submit = SubmitField('Delete')

class EditForm(FlaskForm):
    recaptcha = RecaptchaField()
    form_name = StringField('app_name', validators=[DataRequired()])
    form_url = StringField('app_url')
    form_instruction = StringField('app_instruction', validators=[DataRequired()])
    form_command = StringField('app_command', validators=[DataRequired()])
    form_submit = SubmitField('Update')

class EmailForm(FlaskForm):
    recaptcha = RecaptchaField()
    email_address = EmailField('email address', validators=[DataRequired()])
    email_submit = SubmitField('Send')

class SimpleSearch(FlaskForm):
    search_app = StringField()
    search_distro = SelectField('app_distro', choices=[
        ('', ''), 
        ('Ubuntu', 'Ubuntu'),
        ('Debian', 'Debian'),
        ('Arch', 'Arch'),
        ('Elementary', 'Elementary'),
        ('Alpine', 'Alpine'),
        ('CentOS', 'CentOS'),
        ('Devuan', 'Devuan'),
        ('Fedora', 'Fedora'),
        ('Gentoo', 'Gentoo'),
        ('Linux Mint', 'Linux Mint'),
        ('Mageia', 'Mageia'),
        ('Manjaro', 'Manjaro'),
        ('NixOS', 'NixOS'),
        ('openSUSE', 'openSUSE'),
        ('KaOS', 'KaOS'),
        ('Raspbian', 'Raspbian'),
        ('Sabayon', 'Sabayon'),
        ('Void', 'Void'),
        ('Slackware', 'Slackware')
        ])
    search_submit = SubmitField('Search')

class AddDistroForm(FlaskForm):
    recaptcha = RecaptchaField()
    distro_name = StringField('distro_name', validators=[DataRequired()])
    distro_logo = StringField('distro_logo', validators=[DataRequired()])
    form_submit = SubmitField('Submit')