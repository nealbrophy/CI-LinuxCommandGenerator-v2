from flask_wtf import FlaskForm,RecaptchaField, CSRFProtect
from wtforms import (StringField,SubmitField,
                         DateTimeField, RadioField,
                         SelectField,TextAreaField, DateField)
from wtforms.validators import DataRequired

csrf = CSRFProtect()

class WTForm_with_ReCaptcha(FlaskForm):
    csrf = False
    form_recaptcha = RecaptchaField()
    form_name = StringField('app_name', validators=[DataRequired()])
    form_distro = SelectField('app_distro', validators=[DataRequired()], choices=[
        ('', 'Select distro'), 
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