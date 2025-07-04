from keyboardScanner import keyboardScanner
import os

def getTime():
	time = [12, 0]
	_max = [23, 59]
	position = 0

	while True:
		os.system("clear")
		if position == 0:
			print(" ↑")
		elif position == 1:
			print("   ↑")

		print(f"{str(time[0]).rjust(2)}:{str(time[1]).rjust(2)}")

		if position == 0:
			print(" ↓")
		elif position == 1:
			print("   ↓")

		key = keyboardScanner()

		if key == "left":
			position = max(0, position - 1)
		elif key == "right":
			position = min(1, position + 1)
		elif key == "up":
			time[position] = min(_max[position], time[position] + 1)
		elif key == "down":
			time[position] = max(0, time[position] - 1)
		elif key == "enter":
			return time[0], time[1]
