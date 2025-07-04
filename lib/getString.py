from keyboardScanner import keyboardScanner

import os

def getString():
	customString = ""
	availabeChars = "abcdefghijklmnopqrstuvwxyz1234567890"

	while True:
		os.system("clear")
		print(customString)
		key = keyboardScanner()

		if key in availabeChars:
			customString += key
		elif key == "space":
			customString += " "
		elif key == "enter":
			return customString
		else:
			continue
