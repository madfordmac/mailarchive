#!/usr/bin/env python3
import configparser
from flask import Flask
from flask import jsonify
from pymongo import MongoClient

# Read our config
config = configparser.ConfigParser()
config.read('config.ini')

# Setup database
maildb = MongoClient(config['DEFAULT']['host'], 27017)[config['DEFAULT']['db']]

# Setup Flask App
app = Flask.app(__name__)
app.secret_key = b'\xb3\xd7\x03\x95\x9ep`\x0bxg.\xda;\x90\x9fn'

@app.route('/')
def home():
	return "Home"

@app.route('/api/collections')
def collections():
	return jsonify([coll for coll in maildb.list_collection_names() if not coll.startswith("system")])