from readWriteJson import writeJson
from getString import getString
from getColor import getColor
from getTime import getTime

import time

def editEntry(pickedEntry, highlights, day, highlightPath):
	_name = getString("Enter new entry name\n")
	_color = getColor()

	highlights[str(day)][pickedEntry]["name"] = _name
	highlights[str(day)][pickedEntry]["color"] = _color

	writeJson(highlights, highlightPath)
