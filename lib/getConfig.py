import configparser
import os

def getConfig(configEntry):
	config = configparser.ConfigParser()
	config.read(os.path.expanduser("~/.config/wcal/config.ini"))

	return config["configs"][configEntry]
