from getColor import getColor, allColors
from deleteEntry import deleteEntry
from askQuestion import askQuestion
from chooseList import chooseList
from editEntry import editEntry
from getString import getString
from getConfig import getConfig
from getTime import getTime
from readWriteJson import *
import re

import time

# creates an visual interface for editing highlighted days in a calender
# arg: int, int, int
def editDayHighlights(day, month, year):
	changedDayVisuality = 0

	while True:
		SAVE_DIRECTORY = os.path.expanduser(getConfig("highlightSaveDirectory"))
		highlightPath = f"{year}/{month}.json"
		if not os.path.exists(os.path.join(SAVE_DIRECTORY, str(year))):
			os.makedirs(os.path.join(SAVE_DIRECTORY, str(year)))

		if not os.path.isfile(os.path.join(SAVE_DIRECTORY, highlightPath)):
			writeJson({}, highlightPath)

		highlights = readJson(highlightPath)
		dayEntries = []

		if str(day) in highlights:
			dayEntries = highlights[str(day)]
			arrayDayEntries = [f"{allColors()[info['color']]}{time} | {info['name']}{allColors()[0]}" for time, info in dayEntries.items()]

			arrayDayEntries.append("new Entry +")
			arrayDayEntries.append("return")

			pickedEntry = chooseList(arrayDayEntries)
			if pickedEntry == None:
				if changedDayVisuality == 0:
					return None
				else:
					return "reloadDay"

			pickedID = arrayDayEntries.index(pickedEntry)
			pickedEntry = pickedEntry.split(" ")[0]

			if pickedID <= len(arrayDayEntries) - 3:
				edit = askQuestion("edit this Entry:", ["edit", "delete", "return"])
				_pickedEntry = re.sub(r'\x1b\[[0-9;]*m', '', pickedEntry)

				if edit == 0:
					editEntry(_pickedEntry, highlights, day, highlightPath)
				elif edit == 1:
					rt = askQuestion("delete entry?", ["no", "yes"])
					if rt == 1:
						rt2 = deleteEntry(_pickedEntry, highlights, day, highlightPath)
						if rt2 == "reloadDay":
							return "reloadDay"
			else:
				# new Entry
				if pickedID == len(arrayDayEntries) - 2:
					_hour, _minute = getTime()
					_name = getString()
					_color = getColor()

					highlights[str(day)].setdefault(f"{_hour}:{_minute}", {})

					highlights[str(day)][f"{_hour}:{_minute}"]["name"] = _name
					highlights[str(day)][f"{_hour}:{_minute}"]["color"] = _color

					writeJson(highlights, highlightPath)
				# return
				elif pickedID == len(arrayDayEntries) - 1:
					if changedDayVisuality == 0:
						return None
					else:
						return "reloadDay"

		else:
			_hour, _minute = getTime()
			_name = getString()
			_color = getColor()
			highlights[str(day)] = {
				f"{_hour}:{_minute}" : {
					"name" : _name,
					"color" : _color
				}
			}

			writeJson(highlights, highlightPath)
			changedDayVisuality = 1
