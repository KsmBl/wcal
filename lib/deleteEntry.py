from readWriteJson import writeJson

def deleteEntry(pickedEntry, highlights, day, highlightPath):
	highlights[str(day)].pop(str(pickedEntry))
	writeJson(highlights, highlightPath)

	if highlights[str(day)] == {}:
		highlights.pop(str(day))
		writeJson(highlights, highlightPath)
		return "reloadDay"
