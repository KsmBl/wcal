from readWriteJson import readJson, writeJson

# save an Entry into a json file
# args:	dayEntrys{}, int, int, int
def saveEntry(entrys, day, month, year):
	# remove google entrys
	entrys = {k: v for k, v in entrys.items() if not v["name"].startswith("(G)")}

	# combine highlights from whole month with new dict of entrys for one day
	highlightPath = f"{year}/{month}.json"
	highlights = readJson(highlightPath)

	# remove day if empty
	if entrys == {}:
		if str(day) in highlights:
			highlights.pop(str(day))
	else:
		highlights[str(day)] = entrys

	writeJson(highlights, highlightPath)
