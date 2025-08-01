from askQuestion import askQuestion
from readWriteJson import readJson
from getConfig import getConfig
from log import log
import requests
import hashlib
import json
import glob
import os

import time

REMOTE_URL = ""

# for external use
# sync all files, noting else to care about
def syncFiles():
	ABSOLUTE_SYNC_LOC = os.path.expanduser(getConfig("highlightSaveDirectory"))
	global REMOTE_URL
	REMOTE_URL = f"http://{getConfig('syncIP')}:{getConfig('syncPort')}"
	# test if server is reachable
	try:
		rt = getRequest("ping")
		reachable = True

	except:
		reachable = False

	if not reachable:
		log(1, f"remote Server '{REMOTE_URL}' not reachable")
		return [1, f"{REMOTE_URL} not reachable"]


	# anything out of sync?
	if getWholeChecksum() == getOwnWholeChecksum():
		log(0, "everything synced")
		return [0, "everything synced"]

	# something is out of sync
	else:
		# compare filenames between remote and local
		localFiles = getAllOwnFileNames()
		syncFiles = getAllFileNames()

		# local files that are not synced
		localDiff = [x for x in localFiles if x not in syncFiles]

		# synced files that are not local
		syncDiff = [x for x in syncFiles if x not in localFiles]

		if localDiff != []:
			for x in localDiff:
				rt = uploadFile(os.path.join(ABSOLUTE_SYNC_LOC, x))
				if rt[0] != 0:
					askQuestion(rt[1], ["OK"])
					return [1, "not synced"]

		if syncDiff != []:
			print("have to download or delete remote files")
			time.sleep(2)
			# TODO
			return [1, "not fully synced"]

		# all files exists on both sides
		if localDiff == [] and syncDiff == []:
			# compare all file checksums
			remoteChecksums = getAllChecksums()
			localCheckSums = getAllOwnChecksums()

			mismatches = [key for key in remoteChecksums if remoteChecksums.get(key) != localCheckSums.get(key)]

			for x in mismatches:
				# replace mismatched files
				rt = uploadFile(os.path.join(ABSOLUTE_SYNC_LOC, x))
				if rt[0] != 0:
					askQuestion(rt[1], ["OK"])
					return [1, "not synced"]

	log(0, "everything synced")
	return [0, "everything synced"]

# for interal use only
# checksum of whole sync directory
def getWholeChecksum():
	return getRequest("getWholeChecksum")["hash"]

# checksum of whole local directory
def getOwnWholeChecksum():
	ABSOLUTE_SYNC_LOC = os.path.expanduser(getConfig("highlightSaveDirectory"))
	md5 = hashlib.md5()

	for root, dirs, files in sorted(os.walk(ABSOLUTE_SYNC_LOC)):
		for fname in sorted(files):
			fpath = os.path.join(root, fname)
			relPath = os.path.relpath(fpath, ABSOLUTE_SYNC_LOC)

			md5.update(relPath.encode())
			md5.update(md5ForFile(fpath, "b"))

	hashval = md5.hexdigest()
	return hashval

# get dict with all remote files with all individual checkums
def getAllChecksums():
	return getRequest("getAllChecksums")

# get dict with all local files with all individual checkums
def getAllOwnChecksums():
	ABSOLUTE_SYNC_LOC = os.path.expanduser(getConfig("highlightSaveDirectory"))
	allChecksums = {}
	for filename in glob.glob(f"{ABSOLUTE_SYNC_LOC}/**/*.json", recursive=True):
		allChecksums[filename.replace(f"{ABSOLUTE_SYNC_LOC}/", "")] = md5ForFile(filename, "x")

	return allChecksums

# get array of all remote files
def getAllFileNames():
	return getRequest("getAllFileNames")

# get array of all local files
def getAllOwnFileNames():
	ABSOLUTE_SYNC_LOC = os.path.expanduser(getConfig("highlightSaveDirectory"))
	allFileNames = []
	for filename in glob.glob(f"{ABSOLUTE_SYNC_LOC}/**/*.json", recursive=True):
		allFileNames.append(filename.replace(f"{ABSOLUTE_SYNC_LOC}/", ""))

	return allFileNames

# upload a file
## arg: absolute path
def uploadFile(path):
	# extract month and year from the path
	year, month = map(int, path.replace('.json', '').split("/")[-2:])

	with open(path) as file:
		data = json.load(file)

	jsonRequest = {
		"loginCode": getConfig("loginCode"),
		"year": year,
		"month": month,
		"content": data
	}

	URL = f"{REMOTE_URL}/upload"
	rt = requests.post(URL, headers={"Content-Type": "application/json"}, json=jsonRequest)

	data = rt.json()

	if data[0] == 0:
		log(0, f"'{path}' synced")

	return data

# create an md5 hash value from a file
## arg: absolute path, "x" or "b" for hex or binary mode
def md5ForFile(filePath, mode):
	hasher = hashlib.md5()
	with open(filePath, 'rb') as f:
		for chunk in iter(lambda: f.read(4096), b''):
			hasher.update(chunk)
 
	if mode == "x":
		return hasher.hexdigest()
	elif mode == "b":
		return hasher.digest()

# create a get request
# arg: backend path
def getRequest(path):
	URL = f"{REMOTE_URL}/{path}"
	rt = requests.get(url = URL, params = {}, timeout = 1)
	data = rt.json()
	return data
