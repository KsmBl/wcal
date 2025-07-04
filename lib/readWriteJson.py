import json
import os

# reads a JSON file and returns it as a dict
def readJson(path, SAVE_DIRECTORY):
	if os.path.exists(f"{SAVE_DIRECTORY}/{path}"):
		with open(f"{SAVE_DIRECTORY}/{path}") as jsonData:
			return json.load(jsonData)
	else:
		return None

def writeJson(data, path, SAVE_DIRECTORY):
	with open(f"{SAVE_DIRECTORY}/{path}", "w", encoding="utf-8") as jsonFile:
		json.dump(data, jsonFile, ensure_ascii=False, indent=2)
