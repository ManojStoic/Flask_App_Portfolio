"""**********************************************************************************************************************************

Doc Notes:

    Web server - Stores and loads all static pages related to a website
    http.server -> python lib to implement http servers(web servers)
    Flask -> Python sync framework (analogy - micro-kitchen)
    Django -> Python sync framework (analogy - macro-kitchen)
    Never name a python module under Flask framework under the name  'flask.py' to avoid conflict
    To run the application, use the flask command or python -m flask.
    Before you can do that you need to tell your terminal the application to work with by exporting the FLASK_APP environment variable.
    > set FLASK_APP=hello
    > flask run
    * Running on http://127.0.0.1:5000/
    set FLASK_ENV=development    -> to turn on debug mode
    flask.render_template -> Renders a template from the template folder with the given context.
    Jinja template - {{4+5}} -> Flask built in templating language to evaluate the expression as python.
    url_for('folder','filename.ext') -> alternate Flask in built method/safer method for hardcoding the urls  (folder/filename.ext)
    variable rules -> add variables to the url section by placing the variables within the expression <variables> and pass it
                        to the jinga expression in html
    Browsers use the MIME type and not the file extension to determine how to process a URL, so it's important that Web server sends
        the correct MIME type in the response's Content-Type header (eg - text/javascript, text/html, image/png)
    Request object - To access incoming request data from client
    csv - module to write data to a csv file

    pip freeze > requirements.txt -> pythonic way to automcatically list all dependent libraries/packages
        into a txt file and use it in any machine instead of creating a new venv and downloading all packages.

**********************************************************************************************************************************"""

from flask import Flask, render_template, request, redirect
import json
import csv
app = Flask(__name__) # create the main instance of the Flask app under the name 'app'
# print(__name__)

@app.route("/")
def main_page():
    return render_template('index.html')

@app.route("/<string:pagename>")
def dynamic_page(pagename=None):
    return render_template(pagename)

def write_to_text(data):
    with open('./database.txt','a') as file:
        email = data['email']
        subject = data['subject']
        message = data['message']
        file.write(f'\n{email},{subject},{message}')
    with open('./contact.json','w') as json_file:
        json.dump(data,json_file)

def write_to_csv(data):
    with open('./database.csv','a', newline='') as csv_file:
        email = data['email']
        subject = data['subject']
        message = data['message']
        csv_writer = csv.writer(csv_file, delimiter=',',  quotechar='"',quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow([email,subject,message])

@app.route('/submit_form', methods=['POST', 'GET'])
def submit_form():
    if request.method == 'POST':
        try:
            data = request.form.to_dict()
            write_to_text(data)
            write_to_csv(data)
            return redirect('/greet.html')
        except:
            return "Data did not stored in the database"
    else: 
        return 'Something went wrong, Try again!'
