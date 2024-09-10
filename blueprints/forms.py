from wsgiref.validate import validator

import wtforms
from wtforms.validators import Email, length, EqualTo ,input_required
from models import UserModel

class RegisterForm(wtforms.Form):
    username = wtforms.StringField(validators=[length(min=4, max=20, message='Invalid username')])
    password = wtforms.StringField(validators=[length(min=6, max=20, message='Invalid password')])
    password_confirm = wtforms.StringField(validators=[EqualTo('password', message='Passwords must match')])
    email = wtforms.StringField(validators=[Email(message='Invalid Email')])

    #邮箱唯一性验证
    def validate_email(self, field):
        email = field.data
        user = UserModel.query.filter_by(email=email).first()
        if user:
            raise wtforms.ValidationError(message='Email already registered')


class LoginForm(wtforms.Form):
    password = wtforms.StringField(validators=[length(min=6, max=20, message='Invalid password')])
    email = wtforms.StringField(validators=[Email(message='Invalid Email')])


class QuestionForm(wtforms.Form):
    title = wtforms.StringField(validators=[length(min=1, max=100, message='Invalid title')])
    content = wtforms.StringField(validators=[length(min=1, message='Invalid content')])

class AnswerForm(wtforms.Form):
    content = wtforms.StringField(validators=[length(min=1, message='Invalid content')])
    question_id = wtforms.IntegerField(validators=[input_required(message='Question id is required')])