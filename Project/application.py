import os
import json
import hashlib
import requests

from utils import api, payment
from urllib.request import Request, urlopen
from urllib.parse import urlencode
from flask import Flask, jsonify, render_template, request, redirect, make_response, session

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.secret_key = "RYc9wqxsrf"


@app.route('/', methods=['GET'])
def home():
    logged_in = session.pop('loggedIn', None)

    return render_template("index.html", loggedIn=logged_in)


@app.route('/signin', methods=['POST'])
def signin():
    logged_in = session.pop('loggedIn', None)
    if logged_in == '1':
        return redirect('/', code=307)

    try:
        email = request.args.get('email')

    except:
        return render_template("error.html"), 404

    check, message = api.user_exists(email)
    if check:
        session['loggedIn'] = '1'
        session['email'] = email

        return render_template("index.html", loggedIn='1'), 200

    else:
        check, message = api.create_user(email)
        if check:
            session['loggedIn'] = '1'
            session['email'] = email

            return render_template("index.html", loggedIn='1'), 201

        else:
            return render_template("error.html"), 404


@app.route("/chat", methods=['GET'])
def chat():
    rooms, message = api.get_rooms()
    if rooms == []:
        return redirect("/error?msg=it happens"), 404

    return render_template("chat.html", rooms=rooms)


@app.route("/topic", methods=["POST"])
def create_topic():
    roomname = request.get_data().split(b"=")[1]

    if roomname:
        result, message = api.create_topic(roomname)
        print(result, message)
        if result:
            return redirect("/chat", code=302)

        else:
            return redirect("/error?msg={}".format("couldn't create new topic"), code=401)

    else:
        return redirect("/error?msg={}".format("invalid request"), code=401)


@app.route("/store", methods=['GET'])
def store():
    return render_template("store-homepage.html", param=get_shop_data())


@app.route("/laptops", methods=['GET'])
def laptops():
    return render_template("store-categorypage.html", param=get_category_shop("laptops"))


@app.route("/pcs", methods=['GET'])
def pcs():
    return render_template("store-categorypage.html", param=get_category_shop("pcs"))


@app.route("/accessories", methods=['GET'])
def accessories():
    return render_template("store-categorypage.html", param=get_category_shop("accessories"))


@app.route("/software", methods=['GET'])
def sofware():
    return render_template("store-categorypage.html", param=get_category_shop("software"))


@app.route("/courses", methods=['GET'])
def courses():
    return render_template("store-categorypage.html", param=get_category_shop("courses"))


@app.route("/translate", methods=['POST'])
def translate():
    data = request.json
    headers = {
        'Ocp-Apim-Subscription-Key': 'afa0aa27aa644d62a85f1d31aa26ce4d',
        "Content-Type": "application/json"
    }

    print(data)

    url = "https://andreeaarsene.cognitiveservices.azure.com/translator/text/v3.0/translate?api-version=3.0&to=es"
    r = Request(url, json.dumps(data).encode(), headers=headers)
    req = urlopen(r)

    return jsonify(json.loads(req.read().decode()))


@app.route("/check", methods=["POST"])
def check():
    data = request.json
    headers = {
        'Ocp-Apim-Subscription-Key': '9a4557b9325546be922712b8d7cd63b1',
        "Content-Type": 'application/x-www-form-urlencoded'
    }

    params = {
        'mkt': 'en-us',
        'mode': 'proof'
    }

    url = "https://api.cognitive.microsoft.com/bing/v7.0/SpellCheck"
    r = requests.post(url, headers=headers, data=data, params=params)

    text = ""
    if r.status_code == 200:
        print(r.content)
        text = data["text"]
        content = json.loads(r.content)
        flagged_tokens = content['flaggedTokens']
        for token in flagged_tokens:
            print(token)
            text = text.replace(token["token"], token["suggestions"][0]["suggestion"])

    return jsonify({"spell_checked": text})


@app.route("/payment", methods=["POST"])
def make_payment():
    products = request.get_json()

    url, status_code = payment.create_invoice(products, session['email'])

    if status_code == 200:
        return url, 200

    return url, 404


def get_shop_data():
    params = list()
    nickname = 'Anonymous'
    points = 0
    if 'email' in session:
        user, message = api.get_userInfo(session['email'])

        if user:
            nickname = str(user['email']).split('@')[0]
            points = user['fidelity']
    params.append(nickname)
    params.append(points)

    return params


@app.route("/error", methods=["GET"])
def error():
    if 'msg' not in request.args:
        return render_template("error.html")

    return render_template("error.html", error_message=request.args['msg'])


@app.route("/notification")
def notify_transaction():
    print(request.args.get("id", None))
    pass


def get_category_shop(category):
    params = list()
    params.append(get_shop_data())

    data, message = api.get_products()

    if data != []:
        li = list()
        for elem in data:
            if elem["category"] == category:
                li.append(elem)

        params.append(li)
        return params

    return render_template("error.html", error_message=message), 404


if __name__ == '__main__':
    app.run(debug=True)
