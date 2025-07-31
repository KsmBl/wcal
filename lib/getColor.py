from keyboardScanner import keyboardScanner
import sys
import os

colors = [
	'\033[0m',	# normal
	'\033[45m',	# pink
	'\033[44m',	# dark blue
	'\033[46m',	# light blue
	'\033[42m',	# green
	'\033[43m',	# yellow
	'\033[41m']	# red

def allColors():
	return colors

def getColor():
	colorID = 0
	
	while True:
		os.system("clear")

		print("select Color")
		print(" ← ", end="")
		for i in range(len(colors)):
			if colorID == i:
				print(f"[{colors[i]}   {colors[0]}]", end="")
			else:
				print(f" {colors[i]}   {colors[0]} ", end="")

		print(" →")

		key = keyboardScanner()

		if key == "left":
			colorID = max(colorID - 1, 0)
		elif key == "right":
			colorID = min(colorID + 1, len(colors) - 1)
		elif key == "q":
			sys.exit(0)
		elif key == "enter":
			return colorID
