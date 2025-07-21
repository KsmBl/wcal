from getConfig import getConfig, setConfig
from askQuestion import askQuestion
from chooseList import chooseList
from getString import getString
import time
import re

def settingsMenu():
	while True:
		allSettings = [
			f"sync Highlights - {getConfig('syncHighlights')}",
			f"syncIP - {getConfig('syncIP')}",
			f"syncPort - {getConfig('syncPort')}",
			f"loginCode - {getConfig('loginCode')}",
			f"return"
		]

		rt = chooseList(allSettings)

		if rt == None:
			return

		position = allSettings.index(rt)

		if position == 0:
			rt = askQuestion("sync Highlights to remote Server?", ["Yes", "No"])
			setConfig("syncHighlights", str([True, False][rt]))
		elif position == 1:
			rt = enterIP()
			setConfig("syncIP", rt)
		elif position == 2:
			rt = enterPort()
			setConfig("syncPort", rt)
		elif position == 3:
			rt = getString("Enter new login code\n")
			setConfig("loginCode", rt)
		elif rt == "return":
			return

def enterIP(message = ""):
	ip = getString(message + "Enter remote Server Ip\n")
	ipv4Regex = "^(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$"
	if re.match(ipv4Regex, ip):
		print("good IP")
		return ip
	else:
		return enterIP("thats not an IP. ")

def enterPort(message = ""):
	Port = getString(message + "Enter remote Server Port\n")
	PortRegex = "^([1-9]|[1-9][0-9]{1,3}|[1-5][0-9]{4}|6([0-4][0-9]{3}|5([0-4][0-9]{2}|5([0-2][0-9]|3[0-5]))))$"

	if re.match(PortRegex, Port):
		print("good Port")
		return Port
	else:
		return enterPort("thats not a Port. ")
