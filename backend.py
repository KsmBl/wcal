#!/usr/bin/env python3
from flask import Flask, request
import hashlib
import glob
import json
import os

SYNC_LOCATION = "./syncedHighlights/"
LOGIN_CODE = "420621"
PORT = "4200"

app = Flask(__name__)

# return checksum of whole SYNC_LOCATION directory
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

# return dict of all files with an md5 sum each
@app.route("/getAllChecksums", methods=["GET"])
def getAllChecksums():
	allChecksums = {}
	for filename in glob.glob(f"{SYNC_LOCATION}/**/*.json", recursive=True):
		allChecksums[filename.replace(SYNC_LOCATION, "")] = md5ForFile(filename, "x")
	return allChecksums

# return array of all files / paths
@app.route("/getAllFileNames", methods=["GET"])
def getAllFileNames():
	allFileNames = []
	for filename in glob.glob(f"{SYNC_LOCATION}/**/*.json", recursive=True):
		allFileNames.append(filename.replace(SYNC_LOCATION, ""))

	return allFileNames

# upload a new file
@app.route("/upload", methods=["POST"])
def upload():
	data = request.json

	# test if given parameters are correct to prevent exploit with paths instead of ints
	if type(data["year"]) != int or type(data["month"]) != int:
		print(type(data["year"]))
		print(type(data["month"]))
		return [2, "request parameter type not how expected"]

	year = str(data["year"])
	month = str(data["month"])
	content = data["content"]

	# test if login code is correct
	loginCode = data["loginCode"]

	if loginCode == LOGIN_CODE:
		yearDirectory = os.path.join(SYNC_LOCATION, year)
		os.makedirs(yearDirectory, exist_ok=True)
		filePath = os.path.join(yearDirectory, f"{month}.json")

		with open(filePath, "w", encoding="utf-8") as f:
			json.dump(content, f, ensure_ascii=False, indent=2)

		return [0, "file synced"]
	else:
		return [1, "login code wrong"]

# create a md5 hashvalue from a file
# arg: absolute path, "x" or "b" for hex or binary mode
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
