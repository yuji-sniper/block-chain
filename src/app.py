from flask import Flask, jsonify

import blockchain
import wallet

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello, World!'
