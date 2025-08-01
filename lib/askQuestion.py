from keyboardScanner import keyboardScanner
import os

# create visual interface with mutlible options to pick
# arg: str, str[]
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

		if key == "up":
			position = max(0, position - 1)
		elif key == "down":
			position = min(len(options) - 1, position + 1)
		elif key == "enter":
			return position
