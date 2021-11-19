import os
from flask import Flask

# Only import the env file if it exists within the directory
if os.path.exists("env.py"):
    import env


app = Flask(__name__) # Instance of flask within a variable


@app.route("/") # "/" refers to the default route
def hello():
    return "Hello World .... again!"


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True) # True presents detailed errors, False sends basic server warnings
