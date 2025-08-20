from keyboardScanner import keyboardScanner
import os

# creates an visual interface with multible options
# args: str[], str (optional)
def chooseList(inputList, header=""):
	selectEntry = 0
	cursor = " * "
	noCursor = "   "

	while True:
		os.system("clear")
		print(header)
		_index = 0
		for i in inputList:
			if _index == selectEntry:
				print(f"{cursor}{i}")
			else:
				print(f"{noCursor}{i}")
			_index += 1

		key = keyboardScanner()

		if key == "up":
			selectEntry = max(0, selectEntry -1)
		elif key == "down":
			selectEntry = min(len(inputList) - 1, selectEntry + 1)
		elif key == "enter":
			return inputList[selectEntry]
		elif key in ["1", "2", "3", "4", "5", "6", "7", "8", "9"]:
			if int(key) <= len(inputList):
				return inputList[int(key) - 1]
		elif key == "0":
			if len(inputList) >= 10:
				return inputList[9]
		elif key == "q":
			return None
