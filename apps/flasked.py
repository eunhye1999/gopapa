import json
from flask import Flask, make_response, current_app, jsonify
import sqlite3
from flask import g


app = Flask(__name__)
# app.config.from_object('settings')

@app.route('/')
def hello():
    return "Welcome to WebService"