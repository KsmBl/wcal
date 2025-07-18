from getConfig import getConfig
import requests
import json

import time

# for external use

def syncFiles():
	getWholeChecksum()

def deleteSync():
	print("not written function")


# for interal use only

# checksum of whole directory
def getWholeChecksum():
	URL = f"http://{getConfig('syncIP')}:{getConfig('syncPort')}/getWholeChecksum"
	rt = requests.get(url = URL, params = {})
	data = rt.json()

	print(data)
	time.sleep(5)

# dict with all files with all individual checkums
def getAllChecksums():
	print("not written function")

# upload it and get a valid response
def syncFile(path):
	print("not written function")

# download state from remote sync
def downloadSync():
	print("not written function")
