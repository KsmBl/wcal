from readWriteJson import readJson
from getConfig import getConfig
import requests
import hashlib
import json
import glob
import os

import time

# for external use

def syncFiles():
	# anything out of sync?
	if getWholeChecksum() == getOwnWholeChecksum():
		print("Everything is synced")
		time.sleep(1)
		return 0 # everything is fine

	# something is out of sync
	else:
		localFiles = getAllOwnFileNames()
		syncFiles = getAllFileNames()

		# local files that are not synced
		localDiff = [x for x in localFiles if x not in syncFiles]

		# synced files that are not local
		syncDiff = [x for x in syncFiles if x not in localFiles]

		if localDiff != []:
			print("have to sync files")
			for x in localDiff:
				uploadFile(os.path.expanduser(os.path.join(getConfig("highlightSaveDirectory"), x)))
				print(f"sync {x}")

		if syncDiff != []:
			print("have to download or delete remote files")
			# TODO

		if localDiff == [] and syncDiff == []:
			remoteChecksums = getAllChecksums()
			localCheckSums = getAllOwnChecksums()

			mismatches = [key for key in remoteChecksums if remoteChecksums.get(key) != localCheckSums.get(key)]

			print(mismatches)

			# TODO: upload mismatching files

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


def getAllOwnChecksums():
	allChecksums = {}
	syncLocation = os.path.expanduser(getConfig("highlightSaveDirectory"))
	for filename in glob.glob(f"{syncLocation}/**/*.json", recursive=True):
		allChecksums[filename.replace(f"{syncLocation}/", "")] = md5ForFile(filename, "x")

	return allChecksums

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
def uploadFile(path):
	year, month = map(int, path.replace('.json', '').split("/")[-2:])

	with open(path) as file:
		data = json.load(file)

	jsonRequest = {
		"loginCode": getConfig("loginCode"),
		"year": year,
		"month": month,
		"content": data
	}

	headers = {
		"Content-Type": "application/json"
	}
	URL = f"http://{getConfig('syncIP')}:{getConfig('syncPort')}/upload"
	rt = requests.post(URL, headers=headers, json=jsonRequest)

	data = rt.json()
	return data[0]

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
