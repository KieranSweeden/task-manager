import os
from flask import (
    Flask, flash, render_template, 
    redirect, request, session, url_for)
from flask_pymongo import PyMongo

# MongoDB stores data in a JSON-like format called BSON
# To find documents from MongoDB we need to render the ObjectId
from bson.objectid import ObjectId

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


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True) # True presents detailed errors, False sends basic server warnings
