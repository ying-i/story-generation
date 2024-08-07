from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed,MultipleFileField
from wtforms import FloatField, IntegerField, SubmitField, PasswordField, StringField
from wtforms.validators import InputRequired, NumberRange, Email, Length, EqualTo, DataRequired


# Flask wtf: Integration with WTForms. 
#            Secure Form with CSRF token. 
#            File upload that works with Flask-Uploads.

# step1. define a StoryForm class using Flask-WTF's FlaskForm in forms.py
# step2. using form in template(new_story.html)
class StoryForm(FlaskForm):
    # FlaskForm gives us added functionality to protect us from CSRF attacks.
    image = FileField("Upload Image", validators=[FileRequired(),FileAllowed(['jpg','png', 'gif', 'jpeg'])])
    temperature = FloatField("Temperature", validators=[InputRequired(), NumberRange(min=0.0, max=1.0)], default=0.9)
    max_new_tokens = IntegerField("Max New Tokens", validators=[InputRequired(), NumberRange(min=0, max=3000)], default=1500)
    top_p = FloatField("Top-p", validators=[InputRequired(), NumberRange(min=0.0, max=1.0)], default=0.9)
    repetition_penalty = FloatField("Repetition Penalty", validators=[InputRequired(), NumberRange(min=1.0, max=2.0)], default=1.2)
    submit = SubmitField("Generate") # SubmitField with Generate label

class StoryPdfForm(FlaskForm):
    image = FileField("Upload Image", validators=[FileRequired(), FileAllowed(['jpg','png', 'gif', 'jpeg'])])
    # select multiple files at once, instead of uploading files incremently!!!!!!!!!
    pdfs = MultipleFileField("Upload your PDFs", validators=[FileRequired(), FileAllowed(['pdf'], 'PDFs only!')], render_kw={'multiple': True})
    #pdfs = MultipleFileField("Upload your PDFs", validators=[FileAllowed(['pdf'], 'PDFs only!')])
    temperature = FloatField("Temperature", validators=[InputRequired(), NumberRange(min=0.0, max=1.0)], default=0.9)
    max_new_tokens = IntegerField("Max New Tokens", validators=[InputRequired(), NumberRange(min=0, max=3000)], default=1500)
    top_p = FloatField("Top-p", validators=[InputRequired(), NumberRange(min=0.0, max=1.0)], default=0.9)
    repetition_penalty = FloatField("Repetition Penalty", validators=[InputRequired(), NumberRange(min=1.0, max=2.0)], default=1.2)
    chunk_size = IntegerField("Chunk Size", validators=[InputRequired(), NumberRange(min=50, max=1024)], default=200)
    chunk_overlap = IntegerField("Chunk Overlap", validators=[InputRequired(), NumberRange(min=0, max=50)], default=20)
    top_k = IntegerField("Top-k", validators=[InputRequired(), NumberRange(min=1, max=100)], default=3)
    submit = SubmitField("Generate") # SubmitField with Generate label

# step1: define a RegisterForm
# step2: in routes.py import this RegisterForm 
class RegisterForm(FlaskForm):
    email = StringField("Email", validators=[InputRequired(), Email()])
    password = PasswordField(
        "Password", 
        validators=[InputRequired(), Length(min=4, message="Your password must contain at least 4 characters.")]
        )
    confirm_password = PasswordField(
        "Confirm Password",
        validators=[InputRequired(), EqualTo("password", message="This password did not match the one in the password field.")]
        # "password" is variable . message is custom error message 
    )
    submit = SubmitField("Register")

# step1: define a LoginForm
# step2: in routes.py import this LoginForm
class LoginForm(FlaskForm):
    email = StringField("Email", validators=[InputRequired(), Email()])
    password = PasswordField("Password", validators=[InputRequired()])
    submit = SubmitField("Login")
