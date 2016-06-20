from wtforms import form, fields, validators
from werkzeug.security import check_password_hash
from .. import db
from ..models import User
from flask_admin.form import BaseForm

# Define login and registration forms (for flask-login)
class LoginForm(form.Form):
    login = fields.TextField(validators=[validators.required()])
    password = fields.PasswordField(validators=[validators.required()])

    def validate_login(self, field):
        user = self.get_user()
        if user is None:
            raise validators.ValidationError('Invalid user')
        if not check_password_hash(user.password, self.password.data):
            raise validators.ValidationError('Invalid password')

    def get_user(self):
        return db.session.query(User).filter_by(login=self.login.data).first()


class RegistrationForm(form.Form):
    login = fields.TextField(validators=[validators.required()])
    email = fields.TextField()
    password = fields.PasswordField(validators=[validators.required()])

    def validate_login(self, field):
        if db.session.query(User).filter_by(login=self.login.data).count() > 0:
            raise validators.ValidationError('Duplicate username')

class CreateUserForm(BaseForm):
    login = fields.TextField(validators=[validators.required()])
    email = fields.TextField(validators=[validators.required()])
    role_id = fields.SelectField()
    password = fields.PasswordField(validators=[validators.required()])

    def validate_login(self, field):
        user = self.get_user()
        if user is not None:
            raise validators.ValidationError('user exists')

    def get_user(self):
        return db.session.query(User).filter_by(login=self.login.data).first()

class UserEditForm(BaseForm):
    login = fields.TextField(validators=[validators.required()])
    email = fields.TextField(validators=[validators.required()])
    role_id = fields.SelectField()
    password = fields.PasswordField(validators=[validators.required()])

