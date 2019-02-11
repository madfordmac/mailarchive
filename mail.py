#!/usr/bin/env python3
import configparser
from flask import Flask
from flask import render_template
from flask import jsonify
from email.header import decode_header
from pymongo import MongoClient
from bson.objectid import ObjectId

# Read our config
config = configparser.ConfigParser()
config.read('config.ini')

def headerCleanup(header):
	if isinstance(header, ObjectId):
		return str(header)
	else:
		clean = ""
		for text, encoding in decode_header(header):
			if encoding:
				clean += text.decode(encoding)
			elif isinstance(text,str):
				clean += text
			elif isinstance(text,bytes):
				clean += text.decode('utf-8')
			else:
				clean += " (???) "
				app.logger.warning("Unexpected header content: %r", text)
		return clean

# Setup database
maildb = MongoClient(config['DEFAULT']['host'], 27017)[config['DEFAULT']['db']]

# Setup Flask App
app = Flask(__name__)
app.secret_key = b'\xb3\xd7\x03\x95\x9ep`\x0bxg.\xda;\x90\x9fn'

@app.route('/')
def home():
	return render_template('master')

@app.route('/api/mailboxes')
def collections():
	return jsonify([coll for coll in maildb.list_collection_names() if not coll.startswith("system")])

@app.route('/api/someMessages/<mailbox>')
def someMessages(mailbox):
	return jsonify([{hdr: headerCleanup(msg[hdr]) for hdr in msg} for msg in maildb[mailbox].find(limit=10, projection=['X-Original-To','From','Received','Subject'])])