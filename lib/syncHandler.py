from getConfig import getConfig
import requests
import hashlib
import json
import os

import time

# for external use

def syncFiles():
	print(getWholeChecksum())
	print(getOwnWholeChecksum())
	time.sleep(5)

def deleteSync():
	print("not written function")


# for interal use only

# checksum of whole directory
def getWholeChecksum():
	URL = f"http://{getConfig('syncIP')}:{getConfig('syncPort')}/getWholeChecksum"
	rt = requests.get(url = URL, params = {})
	data = rt.json()

	return data["hash"]

def getOwnWholeChecksum():
	md5 = hashlib.md5()

	syncLocation = os.path.expanduser(getConfig("highlightSaveDirectory"))
	for root, dirs, files in sorted(os.walk(syncLocation)):
		for fname in sorted(files):
			fpath = os.path.join(root, fname)
			relPath = os.path.relpath(fpath, syncLocation)

			md5.update(relPath.encode())
			md5.update(md5ForFile(fpath, "b"))

	hashval = md5.hexdigest()
	return hashval

# dict with all files with all individual checkums
def getAllChecksums():
	URL = f"http://{getConfig('syncIP')}:{getConfig('syncPort')}/getAllChecksums"
	rt = requests.get(url = URL, params = {})
	data = rt.json()

	print(data)
	time.sleep(5)

# upload it and get a valid response
def syncFile(path):
	print("not written function")

# download state from remote sync
def downloadSync():
	print("not written function")

def md5ForFile(filePath, mode):
	hasher = hashlib.md5()
	with open(filePath, 'rb') as f:
		for chunk in iter(lambda: f.read(4096), b''):
			hasher.update(chunk)
 
	if mode == "x":
		return hasher.hexdigest()
	elif mode == "b":
		return hasher.digest()
