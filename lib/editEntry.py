from getString import getString
from saveEntry import saveEntry
from getColor import getColor

def editEntry(pickedEntry, entrys, day, month, year):
	_name = getString("Enter new entry name\n")
	_color = getColor()

	entrys[pickedEntry]["name"] = _name
	entrys[pickedEntry]["color"] = _color

	saveEntry(entrys, day, month, year)
