from readWriteJson import readJson
from saveEntry import saveEntry

def deleteEntry(pickedEntry, day, month, year):
	entrys = readJson(f"{year}/{month}.json")[str(day)]
	entrys.pop(str(pickedEntry))
	entrys = {k: v for k, v in entrys.items() if not v["name"].startswith("(G)")}

	saveEntry(entrys, day, month, year)
	return "reloadDay"
