from flask_wtf import Form
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Regexp, Email, EqualTo, Length, ValidationError

def name_exists(form, field):
	import createuserdb
	a = c.execute("SELECT users FROM users WHERE users='{}'".format(field.data))
	if len(a) == 0:
		return ValidationError('Username exists')

class RegisterForm(Form):
	username = StringField(
		'username',
		validators=[
		DataRequired(),
		Regexp(
			r'^[a-zA-Z0-9_]+$',
			message=('Username should be one word, letters,'
				'numbers, and underscores only.')
			)
		])
	email = StringField(
		'email',
		validators=[
		DataRequired(),
		Email()])
	password = PasswordField(
		'password',
		validators=[
		DataRequired(),
		Length(min=2),
		EqualTo('password2',message="Password don't match")
		])
	password2 = PasswordField(
		'Confirm Password',
		validators=[
		DataRequired()
		])

