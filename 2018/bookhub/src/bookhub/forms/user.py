import os
import flask
from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import DataRequired, StopValidation, Length

from bookhub import app
from bookhub.models import User
from bookhub.helper import ip_address_in, get_remote_addr


class LoginForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    remember_me = BooleanField('remember_me', default=False)

    def validate_password(self, field):
        address = get_remote_addr()
        whitelist = os.environ.get('WHITELIST_IPADDRESS', '127.0.0.1')

        # If you are in the debug mode or from office network (developer)
        if not app.debug and not ip_address_in(address, whitelist):
            raise StopValidation(f'your ip address isn\'t in the {whitelist}.')

        user = User.query.filter_by(username=self.username.data).first()
        if not user or not user.check_password(field.data):
            raise StopValidation('Username or password error.')


class UserForm(FlaskForm):
    username = StringField('username', validators=[DataRequired(), Length(1, 64)])

    def validate_username(self, field):
        if field.data != current_user.username and User.query.filter_by(username=field.data).first():
            raise StopValidation('Username is exists.')
