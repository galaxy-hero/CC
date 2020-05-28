import json
import time
import requests

from utils import api


def create_invoice(products, email):
    product_id = list(products.keys())[0]
    queried_product, message = api.get_product(product_id)
    if not queried_product:
        return False, message

    qty = min(products[product_id], queried_product['quantity'])
    amount = queried_product['price'] * qty

    headers = {
        "Content-Type": "application/json",
        'X-Accept-Version': '2.0.0'
    }

    invoices_url = 'https://bitpay.com/invoices'

    uid = int(time.time())
    data = {
        'currency': 'BTC',
        'price': amount,
        'fullNotifications': True,
        'transactionSpeed': 'high',
        'redirectURL': "https://chatapppython.azurewebsites.net/store",
        'token': '5tUruDVcRSi1UQ84vwuV7cM1gVTszqknREEzEVNyUfjG',
        'notificationURL': "https://chatapppython.azurewebsites.net/notification?id={}".format(uid)
    }

    response = requests.post(invoices_url, data=json.dumps(data), headers=headers)
    content = json.loads(response.content)
    if response.status_code == 200:
        _, _ = api.create_transaction(product_id, api.generate_id(email), amount, qty, uid)
        return content['data']['url'], 200

    else:
        return content['error'], 404
