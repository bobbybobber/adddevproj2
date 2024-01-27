from wtforms import Form, StringField, RadioField, SelectField, TextAreaField, validators, SubmitField
from wtforms.fields import EmailField, DateField, PasswordField
from flask_wtf import *
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms.validators import DataRequired


class CreateStaffForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    phonenumber = StringField('Phone Number', [validators.Length(min=8, max=8), validators.DataRequired()])
    email = EmailField('Email', [validators.Email(), validators.DataRequired()])
    address = StringField('Address', [validators.Length(min=1, max=150), validators.DataRequired()])
    password = PasswordField('Password', [validators.length(min=5, max=15), validators.data_required()])
    role = role = SelectField('Role',
                              choices=[('Manager', 'Manager'), ('Senior Consultant', 'Senior Consultant'),
                                       ('Consultant', 'Consultant')],
                              validators=[validators.DataRequired()])


class CreateBlogForm(FlaskForm):
    name = StringField('Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    comment = StringField('Comment', validators=[DataRequired()])
    # image = FileField('Image', validators=[FileRequired(), FileAllowed(['jpg', 'png'], 'Images only!')])
    image = FileField('Profile Picture', validators=[FileAllowed(['jpg', 'png'], "Images Only!")])


class CreateCustomerForm(Form):
    first_name = StringField('First Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    last_name = StringField('Last Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    email = EmailField('Email', [validators.Email(), validators.DataRequired()])
    password = PasswordField('Password', [validators.length(min=5, max=15), validators.data_required()])


class logininformation(Form):
    email = EmailField('Email', [validators.Email(), validators.DataRequired()])
    password = PasswordField('Password', [validators.length(min=5, max=15), validators.data_required()])


class DocumentUploadForm(Form):
    Name = StringField('Name', validators=[DataRequired()])
    Comment = StringField('Comment', validators=[DataRequired()])
    Image = FileField('Image', validators=[FileRequired(), FileAllowed(['jpg', 'png'], 'Images only!')])


class UploadFileForm(FlaskForm):
    file = FileField("Upload", validators=[DataRequired()])
    submit = SubmitField("Upload")


class ratingcomment(Form):
    email = EmailField('Email', [validators.Email(), validators.DataRequired()])
    comment = StringField('comment', validators=[DataRequired()])
    stars = StringField('stars', validators=[DataRequired()])


class ratingcomment2(Form):
    comment = StringField('comment', validators=[DataRequired()])
    stars = StringField('stars', validators=[DataRequired()])


class logininformation(Form):
    email = EmailField('Email', [validators.Email(), validators.DataRequired()])
    password = PasswordField('Password', [validators.length(min=5, max=15), validators.data_required()])


class emailfield(Form):
    email = EmailField('Email', [validators.Email(), validators.DataRequired()])


class otpfield(Form):
    otp = PasswordField('Password', [validators.length(min=0, max=6), validators.data_required()])


class resetpassword(Form):
    password1 = PasswordField('Password', [validators.length(min=5, max=15), validators.data_required()])
    password2 = PasswordField('Password', [validators.length(min=5, max=15), validators.data_required()])


class CreateProject(Form):
    phone = StringField('', [validators.Length(min=8), validators.DataRequired()])
    address = StringField('', [validators.Length(min=1, max=150), validators.DataRequired()])
    house_type = RadioField('', choices=[('AP', 'Appartment'), ('BUN', 'Bungalow'), ('HDB2', '2-Room HDB'),
                                         ('HDB3', '3-Room HDB'), ('HDB4', '4-Room HDB'),
                                         ('HDB5', '5-Room HDB')
        , ('CON', 'Condominium')], validators=[validators.DataRequired()])
    house_theme = RadioField('', choices=[('Scandanavian'), ('Luxury'), ('Modern-Luxury'),
                                          ('Traditional'), ('Contemporary'),
                                          ('Farmhouse')], validators=[validators.DataRequired()])
    comments = TextAreaField('', [validators.Optional()])


class CreateProject2(Form):
    address = StringField('', [validators.Length(min=1, max=150), validators.DataRequired()])
    comments = TextAreaField('', [validators.Optional()])


class UpdateCustomerForm(Form):
    first_name = StringField('First Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    last_name = StringField('Last Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    email = EmailField('Email', [validators.Email(), validators.DataRequired()])
    password = PasswordField('Password', [validators.length(min=5, max=15), validators.data_required()])
    image = FileField("Upload", validators=None)


class UpdateStaffForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    email = EmailField('Email', [validators.Email(), validators.DataRequired()])
    password = PasswordField('Password', [validators.length(min=5, max=15), validators.data_required()])
    image = FileField("Upload", validators=None)
class update_Project_form(Form):
    phone = StringField('', [validators.Length(min=8), validators.DataRequired()])
    address = StringField('', [validators.Length(min=1, max=150), validators.DataRequired()])
    house_type = RadioField('', choices=[('AP', 'Appartment'), ('BUN', 'Bungalow'), ('HDB2', '2-Room HDB'),
                                         ('HDB3', '3-Room HDB'), ('HDB4', '4-Room HDB'),
                                         ('HDB5', '5-Room HDB')
        , ('CON', 'Condominium')], validators=[validators.DataRequired()])
    house_theme = RadioField('', choices=[('Scandanavian'), ('Luxury'), ('Modern-Luxury'),
                                          ('Traditional'), ('Contemporary'),
                                          ('Farmhouse')], validators=[validators.DataRequired()])
    comments = TextAreaField('', [validators.Optional()])
    status = StringField('', [validators.Length(min=1), validators.DataRequired()])