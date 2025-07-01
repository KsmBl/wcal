import json
import os

# reads a JSON file and returns it as a dict
def readJson(path, SAVE_DIRECTORY):
	if os.path.exists(f"{SAVE_DIRECTORY}/{path}"):
		with open(f"{SAVE_DIRECTORY}/{path}") as jsonData:
			return json.load(jsonData)
	else:
		return None
