#!/usr/bin/env python3
from flask import Flask, request
import hashlib
import glob
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
	md5 = hashlib.md5()

	for root, dirs, files in sorted(os.walk(SYNC_LOCATION)):
		for fname in sorted(files):
			fpath = os.path.join(root, fname)
			relPath = os.path.relpath(fpath, SYNC_LOCATION)

			md5.update(relPath.encode())

			md5.update(md5ForFile(fpath, "b"))

	hashval = md5.hexdigest()

	return {"hash":hashval}


@app.route("/getAllChecksums", methods=["GET"])
def getAllChecksums():
	allChecksums = {}
	for filename in glob.glob(f"{SYNC_LOCATION}/**/*.json", recursive=True):
		allChecksums[filename.replace(SYNC_LOCATION, "")] = md5ForFile(filename, "x")
	return allChecksums

@app.route("/getAllFileNames", methods=["GET"])
def getAllFileNames():
	allFileNames = []
	for filename in glob.glob(f"{SYNC_LOCATION}/**/*.json", recursive=True):
		allFileNames.append(filename.replace(SYNC_LOCATION, ""))

	return allFileNames


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
		filePath = os.path.join(yearDirectory, f"{month}.json")

		with open(filePath, "w", encoding="utf-8") as f:
			json.dump(content, f, ensure_ascii=False, indent=2)

		return [0, "file synced"]
	else:
		return [1, "login code wrong"]


def md5ForFile(filePath, mode):
	hasher = hashlib.md5()
	with open(filePath, 'rb') as f:
		for chunk in iter(lambda: f.read(4096), b''):
			hasher.update(chunk)

	if mode == "x":
		return hasher.hexdigest()
	elif mode == "b":
		return hasher.digest()

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=PORT)
