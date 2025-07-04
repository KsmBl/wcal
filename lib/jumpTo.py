from interactiveMonthViewer import interactiveMonthViewer
from getConfig import getConfig
from datetime import datetime
from readWriteJson import *
import calendar

SAVE_DIRECTORY = "./savedData"

def jumpToDate(day, month, year):
	SAVE_DIRECTORY = getConfig("highlightSaveDirectory")
	highlights = readJson(f"{year}/{month}.json", SAVE_DIRECTORY)
	highlightDays = []

	if highlights == None:
		highlightDays = []
	else:
		for i in highlights:
			highlightDays.append(int(i))

	rt = interactiveMonthViewer(day, month, year, highlightDays)

	if rt == "month - 1":
		if month <= 1:
			_year = year - 1

			# calculate length of last month
			_day = calendar.monthrange(_year, 12)[1]

			# run itself again with new values
			return jumpToDate(_day, 12, _year)
		else:
			_day = calendar.monthrange(year, month - 1)[1]
			return jumpToDate(_day, month - 1, year)
	elif rt == "month + 1":
		if month >= 12:
			return jumpToDate(1, 1, year + 1)
		else:
			return jumpToDate(1, month + 1, year)

	elif rt == "reloadDay":
		return jumpToDate(day, month, year)

	return rt

def jumpToCurrentMonth():
	# get current Date
	currentDay = datetime.now().day
	jumpToCurrentMonth = datetime.now().month
	currentYear = datetime.now().year

	# show current Date
	return jumpToDate(currentDay, jumpToCurrentMonth, currentYear)
