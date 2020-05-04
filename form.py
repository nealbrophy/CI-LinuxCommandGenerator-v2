from flask_wtf import FlaskForm,RecaptchaField, CSRFProtect
from wtforms import (StringField,SubmitField,
                         DateTimeField, RadioField,
                         SelectField,TextAreaField, DateField)
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired


csrf = CSRFProtect()

class WTForm_with_ReCaptcha(FlaskForm):
    form_recaptcha = RecaptchaField()
    form_name = StringField('app_name', validators=[DataRequired()])
    form_distro = SelectField('app_distro', validators=[DataRequired()], choices=[
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
    # form_distro = SelectField('app_distro', choices=[distro for distro in distros_for_form])
    form_selected_distro = StringField('selected_distro')
    form_url = StringField('app_url')
    form_instruction = StringField('app_instruction', validators=[DataRequired()])
    form_command = StringField('app_command', validators=[DataRequired()])
    form_submit = SubmitField('Submit')

class DeleteForm(FlaskForm):
    form_recaptcha = RecaptchaField()
    form_name = StringField('app_name', validators=[DataRequired()])
    # form_distro = SelectField('app_distro', choices=[distro for distro in distros_for_form])
    form_selected_distro = StringField('selected_distro')
    form_url = StringField('app_url')
    form_instruction = StringField('app_instruction', validators=[DataRequired()])
    form_command = StringField('app_command', validators=[DataRequired()])
    form_submit = SubmitField('Delete')

class EditForm(FlaskForm):
    form_recaptcha = RecaptchaField()
    form_name = StringField('app_name', validators=[DataRequired()])
    form_url = StringField('app_url')
    form_instruction = StringField('app_instruction', validators=[DataRequired()])
    form_command = StringField('app_command', validators=[DataRequired()])
    form_submit = SubmitField('Update')

class EmailForm(FlaskForm):
    email_recaptcha = RecaptchaField()
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