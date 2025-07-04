import configparser

def getConfig(configEntry):
	config = configparser.ConfigParser()
	config.read("/home/whisper/.config/wcal/config.ini")
	# TODO replace with ~/.config/wcal/config.ini after replacing keyboadScanner

	return config["configs"][configEntry]
