from flask import Flask
from gradio_client import Client
import os
from pymongo import MongoClient
from dotenv import load_dotenv
from story_generator.routes import pages

load_dotenv()
# will go into .env file, and populate environment variables(MONGODB_URI)

def create_app():
    app = Flask(__name__)
    # RuntimeError: The session is unavailable because no secret key was set.  Set the secret_key on the application to something unique and secret.
    app.config["SECRET_KEY"] = os.environ.get(
        "SECRET_KEY", "pf9Wkove4IKEAXvy-cQkeDPhv9Cb3Ag-wyJILbq_dFw"
    )

    # mongoDB_client = MongoClient("mongodb://localhost:27017")
    # hide MongoDB details from GitHub. access environment variable
    mongoDB_client = MongoClient(os.getenv("MONGODB_URI"))
    
    # connect to the stories database, and put the database value inside the app
    app.db = mongoDB_client.stories
    # app.db = mongoDB_client.get_default_database()
    # Error: No default database name defined or provided

    # Gradio python client Doc: For certain inputs, such as images, you should pass in the filepath or URL to the file.
    # save the uploaded image temporarily on my server and then pass the file path to the Gradio API.
    # Define a folder to store temporary images
    # UPLOAD_FOLDER = 'uploads'
    # app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDE
    # if not os.path.exists(UPLOAD_FOLDER):
    #   os.makedirs(UPLOAD_FOLDER)
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    STATIC_DIR = os.path.join(BASE_DIR, 'static')
    TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')
    # move UPLOAD_IMAGES_DIR under static folder
    UPLOAD_IMAGES_DIR = os.path.join(STATIC_DIR, 'uploads/images') 
    UPLOAD_PDFS_DIR = os.path.join(STATIC_DIR, 'uploads/pdfs')
     # use app.config directly instead of current_app.config
    app.config['UPLOAD_IMAGES_DIR'] = UPLOAD_IMAGES_DIR
    app.config['UPLOAD_PDFS_DIR'] = UPLOAD_PDFS_DIR

    app.register_blueprint(pages)
    return app
    # running on http://127.0.0.1:5000/
    # pip show gradio_client

