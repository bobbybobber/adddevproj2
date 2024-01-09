from wtforms import Form, StringField, RadioField, SelectField, TextAreaField, validators, SubmitField
from wtforms.fields import EmailField, DateField, PasswordField
from flask_wtf import *
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms.validators import DataRequired

class CreateStaffForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    phonenumber = StringField('Phone Number',[validators.Length(min=8, max=8), validators.DataRequired()])
    email = EmailField('Email', [validators.Email(), validators.DataRequired()])
    address = StringField('Address', [validators.Length(min=1, max=150), validators.DataRequired()])
    password = PasswordField('Password', [validators.length(min=5, max=15), validators.data_required()])
class CreateBlogForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    comment = StringField('Comment', validators=[DataRequired()])
    # image = FileField('Image', validators=[FileRequired(), FileAllowed(['jpg', 'png'], 'Images only!')])
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


class CreateProject(Form):
    first_name = StringField('First Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    last_name = StringField('Last Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    phone = StringField('Phone', [validators.Length(min=8), validators.DataRequired()])
    email = EmailField('Email', [validators.Email(), validators.DataRequired()])
    address = StringField('House address', [validators.Length(min=1, max=150), validators.DataRequired()])
    house_type = RadioField('House Type', choices=[('AP', 'Appartment'), ('BUN', 'Bungalow'), ('HDB2', '2-Room HDB'),
                                                   ('HDB3', '3-Room HDB'), ('HDB4', '4-Room HDB'),
                                                   ('HDB5', '5-Room HDB')
        , ('CON', 'Condominium'), validators.DataRequired()])
    house_theme = RadioField('House Theme', choices=[('Scandanavian'), ('Luxury'), ('Modern-Luxury'),
                                                     ('Traditional'), ('Contemporary'),
                                                     ('Farmhouse'), ('CON', 'Condominium'), validators.DataRequired()])
    comments = TextAreaField('Additional Request', [validators.Optional()])

