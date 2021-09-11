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
