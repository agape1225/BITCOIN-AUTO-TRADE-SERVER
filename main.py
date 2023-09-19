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


app.run(debug=True)
