from keyboardScanner import keyboardScanner
import time
import os

def askQuestion(question, options):
	position = 0

	while True:
		os.system("clear")
		width = max(len(max(options, key=len)), len(question)) + 10

		print("-" * (width + 2))
		print(f"|{question.center(width)}|")
		print(f"|{' ' * width}|")

		_index = 0
		for i in options:
			if position == _index:
				print(f"|{('[' + i + ']').center(width)}|")
			else:
				print(f"|{i.center(width)}|")

			_index += 1

		print(f"|{' ' * width}|")
		print("-" * (width + 2))

		key = keyboardScanner()

		if key == "Key.up":
			position = max(0, position - 1)
		elif key == "Key.down":
			position = min(len(options) - 1, position + 1)
		elif key == "Key.enter":
			return position
