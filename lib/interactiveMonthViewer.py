import calendar
import os

from editDayHighlights import editDayHighlights
from keyboardScanner import keyboardScanner
from printMonth import printMonth

# interactive Month viewer where a day can be picked for editing highlights
def interactiveMonthViewer(day, month, year, highlightDays):
	cursorDay = day

	monthStart, monthLength = calendar.monthrange(year, month)

	while True:
		os.system('clear')
		printMonth(monthStart, monthLength, highlightDays, cursorDay, calendar.month_name[month], year)
		key = keyboardScanner()

		if key == "Key.left":
			cursorDay -= 1

			if cursorDay <= 0:
				return "month - 1"

		elif key == "Key.right":
			cursorDay += 1
			if cursorDay > monthLength:
				return "month + 1"

		elif key == "Key.up":
			cursorDay = max(cursorDay - 7, 1)

		elif key == "Key.down":
			cursorDay = min(cursorDay + 7, monthLength)

		elif key == "Key.enter":
			rt = editDayHighlights(cursorDay, month, year)
			if rt == "reloadDay":
				return rt

		elif key == "q":
			return "quit"
