import time
import json
import hashlib
import requests

api_url = "https://chatroomapilinux2.azurewebsites.net/"


def generate_id(email):
    secret = "Trecem la CC"

    _id = hashlib.sha256((email + secret).encode('utf-8'))

    return _id.hexdigest()


def user_exists(email):
    _id = generate_id(email)
    request_url = api_url + "user/id={}".format(_id)
    response = requests.get(request_url)

    if response.status_code != 200:
        return False, "Request returned status_code {}".format(response.status_code)

    data = json.loads(response.content)
    if data['status_code'] == 200:
        return True, data['message']

    return False, data['message']


def get_userInfo(email):
    _id = generate_id(email)
    request_url = api_url + "user/id={}".format(_id)
    response = requests.get(request_url)

    if response.status_code != 200:
        return False, "Request returned status_code {}".format(response.status_code)

    data = json.loads(response.content)
    if data['status_code'] == 200:
        return data['data'][0], data['message']

    return False, data['message']


def create_user(email):
    _id = generate_id(email)
    request_url = api_url + "user"
    data = {
        "userId": _id,
        "email": email
    }

    response = requests.post(request_url, data)
    if response.status_code != 200:
        return False, "Request returned status_code {}".format(response.status_code)

    data = json.loads(response.content)
    if data['status_code'] == 200:
        return True, data['message']

    return False, data['message']


def get_product(product_id):
    request_url = api_url + "product/id={}".format(product_id)
    response = requests.get(request_url)

    if response.status_code != 200:
        return False, "Request returned status_code {} -- {}".format(response.status_code, response.content)

    data = json.loads(response.content)
    if data['status_code'] == 200:
        return data['data'][0], data['message']

    return None, "API returned {} -- {}".format(data['status_code'], data['message'])


def get_products():
    request_url = api_url + "products"
    response = requests.get(request_url)

    if response.status_code != 200:
        return False, "Request returned status_code {} -- {}".format(response.status_code, response.content)

    data = json.loads(response.content)
    if data['status_code'] == 200:
        return data['data'], data['message']

    return [], "API returned {} -- {}".format(data['status_code'], data['message'])


def get_rooms():
    request_url = api_url + "topics"
    response = requests.get(request_url)

    if response.status_code != 200:
        return False, "Request returned status_code {} -- {}".format(response.status_code, response.content)

    data = json.loads(response.content)
    if data['status_code'] == 200:
        return data['data'], data['message']

    return [], "API returned {} -- {}".format(data['status_code'], data['message'])


def create_topic(name):
    request_url = api_url + "topic"
    data = {
        "name": name,
        "topicId": int(time.time())
    }

    response = requests.post(request_url, data)
    if response.status_code != 200:
        return False, "Request returned status_code {} -- {}".format(response.status_code, response.content)

    data = json.loads(response.content)
    if data['status_code'] == 200:
        return True, data['message']

    return False, "API returned {} -- {}".format(data['status_code'], data['message'])


def create_transaction(product_id, user_id, amount, qty, transaction_id):
    request_url = api_url + "transaction"
    data = {
        "productId": product_id,
        "userId": user_id,
        "amount": amount,
        "quantity": qty,
        "transactionId": transaction_id
    }

    response = requests.post(request_url, data)
    if response.status_code != 200:
        return False, "Request returned status_code {} -- {}".format(response.status_code, response.content)

    data = json.loads(response.content)
    if data['status_code'] == 200:
        return True, data['message']

    return False, "API returned {} -- {}".format(data['status_code'], data['message'])
