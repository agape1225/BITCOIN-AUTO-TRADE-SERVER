from pip._vendor import requests
import json


class BithumbMachine:

    def get_ticker_details(self, order_currency, payment_currency):

        url = "https://api.bithumb.com/public/ticker/" + order_currency + "_" + payment_currency
        headers = {"accept": "application/json"}
        response = requests.get(url, headers=headers)

        print(response.text)
    
    def get_local_data(self):
        url = "https://api.bithumb.com/public/candlestick/BTC_KRW/24h"

        headers = {"accept": "application/json"}
        response = requests.get(url, headers=headers)
        res = json.loads(response.text)

        return [[eval(sublist[2]) + 0.0] for sublist in res["data"][-15:]]