from keyboardScanner import keyboardScanner
from datetime import datetime
import calendar
import sys
import os

# graphical ascii interface that returns selected [day, month, year]
def getDate():
	day = datetime.now().day
	month = datetime.now().month
	year = datetime.now().year
	cursor = 0 # 0=day, 1=month, 2=year
	while True:
		os.system("clear")
		_day = str(day).rjust(2)
		_month = str(month).rjust(2)
		_year = str(year).rjust(4)

		if cursor == 0:
			_day = f"[{_day}]"
		elif cursor == 1:
			_month = f"[{_month}]"
		elif cursor == 2:
			_year = f"[{_year}]"

		if cursor == 0:
			print("  ↑")
		elif cursor == 1:
			print("     ↑")
		elif cursor == 2:
			print("        ↑")

		print(f"{_day}.{_month}.{_year}")

		if cursor == 0:
			print("  ↓")
		elif cursor == 1:
			print("     ↓")
		elif cursor == 2:
			print("        ↓")

		key = keyboardScanner()
		if key == "enter":
			return day, month, year
		elif key == "up":
			if cursor == 0:
				day += 1
			elif cursor == 1:
				month += 1
			elif cursor == 2:
				year += 1

		elif key == "down":
			if cursor == 0:
				day -= 1
			elif cursor == 1:
				month -= 1
			elif cursor == 2:
				year -= 1

		elif key == "right":
			cursor += 1
			cursor = min(cursor, 2)

		elif key =="left":
			cursor -= 1
			cursor = max(cursor, 0)

		# set min / max for day, month, year
		month = max(1, min(month, 12))
		year = max(1, year)
		day = max(1, min(day, calendar.monthrange(year, month)[1]))
