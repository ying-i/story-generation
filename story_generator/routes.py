import uuid
from flask import Blueprint, current_app, render_template, request, url_for, session, redirect,flash
#flash is to display a message when something goes wrong.
from gradio_client import Client
import datetime 
#import base64
from story_generator.forms import StoryForm, RegisterForm, LoginForm, StoryPdfForm
import os
from werkzeug.utils import secure_filename
from story_generator.models import Story, User,StoryPdf
from dataclasses import asdict
from datetime import datetime
from passlib.hash import pbkdf2_sha256
# password hashing using the PBKDF2 algorithm with SHA-256.
import functools

pages = Blueprint("pages", __name__, template_folder="templates", static_folder="static")

client2 = Client("yiyii/RAG-2")
client3 = Client("yiyii/RAG-3")

stories = []

# define a login_required decorator that make sure user is logged in before accessing particular route
def login_required(route):
    @functools.wraps(route)
    def route_wrapper(*args, **kwargs): 
    # replace any of the endpoints that use this decorator on with route_wrapper(*args, **kwargs) function
    # *args, **kwargs will work with routes that have argument

    # route_wrapper(*args, **kwargs) function will check the email, if email doesn't exist, redirect to login
        if session.get("email") is None:
            return redirect(url_for(".login"))
        # otherwise, if email exist, run the original route itself
        return route(*args, **kwargs)
    return route_wrapper # the login_required(route) function just returns the inner function: route_wrapper

@pages.route("/", methods=["GET", "POST"])
@login_required
def index():
    #grab the current user's data
    user_data = current_app.db.user.find_one({"email": session["email"]})
    # create a User object
    user = User(**user_data)
    # # get all the story data to this template
    # story_data = current_app.db.story.find({})

    # get the stories by id
    story_data = current_app.db.story.find({"_id": {"$in": user.stories}})
    # create a Story object for each elements in story_data
    # through all the story. unpack story and then put into Story class
    stories = [Story(**story) for story in story_data]
    # ** is used for dictionary unpacking. 
    # stories is a list of story objects

    #get stories from storyPdf collection by using story's id in user collection
    storypdf_data = current_app.db.storyPdf.find({"_id": {"$in": user.stories}})
    stories_pdf = [StoryPdf(**story) for story in storypdf_data]

    #all_stories = stories + stories_pdf
    # sort by created time
    all_stories = sorted(stories + stories_pdf, key=lambda s: s.created_time, reverse=True)
    
    return render_template("index.html", all_stories=all_stories)
    # return render_template("index.html", stories_data=[])-----test index.html when these's no story
       

@pages.route("/register", methods=["GET", "POST"])
def register():
    if session.get("email"):
        return redirect(url_for(".index"))
        # def index() function in routes.py 
        # index refers to the index function within the current module or blueprint.
    #create form
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(
            _id=uuid.uuid4().hex, 
            email = form.email.data,
            # hash the password
            password = pbkdf2_sha256.hash(form.password.data)
            )
        # insert user data into MongoDB
        current_app.db.user.insert_one(asdict(user))
        # when type is success, the message "User registered successfully" will be flashed.
        flash("User registered successfully", "success")
        return redirect(url_for(".login"))
    return render_template("register.html", form=form) # url "/register" will go register.html


@pages.route("/login", methods=["GET", "POST"])
def login():
    # see if user is already logged in or not
    if session.get("email"):
        return redirect(url_for(".index"))
    # create form
    form = LoginForm()
    if form.validate_on_submit():
        # try to find a user in database with the email that we've received in the form.
        user_data = current_app.db.user.find_one({ "email": form.email.data})
        # if the email is not existing
        if not user_data:
            flash("login credentials not correct", category="danger")
            return redirect(url_for(".login"))

        user = User(**user_data)
        # if email is existing 
        # and validate the password is valid(if form.password.data and user.password are matched, it will return ture)
        if user and pbkdf2_sha256.verify(form.password.data, user.password):
            session["user_id"] = user._id
            session["email"] = user.email
            return redirect(url_for(".index"))
        # if the email exist and the password is incorrect, flash the following message
        flash("login credentials not correct", category="danger")
    return render_template("login.html", title="login", form=form) # url "/login" will go login.html

@pages.route("/logout")
def logout():
    # only keep current_theme, delete everthing else that's in the session
    current_theme = session.get("theme")
    session.clear()
    session["theme"] = current_theme
    return redirect(url_for(".login"))

@pages.route("/create", methods=["GET", "POST"])
@login_required
def create_story():
    form = StoryForm()
    # if request.method == "POST":
    # In Flask-WTF, form.validate_on_submit() is a method used to check if the form has been submitted and passes validation.
    if form.validate_on_submit():
        # get data from form
        # image = request.files["image"] #image_file is a binary file
        image = form.image.data 
        temperature = form.temperature.data
        max_new_tokens = form.max_new_tokens.data
        top_p = form.top_p.data
        repetition_penalty = form.repetition_penalty.data

        # Save the uploaded image 
        filename = secure_filename(image.filename) # make sure filename is right in Python's filename rules
        # image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        image_path = os.path.join(current_app.config['UPLOAD_IMAGES_DIR'], filename)
        # current_app is flask app in __init__.py
        image.save(image_path)

        print("Image file content:", image_path)
        print("Temperature:", temperature)
        print("Max new tokens:", max_new_tokens)
        print("Top_p:", top_p)
        print("Repetition penalty:", repetition_penalty)

        result = client2.predict(
                image_path,	# filepath  in 'Upload Image' Image component
                temperature,	# float (numeric value between 0.0 and 1.0) in 'Temperature' Slider component
                max_new_tokens,	# float (numeric value between 0 and 3000) in 'Max new tokens' Slider component
                top_p,	# float (numeric value between 0.0 and 1) in 'Top-p (nucleus sampling)' Slider component
                repetition_penalty,	# float (numeric value between 1.0 and 2.0) in 'Repetition penalty' Slider component
                api_name="/predict"
        )

        # only display date portion rather than 2024-04-15 12:57:44.947000
        formatted_date = datetime.now().strftime('%Y-%m-%d')

        # # to solve error: Not allowed to load local resource: file:///D:/life6/projectCode/gradio-python-client/queryAppViaApi-flaskApp-MongoDB-3/story_generator/static/uploads/happy-girl-blue-sky-17121618.jpg
        # path = 'uploads/images'
        # image_database_path = os.path.join(path, filename)
        
        # create a story object, Story is imported form story_generator.models
        story = Story(
            #create a unique identifier for the story
            _id = uuid.uuid4().hex, 
            # image = image_path,
            # image = image_database_path,
            image = filename,
            temperature = temperature,
            max_new_tokens = max_new_tokens,
            top_p = top_p,
            repetition_penalty = repetition_penalty,
            result = result,
            date = formatted_date
        )       

        print("story:", story)
        # image='D:\\life6\\projectCode\\gradio-python-client\\queryAppViaApi-flaskApp-MongoDB-3\\story_generator\\static\\uploads\\happy-girl-blue-sky-17121618.jpg'
        
        # insert data into mongoDB
        # asdict() function is provided by "dataclassed", it can convert a data class into a dictionary.
        # when we create a new story and insert it into MongoDB, it wil not only include _id,image, temprature,
        # max_new_tokens, top_p, repetition_penalty, result but also will include rating and date which are in models.py
        current_app.db.story.insert_one(asdict(story))

        # target the currently logged in user by using session["user_id"]: in def login(), we've saved the uer_id into session
        # {"$push": {"stories": story._id}}: add the current story's _id into User's stories in database
        current_app.db.user.update_one({"_id": session["user_id"]}, {"$push": {"stories": story._id}})

        # redirect to def story(_id: str) function when user click submit
        return redirect(url_for(".story", _id=story._id))
    return render_template("new_story.html", title="Create Story", form=form)
    # redirect is to sent to a different url web.
    # render_template is to render an html template and return the results as response to the client's request

@pages.route("/create_pdf", methods=["GET", "POST"])
@login_required
def create_story_pdf():
    form = StoryPdfForm()
    # if request.method == "POST":
    # In Flask-WTF, form.validate_on_submit() is a method used to check if the form has been submitted and passes validation.
    if form.validate_on_submit():
        # get data from form
        # image = request.files["image"] #image_file is a binary file
        image = form.image.data 
        pdfs = form.pdfs.data # return a list
        # pdfs = request.files.getlist('pdfs')
        print(f"Received {len(pdfs)} files")
        temperature = form.temperature.data
        max_new_tokens = form.max_new_tokens.data
        top_p = form.top_p.data
        repetition_penalty = form.repetition_penalty.data
        chunk_size = form.chunk_size.data
        chunk_overlap = form.chunk_overlap.data
        top_k = form.top_k.data

        # Save the uploaded image 
        filename = secure_filename(image.filename) # make sure filename is right in Python's filename rules
        # image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        image_path = os.path.join(current_app.config['UPLOAD_IMAGES_DIR'], filename)
        # current_app is flask app in __init__.py
        image.save(image_path)
        print("Image_path:", image_path)

        # save the uploaded pdfs
        pdf_paths = []
        pdf_filenames =[]
        for pdf in pdfs:
            pdf_filename = secure_filename(pdf.filename)
            print("PDF filename:", pdf_filename)
            pdf_path = os.path.join(current_app.config['UPLOAD_PDFS_DIR'], pdf_filename)
            print("PDF path:",pdf_path )
            pdf.save(pdf_path)
            pdf_paths.append(pdf_path)
            pdf_filenames.append(pdf_filename)

        result = client3.predict(
                image_path,	# filepath  in 'Upload Image' Image component
                pdf_paths,
                temperature,	# float (numeric value between 0.0 and 1.0) in 'Temperature' Slider component
                max_new_tokens,	# float (numeric value between 0 and 3000) in 'Max new tokens' Slider component
                top_p,	# float (numeric value between 0.0 and 1) in 'Top-p (nucleus sampling)' Slider component
                repetition_penalty,	# float (numeric value between 1.0 and 2.0) in 'Repetition penalty' Slider component
                chunk_size,
                chunk_overlap,
                top_k,
                api_name="/predict"
        )
        # only display date portion rather than 2024-04-15 12:57:44.947000
        formatted_date = datetime.now().strftime('%Y-%m-%d')

        # # to solve error: Not allowed to load local resource: file:///D:/life6/projectCode/gradio-python-client/queryAppViaApi-flaskApp-MongoDB-3/story_generator/static/uploads/happy-girl-blue-sky-17121618.jpg
        # path = 'uploads/images'
        # image_database_path = os.path.join(path, filename)
        
        # create a story object, Story is imported form story_generator.models
        storyPdf = StoryPdf(
            #create a unique identifier for the story
            _id = uuid.uuid4().hex, 
            # image = image_path,
            # image = image_database_path,
            image = filename,
            pdfs = pdf_filenames,
            temperature = temperature,
            max_new_tokens = max_new_tokens,
            top_p = top_p,
            repetition_penalty = repetition_penalty,
            chunk_size = chunk_size,
            chunk_overlap = chunk_overlap,
            top_k = top_k,
            result = result,
            date = formatted_date
        )       
        print("story:", storyPdf)
        # image='D:\\life6\\projectCode\\gradio-python-client\\queryAppViaApi-flaskApp-MongoDB-3\\story_generator\\static\\uploads\\happy-girl-blue-sky-17121618.jpg'
        
        # insert data into mongoDB
        # asdict() function is provided by "dataclassed", it can convert a data class into a dictionary.
        # when we create a new story and insert it into MongoDB, it wil not only include _id,image, temprature,
        # max_new_tokens, top_p, repetition_penalty, result but also will include rating and date which are in models.py
        current_app.db.storyPdf.insert_one(asdict(storyPdf))

        # target the currently logged in user by using session["user_id"]: in def login(), we've saved the uer_id into session
        # {"$push": {"stories": story._id}}: add the current story's _id into User's stories in database
        current_app.db.user.update_one({"_id": session["user_id"]}, {"$push": {"stories": storyPdf._id}})

        # redirect to def story(_id: str) function when user click submit
        return redirect(url_for(".story_pdf", _id=storyPdf._id))
    return render_template("new_story_pdf.html", title="Create Story", form=form)
    # redirect is to sent to a different url web.
    # render_template is to render an html template and return the results as response to the client's request 

@pages.route("/delete/<string:_id>")
@login_required
def delete(_id: str):
    current_app.db.story.delete_one({"_id": _id})
    return redirect(url_for(".index"))

@pages.route("/delete_pdf/<string:_id>")
@login_required
def delete_pdf(_id: str):
    current_app.db.storyPdf.delete_one({"_id": _id})
    return redirect(url_for(".index"))

# inorder to access a specific story, we need the story id
@pages.get("/story/<string:_id>")
@login_required
def story(_id: str): 
    # grab a story from database
    story_data = current_app.db.story.find_one({"_id": _id})
    # TypeError: story_generator.models.Story() argument after ** must be a mapping, not NoneType
    if story_data:
        # create a story with all the different values that are in MongoDB
        story= Story(**story_data)
        return render_template("story_details.html", story=story)
    else:
        return "story not found", 404

# inorder to access a specific story, we need the story id
@pages.get("/story_pdf/<string:_id>")
@login_required
def story_pdf(_id: str): 
    # grab a story from database
    story_data = current_app.db.storyPdf.find_one({"_id": _id})
    # TypeError: story_generator.models.Story() argument after ** must be a mapping, not NoneType
    if story_data:
        # create a story with all the different values that are in MongoDB
        storyPdf= StoryPdf(**story_data)
        return render_template("story_details_pdf.html", storyPdf=storyPdf)
    else:
        return "story not found", 404

@pages.get("/toggle-theme")
def toggle_theme():
    current_theme = session.get("theme")
    
    if current_theme == "dark":
        session["theme"] = "ligth"
    else:
        session["theme"] = "dark"
    return redirect(request.args.get("current_page"))
    # to make sure when user click the icon to change them, we still stay in the same page.






