from keyboardScanner import keyboardScanner
import sys
import os

colors = [
	'\033[0m',	# 0 normal
	'\033[45m',	# 1 pink
	'\033[44m',	# 2 dark blue
	'\033[46m',	# 3 light blue
	'\033[42m',	# 4 green
	'\033[43m',	# 5 yellow
	'\033[41m']	# 6 red

def allColors():
	return colors

# ascii interface for choosing a color
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
		elif key == "enter":
			return colorID
