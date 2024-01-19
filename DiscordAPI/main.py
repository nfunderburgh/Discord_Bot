import os
from flask import Flask, request, Response
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

port = int(os.environ.get("PORT", 5000))


@app.route('/')
def home():
    return '<h1>Welcome to the Prayer Requests</h1>'


if __name__ == '__main__':
    app.run(port=port)
