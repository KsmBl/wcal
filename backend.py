#!/usr/bin/env python3
from flask import Flask, request
import json
import os

SYNC_LOCATION = "./syncedHighlights/"
LOGIN_CODE = "420621"
PORT = "4200"

# run http server
## get: array for synced files
## get: md5 hash value for each synced file
## post: new file
## post: update file

app = Flask(__name__)

@app.route("/test", methods=["GET"])
def handle_get():
	return "pog"

@app.route("/getWholeChecksum", methods=["GET"])
def getWholeChecksum():
	print("TODO")

@app.route("/upload", methods=["POST"])
def upload():
	data = request.json
	loginCode = data["loginCode"]

	if type(data["year"]) != int or type(data["month"]) != int:
		print(type(data["year"]))
		print(type(data["month"]))
		return [2, "request parameter type not how expected"]

	year = str(data["year"])
	month = str(data["month"])
	content = data["content"]

	if loginCode == LOGIN_CODE:
		yearDirectory = os.path.join(SYNC_LOCATION, year)
		os.makedirs(yearDirectory, exist_ok=True)
		file_path = os.path.join(yearDirectory, f"{month}.json")

		with open(file_path, "w", encoding="utf-8") as f:
			json.dump(content, f, ensure_ascii=False, indent=2)

		return [0, "file synced"]
	else:
		return [1, "login code wrong"]

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=PORT)
