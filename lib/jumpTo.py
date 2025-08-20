from interactiveMonthViewer import interactiveMonthViewer
from getGoogleCalendar import getGoogleHighlights
from syncHandler import syncFiles
from getConfig import getConfig
from datetime import datetime
from readWriteJson import *
import calendar

import time

# jump to a specific date
# arg: int, int, int
def jumpToDate(day, month, year):
	SAVE_DIRECTORY = os.path.expanduser(getConfig("highlightSaveDirectory"))

	# parse local saved highlights
	SAVE_DIRECTORY = os.path.expanduser(getConfig("highlightSaveDirectory"))
	if os.path.exists(f"{SAVE_DIRECTORY}/{year}/{month}.json"):
		highlights = readJson(f"{year}/{month}.json")
	
	else:
		createMissingPathObjects(year, month)
		highlights = {}

	allHighlights = {}

	# parse google calendar
	if getConfig("enableGoogleCal") == "True":
		start = datetime(year, month, 1, 0, 0, 0, 0)
		lastDay = calendar.monthrange(year, month)[1]
		end = datetime(year, month, lastDay, 23, 59, 59, 999999)
		googleHighlightDays = getGoogleHighlights(start, end)


		# combine local and google highlights
		allHighlights = {**highlights}
		for _day, times in googleHighlightDays.items():
			if _day not in allHighlights:
				allHighlights[_day] = times.copy()
			else:
				for time_, details in times.items():
					allHighlights[_day][time_] = details.copy()

	else:
		allHighlights = highlights


	rt = interactiveMonthViewer(day, month, year, allHighlights)

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

	elif rt == "quit":
		return "quit"

	elif rt[0] == "changedEntrys":
		# return whole day with changed, removed or new entrys
		jumpToDate(rt[2], month, year)

	if getConfig("syncHighlights") == "True":
		rt2 = syncFiles()
		if rt2[0] != 0:
			print(rt2[1])
			time.sleep(1)


# use jumpToDate() to jump to the current month and day
def jumpToCurrentMonth():
	# get current Date
	currentDay = datetime.now().day
	jumpToCurrentMonth = datetime.now().month
	currentYear = datetime.now().year

	# show current Date
	return jumpToDate(currentDay, jumpToCurrentMonth, currentYear)

def createMissingPathObjects(year, month):
	SAVE_DIRECTORY = os.path.expanduser(getConfig("highlightSaveDirectory"))

	# create missing dir
	if not os.path.exists(os.path.join(SAVE_DIRECTORY, str(year))):
		os.makedirs(os.path.join(SAVE_DIRECTORY, str(year)))
	 
	# create missing file
	highlightPath = f"{year}/{month}.json"
	if not os.path.isfile(os.path.join(SAVE_DIRECTORY, highlightPath)):
		writeJson({}, highlightPath)
