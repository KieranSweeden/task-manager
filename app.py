import os
from flask import (
    Flask, flash, render_template, 
    redirect, request, session, url_for)
from flask_pymongo import PyMongo

# MongoDB stores data in a JSON-like format called BSON
# To find documents from MongoDB we need to render the ObjectId
from bson.objectid import ObjectId

# Get werzeug's security features
from werkzeug.security import generate_password_hash, check_password_hash

# Only import the env file if it exists within the directory
if os.path.exists("env.py"):
    import env


app = Flask(__name__) # Instance of flask within a variable

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

# Setup instance of PyMongo, inserting our Flask app as an argument
# This is the final step to ensure the flask app is communicating
# with the Mongo database
mongo = PyMongo(app)


@app.route("/") # "/" refers to the default route
@app.route("/get_tasks")
def get_tasks():
    tasks = mongo.db.tasks.find()
    return render_template("tasks.html", tasks=tasks)

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":

        # check is username already exists in database
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})
        
        if existing_user:
            flash("Username already exists")
            return redirect(url_for("register"))

        # Stores name attribute values when form is submitted
        register = {
            "username": request.form.get("username").lower(),
            "password": generate_password_hash(request.form.get("password"))
        }

        # Insert the dictionary to the database
        mongo.db.users.insert_one(register)

        # Put the new user into 'session' cookie
        session["user"] = request.form.get("username").lower()
        flash("Registration Successful")
    return render_template("register.html")


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True) # True presents detailed errors, False sends basic server warnings
