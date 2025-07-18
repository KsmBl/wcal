from getConfig import getConfig
import requests
import hashlib
import json
import glob
import os

import time

# for external use

def syncFiles():
	if getWholeChecksum() == getOwnWholeChecksum():
		return 0 # everything is fine
	else:
		localFiles = getAllOwnFileNames()
		syncFiles = getAllFileNames()

		# local files that are not synced
		localDiff = [x for x in localFiles if x not in syncFiles]

		# synced files that are not local
		syncDiff = [x for x in syncFiles if x not in localFiles]

		print(localFiles)
		print(syncFiles)
		print(localDiff)
		print(syncDiff)

		if localDiff != []:
			print("have to sync files")

		if syncDiff != []:
			print("have to download or delete remote files")

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
	return data

def getAllFileNames():
	URL = f"http://{getConfig('syncIP')}:{getConfig('syncPort')}/getAllFileNames"
	rt = requests.get(url = URL, params = {})
	data = rt.json()
	return data

def getAllOwnFileNames():
	allFileNames = []
	storeLocation = os.path.expanduser(getConfig("highlightSaveDirectory"))
	for filename in glob.glob(f"{storeLocation}/**/*.json", recursive=True):
		allFileNames.append(filename.replace(f"{storeLocation}/", ""))

	return allFileNames

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
