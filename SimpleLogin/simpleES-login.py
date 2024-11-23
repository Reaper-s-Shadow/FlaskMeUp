from flask import Flask, render_template, request, redirect, url_for, session
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
import secrets
from dotenv import load_dotenv
import os

# Create main app container and link to html templates
# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = 
app = Flask(__name__, template_folder=r'YOUR-TEMPLATE-DIRECTORY')

# Check if local environment has a flask secret key already, if not, create and store a random one.
# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = 
try:
    app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY')
except:
    secret_key = secrets.token_hex(32)
    SECRET_KEY=secret_key
    load_dotenv()
    secret_key = os.getenv("FLASK_SECRET_KEY")
    app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY')

# Create app function to load page and handle submitted data
# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = 
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        access = request.form['access']
        es = Elasticsearch(
            access, # Elasticsearch location, must be full url (https....)
            basic_auth=(username, password), # basic auth: (username, password)
            # api_key=, # can use API key over basic auth
            request_timeout=30
        )
        if es.ping():
            return 'Welcome, {}!'.format(username)
        else:
            return 'Invalid username or password.'         

    return render_template('login_page.html')

if __name__ == "__main__":
    app.run(host="localhost",port=int(5000),debug=True)
