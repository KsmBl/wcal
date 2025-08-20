from editDayHighlights import editDayHighlights, newEntry
from keyboardScanner import keyboardScanner
from readWriteJson import readJson
from printMonth import printMonth
from collections import Counter
from saveEntry import saveEntry
from getConfig import getConfig
import calendar
import os

# interactive Month viewer where a day can be picked for editing highlights
def interactiveMonthViewer(day, month, year, allHighlights):
	# set cursor
	cursorDay = day

	monthStart, monthLength = calendar.monthrange(year, month)

	# get array of days with highlights
	highlightDays = []
	if allHighlights == None:
		highlightDays = []
	else:
		for i in allHighlights:
			highlightDays.append(int(i))

	# get dict of days that are colored
	coloredDays = getDayColors(allHighlights)

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


def getDayColors(highlightColors):
	coloredDays = {}
	for i in highlightColors:
		dayColor = []
		for ii in highlightColors[i]:
			dayColor.append(highlightColors[i][ii]["color"])

			_countedNumber= Counter(dayColor)
			_mostUsedColor = max(_countedNumber.values())
			_mostUsedColors = [nbr for nbr, count in _countedNumber.items() if count == _mostUsedColor]

			coloredDays[i] = max(_mostUsedColors)

	return coloredDays
