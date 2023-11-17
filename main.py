from flask import Flask, request, render_template
from bs4 import BeautifulSoup
import urllib
import urllib.request
from tensorflow.keras.models import load_model
import tensorflow as tf
from sklearn.preprocessing import MinMaxScaler
import numpy as np
from system.AI.lstm_machine import LstmMachine
from db.mongodb.mongodb_handler import MongoDBHandler
from machine.bithumb_machine import BithumbMachine
from bson import json_util

app = Flask(__name__)


@app.route("/test_model")
def model():
    #new_model = tf.keras.models.load_model('static/BITCOIN_MODEL_VER1')

    """loaded_model = load_model("static/BITCOIN_MODEL_VER1.h5", compile=False)
    predicted_values = [
        [35268000.0],
        [35616000.0],
        [34978000.0],
        [35019000.0],
        [34951000.0],
        [35246000.0],
        [35142000.0],
        [35319000.0],
        [35442000.0],
        [37023000.0],
        [37354000.0],
        [35268000.0],
        [35355000.0],
        [35351000.0],
        [35425000.0]]
    predicted_values.reverse()
    scaler=MinMaxScaler(feature_range=(0,1))
    predicted_values = scaler.fit_transform(
    np.array(predicted_values).reshape(-1, 1))
    predicted_values = np.array([predicted_values])

    predicted = loaded_model.predict(predicted_values)
    predicted_values.shape, predicted.shape

    print(predicted_values)

    predicted = scaler.inverse_transform(predicted)
    print(predicted)"""

    # test_value = [
    #     35268000.0,
    #     35616000.0,
    #     34978000.0,
    #     35019000.0,
    #     34951000.0,
    #     35246000.0,
    #     35142000.0,
    #     35319000.0,
    #     35442000.0,
    #     37023000.0,
    #     37354000.0,
    #     35268000.0,
    #     35355000.0,
    #     35351000.0,
    #     35425000.0
    # ]

    # db = MongoDBHandler("local", "AI", "predicted_data")
    # #db.set_db("AI", "predicted_data")
    # data = db.find_item()
    # print(data)
    # data = db.find_last_item()
    # print(data)
    # data = {"date": "2023-09-18", "price":35000000.0}
    # db.insert_item(data)
    # data = db.find_last_item()
    # print(data)
    # data = db.find_last_item()
    # print(data)

    # test_value.reverse()

    aiMachine = LstmMachine()
    machine = BithumbMachine()
    data = machine.get_local_data()

    data = aiMachine.data_processing(data)
    predicted_data = aiMachine.get_predict_value(data)
    print(predicted_data)
    return "예측값: " + str(predicted_data)
    #return "예측값: " + str(data["price"])  

@app.route("/test_bithumb")
def bithumb():
    machine = BithumbMachine()
    data = machine.get_local_data()

    return data


@app.route("/")
def home():
    html = """
    <html><head><meta charset="utf-8"></head>
  <body>
     날씨정보<br/>
    <form action = "/weather">
      <input type = "text" name = "city" />
      <input type = "submit"/>
    </form>
  </body>
</html>
"""
    return html


@app.route('/weather')
def weather():
    city = request.args.get("city", "")
    url = "https://search.naver.com/search.naver?&query="
    url = url + urllib.parse.quote_plus(city + "날씨")

    soup = BeautifulSoup(urllib.request.urlopen(url).read(), "html.parser")

    temp = soup.select("div.weather_graphic > div.temperature_text > strong")
    desc = soup.select("div._today > div.temperature_info > p")
    summary = soup.select("div._today > div.temperature_info > dl")

    return render_template("weather.html", weather={"city": city, "temp": temp[0].text, "desc": desc[0].text, "summary": summary[0].text})

@app.route("/get_predict_value")
def get_predict_value():
    db = MongoDBHandler(db_name="AI", collection_name="predicted_data")

    data = db.find_last_item(db_name="AI", collection_name="predicted_data")
    data['_id'] = str(data['_id'])
    #print(data)

    return data

@app.route("/get_basic_chart")
def get_basic_chart():
    db = MongoDBHandler(db_name="AI", collection_name="actual_data")
    actual_data = db.find_items_for_chart( db_name="AI", collection_name="actual_data", limit=14)
    predicted_data = db.find_items_for_chart(db_name="AI", collection_name="predicted_data", limit=15)

    actual_data_list = []
    predicted_data_list = []
    lables = []

    for i in actual_data:
        print(i)
        #i["_id"] = str(i["_id"])
        #del i["_id"]
        actual_data_list.append(i["close_price"])

    for i in predicted_data:
        print(i)
        #i["_id"] = str(i["_id"])
        #del i["_id"]
        lables.append(i["timestamp"])
        predicted_data_list.append(i["predicted_price"])

    chart_data = {}
    actual_data_list.reverse()
    predicted_data_list.reverse()
    lables.reverse()

    max_value = max(actual_data_list + predicted_data_list)
    min_value = min(actual_data_list + predicted_data_list)

    blank = (min_value + max_value) / 10
    chart_data["max"] = max_value + blank
    chart_data["min"] = min_value + blank
    chart_data["label"] = lables
    chart_data["datas"] = [
        {"label" : "actual_data", "datas" : actual_data_list}, 
        {"label" : "predicted_data", "datas" : predicted_data_list}]
    
    #chart_data["actual_data"] = [{"label" : "actual_data", "datas" : actual_data_list}, {"label" : "predicted_data", "datas" : predicted_data_list}]
    #chart_data["predicted_data"] = predicted_data_list

    return chart_data

app.run(debug=True)
