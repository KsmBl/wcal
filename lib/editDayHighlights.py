from getGoogleCalendar import getGoogleHighlights
from deleteGoogleEntry import deleteGoogleEntry
from getColor import getColor, allColors
from deleteEntry import deleteEntry
from askQuestion import askQuestion
from chooseList import chooseList
from editEntry import editEntry
from saveEntry import saveEntry
from getString import getString
from getConfig import getConfig
from datetime import datetime
from getTime import getTime
from readWriteJson import *
import re

# creates an visual interface for editing highlighted days in a calender
# arg: int, int, int
def editDayHighlights(day, month, year, entrys):
	changedDayVisuality = 0

	while True:
		# create missing files or dirs
		highlightPath = f"{year}/{month}.json"
		SAVE_DIRECTORY = os.path.expanduser(getConfig("highlightSaveDirectory"))
		createMissingPathObjects(SAVE_DIRECTORY, year, highlightPath)

		# show entrys as array with + and return button
		arrayDayEntries = [f"{allColors()[info['color']]}{_time} | {info['name']}{allColors()[0]}" for _time, info in entrys.items()]
		arrayDayEntries.append("new Entry +")
		arrayDayEntries.append("return")

		# select one of the entrys in a list
		pickedEntry = chooseList(arrayDayEntries)

		if pickedEntry == None:
			return

		pickedID = arrayDayEntries.index(pickedEntry)
		pickedEntry = pickedEntry.split(" ")[0]

		if pickedID <= len(arrayDayEntries) - 3:
			# an entry was picked
			rt = editEntryMenu(pickedEntry, entrys, day, month, year)
			if rt == "reloadDay":
				return rt

		else:
			# new Entry was picked
			if pickedID == len(arrayDayEntries) - 2:
				newEntry(entrys)
				saveEntry(entrys, day, month, year)
				return "reloadDay"

			# return was picked
			elif pickedID == len(arrayDayEntries) - 1:
				return


def editEntryMenu(pickedEntry, entrys, day, month, year):
	# remove color code
	_pickedEntry = re.sub(r'\x1b\[[0-9;]*m', '', pickedEntry)

	# check if entry is from google
	if entrys[str(_pickedEntry)]["name"].startswith("(G)"):
		# entry is from google
		edit = askQuestion("delete Entry in Google:", ["No", "Yes"])

		if edit == 1:
			# 2025-08-01 00:00:00
			dayStart = datetime(year, month, day, 0, 0, 0)
			dayEnd = datetime(year, month, day + 1, 0, 0, 0)
			googleHighlights = getGoogleHighlights(dayStart, dayEnd)

			# delete Google Entry
			googleEntryId = googleHighlights[str(day)][str(_pickedEntry)]["eventId"]
			deleteGoogleEntry(googleEntryId)
			return "reloadDay"
		elif edit == 0:
			return 0
	else:
		# entry is not from google
		edit = askQuestion("edit this Entry:", ["edit", "delete", "return"])

		if edit == 0:
			editEntry(_pickedEntry, entrys, day, month, year)
		elif edit == 1:
			if askQuestion("delete entry?", ["no", "yes"]) == 1:
				rt = deleteEntry(_pickedEntry, day, month, year)
				if rt == "reloadDay":
					return rt
		elif edit == 2:
			return 0


def newEntry(entrys):
	_hour, _minute, _name, _color = getEntryData()
	entrys.setdefault(f"{_hour}:{_minute}", {})

	entrys[f"{_hour}:{_minute}"]["name"] = _name
	entrys[f"{_hour}:{_minute}"]["color"] = _color


def getEntryData():
	_hour, _minute = getTime()
	_name = getString()
	_color = getColor()

	return _hour, _minute, _name, _color


def createMissingPathObjects(SAVE_DIRECTORY, year, highlightPath):
	# create missing dir
	if not os.path.exists(os.path.join(SAVE_DIRECTORY, str(year))):
		os.makedirs(os.path.join(SAVE_DIRECTORY, str(year)))

	# create missing file
	if not os.path.isfile(os.path.join(SAVE_DIRECTORY, highlightPath)):
		writeJson({}, highlightPath)
