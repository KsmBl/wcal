from getConfig import getConfig
import time
import os

logLevels = [
	"[ INFO  ]",	# 0
	"[WARNING]",	# 1
	"[ ERROR ]",	# 2
	"[  UwU  ]"	# 3
]

def log(level, text):
	timestamp = round(time.time(), 2)
	content = f"[{timestamp}]{logLevels[level]} : {text}\n"

	logLocation = os.path.expanduser(getConfig("logLocation"))

	if not os.path.exists(logLocation):
		with open(logLocation, 'w') as f:
			f.write("[timestamp][loglevel][message]\n")

	with open(logLocation, "a", encoding="utf-8") as logfile:
		logfile.write(content)
