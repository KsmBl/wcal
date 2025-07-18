from keyboardScanner import keyboardScanner
import os

# creates an visual interface with multible options
# arg: str[]
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

		if key == "up":
			selectEntry = max(0, selectEntry -1)
		elif key == "down":
			selectEntry = min(len(inputList) - 1, selectEntry + 1)
		elif key == "enter":
			return inputList[selectEntry]
		elif key == "q":
			return None
