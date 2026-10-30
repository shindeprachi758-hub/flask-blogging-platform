from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, TextAreaField, SelectField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError, Optional
from app.models import User, Category


class RegistrationForm(FlaskForm):
    """User account registration form with uniqueness checks."""
    username = StringField('Username', validators=[
        DataRequired(message='Username is required.'),
        Length(min=3, max=40, message='Username must be between 3 and 40 characters.')
    ])
    email = StringField('Email Address', validators=[
        DataRequired(message='Email is required.'),
        Email(message='Please provide a valid email address.')
    ])
    password = PasswordField('Password', validators=[
        DataRequired(message='Password is required.'),
        Length(min=6, max=128, message='Password must be at least 6 characters.')
    ])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(message='Please confirm your password.'),
        EqualTo('password', message='Passwords must match.')
    ])
    submit = SubmitField('Create Account')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data.strip()).first()
        if user:
            raise ValidationError('This username is already taken. Please choose another.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data.strip().lower()).first()
        if user:
            raise ValidationError('An account with this email address already exists.')


class LoginForm(FlaskForm):
    """User authentication login form."""
    email = StringField('Email Address', validators=[
        DataRequired(message='Email is required.'),
        Email(message='Please provide a valid email address.')
    ])
    password = PasswordField('Password', validators=[
        DataRequired(message='Password is required.')
    ])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class ProfileEditForm(FlaskForm):
    """User profile update form."""
    username = StringField('Username', validators=[
        DataRequired(),
        Length(min=3, max=40)
    ])
    email = StringField('Email Address', validators=[
        DataRequired(),
        Email()
    ])
    bio = TextAreaField('About You / Bio', validators=[
        Optional(),
        Length(max=300, message='Bio cannot exceed 300 characters.')
    ])
    submit = SubmitField('Update Profile')

    def __init__(self, original_user, *args, **kwargs):
        super(ProfileEditForm, self).__init__(*args, **kwargs)
        self.original_user = original_user

    def validate_username(self, username):
        if username.data.strip() != self.original_user.username:
            user = User.query.filter_by(username=username.data.strip()).first()
            if user:
                raise ValidationError('This username is already taken.')

    def validate_email(self, email):
        if email.data.strip().lower() != self.original_user.email.lower():
            user = User.query.filter_by(email=email.data.strip().lower()).first()
            if user:
                raise ValidationError('An account with this email address already exists.')


class PostForm(FlaskForm):
    """Blog post creation and editing form."""
    title = StringField('Post Title', validators=[
        DataRequired(message='Title is required.'),
        Length(min=5, max=200, message='Title must be between 5 and 200 characters.')
    ])
    summary = StringField('Brief Summary', validators=[
        Optional(),
        Length(max=300, message='Summary cannot exceed 300 characters.')
    ])
    category_id = SelectField('Category', coerce=int, validators=[
        DataRequired(message='Please select a category.')
    ])
    tags = StringField('Tags', validators=[
        Optional(),
        Length(max=150, message='Tags string is too long.')
    ])
    content = TextAreaField('Article Content', validators=[
        DataRequired(message='Content cannot be empty.')
    ])
    submit = SubmitField('Publish Post')


class CategoryForm(FlaskForm):
    """Category creation form."""
    name = StringField('Category Name', validators=[
        DataRequired(message='Category name is required.'),
        Length(min=2, max=60, message='Category name must be 2 to 60 characters.')
    ])
    description = TextAreaField('Description', validators=[
        Optional(),
        Length(max=255, message='Description cannot exceed 255 characters.')
    ])
    submit = SubmitField('Save Category')

    def validate_name(self, name):
        category = Category.query.filter_by(name=name.data.strip()).first()
        if category:
            raise ValidationError('A category with this name already exists.')


class CommentForm(FlaskForm):
    """Comment form on blog posts."""
    content = TextAreaField('Join the conversation...', validators=[
        DataRequired(message='Comment cannot be empty.'),
        Length(min=2, max=1000, message='Comment must be between 2 and 1000 characters.')
    ])
    submit = SubmitField('Post Comment')

