from flask import Flask, jsonify, render_template, request
from urllib.request import Request, urlopen
import json, http.client, urllib.parse

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True


@app.route('/', methods=['GET'])
def home():
    return render_template("index.html")


@app.route("/chat", methods=['GET'])
def chat():
    return render_template("chat.html")

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

@app.route("/autosuggest", methods=['GET'])
def autosuggest():
    host = 'api.cognitive.microsoft.com'
    path = '/bing/v7.0/Suggestions'
    mkt = 'en-US'
    query = request.args.get('text')

    params = '?mkt=' + mkt + '&q=' + query

    headers = {
        'Ocp-Apim-Subscription-Key': '3cf388703aa7433fa7ad796111fcbab2'
    }
    
    conn = http.client.HTTPSConnection(host)
    conn.request ("GET", path + params, None, headers)
    response = conn.getresponse ()
    result = response.read()

    return(json.dumps(json.loads(result), indent=4))


if __name__ == '__main__':
    app.run(debug=True)
