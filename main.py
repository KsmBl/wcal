#!/usr/bin/env python3
from datetime import datetime
import calendar
import math
import time
import sys
import os

sys.path.append(os.path.abspath("./lib/"))
from keyboardScanner import keyboardScanner
from chooseList import chooseList
from readJson import readJson
from getDate import getDate

SAVE_DIRECTORY = "./savedData"

def printMonth(startDay, monthLength, highlight, cursor, header1, header2):
	weekCount = math.ceil((startDay + monthLength) / 7)
	weeks = []
	currentDay = 0

	allDays = []

	# get array with all days
	for i in range(startDay):
		allDays.append("X")
	for i in range(monthLength):
		allDays.append(i + 1)

	# create dayArray for each week
	for i in range(weekCount):
		currentWeek = []
		for ii in range (7):
			try:
				currentWeek.append(allDays[currentDay])
				currentDay += 1
			except:
				currentWeek.append("X")

		weeks.append(currentWeek)
	
	print(f" {header1:<23}{header2:>4} \n")
	print(" Mo  Tu  We  Th  Fr  Sa  Su ")

	for week in weeks:
		line = ""
		for day in week:
			if day == cursor and day in highlight:
				line += ("{" + str(day) + "}").rjust(4)
			elif day == cursor:
				line += ("(" + str(day) + ")").rjust(4)
			elif day in highlight:
				line += ("[" + str(day) + "]").rjust(4)
			else:
				line += str(day).rjust(3) + " "

		print(line)

def monthViewer(day, month, year, highlightDays):
	cursorDay = day

	monthStart, monthLength = calendar.monthrange(year, month)

	while True:
		os.system('clear')
		printMonth(monthStart, monthLength, highlightDays, cursorDay, calendar.month_name[month], year)
		key = keyboardScanner()

		if key == "left":
			cursorDay = max(cursorDay - 1, 1)
			# TODO: goto last month

		elif key == "right":
			cursorDay = min(cursorDay + 1, monthLength)
			# TODO: goto next month

		elif key == "up":
			cursorDay = max(cursorDay - 7, 1)

		elif key == "down":
			cursorDay = min(cursorDay + 7, monthLength)

		elif key == "enter":
			return "highlight_Day", cursorDay, month, year

		elif key == "q":
			return "quit"

def jumpToDate(day, month, year):
	highlights = readJson(f"{year}/{month}.json", SAVE_DIRECTORY)
	highlightDays = []

	if highlights == None:
		highlightDays = []
	else:
		for i in highlights:
			highlightDays.append(int(i))

	return monthViewer(day, month, year, highlightDays)

def currentMonth():
	currentDay = datetime.now().day
	currentMonth = datetime.now().month
	currentYear = datetime.now().year
	return jumpToDate(currentDay, currentMonth, currentYear)

def getString():
	customString = ""
	availabeChars = "abcdefghijklmnopqrstuvwxyz1234567890"

	while True:
		os.system("clear")
		print(customString)
		key = keyboardScanner()

		if key in availabeChars:
			customString += key
		elif key == "space":
			customString += " "
		elif key == "enter":
			return customString
		else:
			continue

def editDay(day, month, year):
	highlights = readJson(f"{year}/{month}.json", SAVE_DIRECTORY)
	dayEntries = []
	selectEntry = 0
	cursor = " * "
	noCursor = "   "

	if str(day) in highlights:
		dayEntries = highlights[str(day)]
		arrayDayEntries = [f"{t} | {msg}" for t, msg in sorted(dayEntries.items())]
		arrayDayEntries.append("new Entry +")
		picked = chooseList(arrayDayEntries)


def mainMenu():
	menus = ["current Month", "jump to Date", "Exit", "chooseList"]

	while True:
		position = chooseList(menus)
		if position == 1:
			day, month, year = getDate()
			rt = jumpToDate(day, month, year)
			if rt[0] == "highlight_Day":
				hlDay = rt[1]
				hlMonth = rt[2]
				hlYear = rt[3]

				editDay(hlDay, hlMonth, hlYear)
		elif position == 0:
			rt = currentMonth()
			if rt[0] == "highlight_Day":
				hlDay = rt[1]
				hlMonth = rt[2]
				hlYear = rt[3]

				editDay(hlDay, hlMonth, hlYear)
		elif position == 2:
			sys.exit(0)
		elif position == 3:
			rt = chooseList(["14:00 : POGGERS", "14:04 : massive POGCHAMP", "14:61 : hyperpog"])
			print(rt)
			time.sleep(1)

if not os.path.exists(SAVE_DIRECTORY):
	os.makedirs(SAVE_DIRECTORY)

mainMenu()
