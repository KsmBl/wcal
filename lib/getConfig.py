import configparser
import os

CONFIG_LOCATION = "~/.config/wcal/"

# creates a default config file in ~/.config/wcal/
def createConfigFile():
	# set data for default config file
	path = os.path.expanduser(CONFIG_LOCATION)
	filename = "config.ini"
	content = "[configs]\nhighlightSaveDirectory = ~/.config/wcal/savedData\nlogLocation = ~/.config/wcal/.wcal.log\nsyncIP = 0.0.0.257\nsyncPort = 4200\nloginCode = 420621\nsyncHighlights = True"
	fullPath = os.path.join(path, filename)

	# test if config file already exists
	if not os.path.isfile(fullPath):
		# write path for config file
		os.makedirs(path, exist_ok=True)

		# write default config file
		with open(fullPath, 'w', encoding='utf-8') as file:
			file.write(content)

# get a config entry
# arg: str
def getConfig(configEntry):
	config = configparser.ConfigParser()
	config.read(os.path.expanduser(f"{CONFIG_LOCATION}config.ini"))

	return config["configs"][configEntry]

def setConfig(configEntry, value):
	config = configparser.ConfigParser()

	config.read(os.path.expanduser(f"{CONFIG_LOCATION}config.ini"))

	if "configs" not in config.sections():
		config.add_section("configs")

	config.set("configs", configEntry, value)

	with open(os.path.expanduser(f"{CONFIG_LOCATION}config.ini"), 'w') as configfile:
		config.write(configfile)
