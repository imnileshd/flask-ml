# import packages
from flask import Flask, jsonify, abort, request
from model import forecast

# create an instance of the flask app
app = Flask(__name__)

# map home page (/) to `say_hello()` using python decorator
@app.route('/')
def say_hello():
    return 'Hello, World!'


@app.route("/forecast", methods=["POST"])
def get_forecast():

    if not request.json or not 'days' in request.json:
        predictions = forecast()
    else:
        predictions = forecast(request.json['days'])

    if not predictions:
        abort(400, "Model not found.")

    return jsonify({"forecast": predictions})


if __name__ == "__main__":
    app.run(debug=True)
