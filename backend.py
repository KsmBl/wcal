#!/usr/bin/env python3

SYNC_LOCATION = "./syncedHighlights/"
LOGIN_CODE = "420621"
PORT = "4200"

# run http server
## get: array for synced files
## get: md5 hash value for each synced file
## post: new file
## post: update file

from flask import Flask, request
import json

app = Flask(__name__)

@app.route('/test', methods=['GET'])
def handle_get():
	return 'pog'

@app.route("/upload", methods=["POST"])
def upload():
	data = request.json
	loginCode = data["loginCode"]

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=PORT)
