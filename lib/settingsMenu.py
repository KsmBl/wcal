from askQuestion import askQuestion
from chooseList import chooseList
from getString import getString
import time
import re

def settingsMenu():
	while True:
		rt = chooseList(["sync Highlights", "syncIP", "syncPort", "loginCode", "return"])
		print(rt)

		if rt == "sync Highlights":
			askQuestion("sync Highlights to remote Server?", ["Yes", "No"])
			# TODO: change setting
		elif rt == "syncIP":
			enterIP()
			# TODO: save new IP
		elif rt == "syncPort":
			rt2 = enterPort()
			# TODO: save new Port
		elif rt == "loginCode":
			rt2 = getString("Enter new login code")
			# TODO: save new login code
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
