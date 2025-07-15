import configparser
import os

def createConfigFile():
	# set data for default config file
	path = os.path.expanduser("~/.config/wcal/")
	filename = "config.ini"
	content = "[configs]\nhighlightSaveDirectory = ~/.config/wcal/savedData"
	fullPath = os.path.join(path, filename)

	# test if config file already exists
	if not os.path.isfile(fullPath):
		# write path for config file
		os.makedirs(path, exist_ok=True)

		# write default config file
		with open(fullPath, 'w', encoding='utf-8') as file:
			file.write(content)

def getConfig(configEntry):
	config = configparser.ConfigParser()
	config.read(os.path.expanduser("~/.config/wcal/config.ini"))

	return config["configs"][configEntry]
