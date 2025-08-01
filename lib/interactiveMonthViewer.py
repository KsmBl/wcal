from editDayHighlights import editDayHighlights
from keyboardScanner import keyboardScanner
from readWriteJson import readJson
from printMonth import printMonth
from collections import Counter
from getConfig import getConfig
import calendar
import os

# interactive Month viewer where a day can be picked for editing highlights
def interactiveMonthViewer(day, month, year, highlightDays):
	cursorDay = day
	monthStart, monthLength = calendar.monthrange(year, month)

	coloredDays = {}

	SAVE_DIRECTORY = os.path.expanduser(getConfig("highlightSaveDirectory"))
	if os.path.exists(f"{SAVE_DIRECTORY}/{year}/{month}.json"):
		highlightColors = readJson(f"{year}/{month}.json")
		print(highlightColors)
		for i in highlightColors:
			dayColor = []
			for ii in highlightColors[i]:
				dayColor.append(highlightColors[i][ii]["color"])

				_countedNumber= Counter(dayColor)
				_mostUsedColor = max(_countedNumber.values())
				_mostUsedColors = [nbr for nbr, count in _countedNumber.items() if count == _mostUsedColor]

				coloredDays[i] = max(_mostUsedColors)

	while True:
		os.system('clear')
		printMonth(monthStart, monthLength, highlightDays, cursorDay, calendar.month_name[month], year, coloredDays)
		key = keyboardScanner()

		if key == "left":
			cursorDay -= 1

			if cursorDay <= 0:
				return "month - 1"

		elif key == "right":
			cursorDay += 1
			if cursorDay > monthLength:
				return "month + 1"

		elif key == "up":
			cursorDay = max(cursorDay - 7, 1)

		elif key == "down":
			cursorDay = min(cursorDay + 7, monthLength)

		elif key == "enter":
			rt = editDayHighlights(cursorDay, month, year)
			if rt == "reloadDay":
				return rt

		elif key == "q":
			return "quit"
