from askQuestion import askQuestion
from chooseList import chooseList
from getString import getString
from getConfig import getConfig
from getTime import getTime
from readWriteJson import *

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
			writeJson({}, highlightPath, SAVE_DIRECTORY)

		highlights = readJson(highlightPath, SAVE_DIRECTORY)
		dayEntries = []

		if str(day) in highlights:
			dayEntries = highlights[str(day)]
			arrayDayEntries = [f"{t} | {msg}" for t, msg in sorted(dayEntries.items())]
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
				remove = askQuestion("remove this Entry?", ["no", "yes"])

				if remove == 1:
					highlights[str(day)].pop(pickedEntry)
					writeJson(highlights, highlightPath, SAVE_DIRECTORY)

					if highlights[str(day)] == {}:
						highlights.pop(str(day))
						writeJson(highlights, highlightPath, SAVE_DIRECTORY)
						return "reloadDay"
			else:
				# new Entry
				if pickedID == len(arrayDayEntries) - 2:
					_hour, _minute = getTime()
					_name = getString()
					highlights[str(day)][f"{_hour}:{_minute}"] = _name
					writeJson(highlights, highlightPath, SAVE_DIRECTORY)
				# return
				elif pickedID == len(arrayDayEntries) - 1:
					if changedDayVisuality == 0:
						return None
					else:
						return "reloadDay"

		else:
			_hour, _minute = getTime()
			_name = getString()
			print(highlights)
			highlights[str(day)] = {}
			highlights[str(day)][f"{_hour}:{_minute}"] = _name
			writeJson(highlights, highlightPath, SAVE_DIRECTORY)
			changedDayVisuality = 1
