from keyboardScanner import keyboardScanner
import time
import os

def chooseList(inputList):
	selectEntry = 0
	cursor = " * "
	noCursor = "   "

	while True:
		os.system("clear")
		_index = 0
		for i in inputList:
			if _index == selectEntry:
				print(f"{cursor}{i}")
			else:
				print(f"{noCursor}{i}")
			_index += 1

		key = keyboardScanner()

		if key == "Key.up":
			selectEntry = max(0, selectEntry -1)
		elif key == "Key.down":
			selectEntry = min(len(inputList) - 1, selectEntry + 1)
		elif key == "Key.enter":
			return inputList[selectEntry]
		elif key == "q":
			return None
