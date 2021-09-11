# Deploying Machine Learning Model using Flask

When a data scientist develops a machine learning model, the ultimate goal is to make it available in production. Deployment of machine learning models or putting models into production means making your models available to the end users.

In this article, we'll look at how to deploy a machine learning model, for predicting avocado prices, as a RESTful API using Flask.

## Flask

Flask is one of the most popular web frameworks written in Python. It is designed to make getting started quick and easy, with the ability to scale up to complex applications. At its core, Flask is simple yet extensible, which is perfect for developing RESTful APIs.

## Setup Environment

Before we can build our application, we need to install some dependencies.

To verify if Python is installed and configured correctly on your system, Open the terminal and type in the command `python --version` else you’ll need to install [Python](https://www.python.org/) 3.6+ on your system.

```bash
$ python --version
Python 3.7.6
```

Now We'll start by creating our project's work directory for our project.

Run `mkdir flask-ml` to create our working directory.

```bash
mkdir flask-ml
cd flask-ml
```

Add below dependencies to the requirements file:

```bash
flask
pandas==1.1.1
pystan==2.19.1.1
fbprophet==0.6.0
```

Now, Install the dependencies:

```bash
pip install -r requirements.txt
```

We have setup required environment, Let's create a simple app.

## Create a simple app

The reason I like Flask is because of the simplicity of getting a basic web page running — we can do this in only a few lines of code.

Create the `flask-ml/app/app.py` file. open `app.py` in code editor and add the following lines of code:

```python
# import packages
from flask import Flask

# create an instance of the flask app
app = Flask(__name__)

# map home page (/) to `say_hello()` using python decorator
@app.route('/')
def say_hello():
    return 'Hello, World!'
    
if __name__ == "__main__":
    app.run(debug=True)
```

Note that we set `debug=True` so we don't have to reload our server each time we make a change in our code.

## Run the app

Run below command:

```bash
python ./app/app.py
```

Now we can go to `http://127.0.0.1:5000/` and inspect our first running app!

## Machine Learning Model

The model that we'll deploy uses [Prophet](https://facebook.github.io/prophet/) to predict avocado prices. You can learn more about how to create machine learning model using Prophet from [here](https://github.com/imnileshd/time-series-prophet). We'll use the same model here and forecast the prices for next 7 days.

Create the `flask-ml/app/model.py` file. open `model.py` in code editor and add the following lines of code:

```python
import os
import json
import datetime
import pandas as pd
from fbprophet.serialize import model_from_json

def forecast(days=7):

    model_file = "app\models\model_avocados_avg_prices.json"

    # check if model is exists
    if not os.path.exists(model_file):
        return False

    # load model
    with open(model_file, 'r') as fin:
        model = model_from_json(json.load(fin))  
    
    # future = model.make_future_dataframe(periods=days, include_history=False)

    # generate future dates
    dates = pd.date_range(start=datetime.datetime.now().date(), end=datetime.datetime.now().date() + datetime.timedelta(days=days), freq='D')

    # create future dataframe using dates
    future = pd.DataFrame({"ds": dates})

    # forecast on future dataframe
    forecast = model.predict(future)

    # return required results
    return forecast[['ds', 'yhat']].tail(days).to_dict("records")
```

## Create New Routes

Now we'll add a `/forecast` endpoint by importing `forecast` function from `model.py` into `app.py` like below:

```python
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
```

Here, in the new `get_forecast` view function, we passed `days` to predict or forecast the prices. This function will return json object containing future dates with forecasted values based on given `days`.

## Testing Endpoint

Now in a new terminal window, use curl to test the endpoint:

```bash
curl --location --request POST 'http://127.0.0.1:5000/forecast' \
--header 'Content-Type: application/json' \
--data-raw '{
    "days":2
}'
```

You should see output something like:

```json
{
    "forecast": [
        {
            "ds": "Mon, 13 Sep 2021 00:00:00 GMT",
            "yhat": 0.2685102248435055
        },
        {
            "ds": "Tue, 14 Sep 2021 00:00:00 GMT",
            "yhat": 0.27008814433702905
        }
    ]
}
```

Finally, our Machine Learning model is able to forecast with a RESTful API using Flask.

## Conclusion

In this article, we looked at how to deploy a machine learning model, for predicting prices, as a RESTful API using Flask.

I hope this article was valuable to you and that you learned something that you can use in your own work.

Go ahead and clone the repos [flask-ml](https://github.com/imnileshd/flask-ml) to view the full code of the project.

Happy Coding!
