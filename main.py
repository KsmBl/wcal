#!/usr/bin/env python3
from datetime import datetime
import calendar
import keyboard
import json
import math
import time
import sys
import os

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

def selectController(day, month, year, highlightDays):
	cursorDay = day

	monthStart, monthLength = calendar.monthrange(year, month)

	while True:
		os.system('clear')
		printMonth(monthStart, monthLength, highlightDays, cursorDay, calendar.month_name[month], year)
		key = keyboardScanner()

		if key == "left":
			cursorDay -= 1
			if cursorDay < 1:
				cursorDay = 1

		elif key == "right":
			cursorDay += 1
			if cursorDay > monthLength:
				cursorDay = monthLength

		elif key == "up":
			cursorDay -= 7
			if cursorDay < 1:
				cursorDay = 1

		elif key == "down":
			cursorDay += 7
			if cursorDay > monthLength:
				cursorDay = monthLength

		elif key == "q":
			return "quit"

def readJson(path):
	if os.path.exists(f"{SAVE_DIRECTORY}/{path}"):
		with open(f"{SAVE_DIRECTORY}/{path}") as jsonData:
			return json.load(jsonData)
	else:
		return None

def keyboardScanner():
	event = keyboard.read_event()
	if event.event_type == keyboard.KEY_DOWN:
		return event.name

def jumpToDate(day, month, year):
	highlights = readJson(f"{year}/{month}.json")
	highlightDays = []

	if highlights == None:
		highlightDays = []
	else:
		for i in highlights:
			highlightDays.append(int(i))

	return selectController(day, month, year, highlightDays)

def currentMonth():
	currentDay = datetime.now().day
	currentMonth = datetime.now().month
	currentYear = datetime.now().year
	return jumpToDate(currentDay, currentMonth, currentYear)

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
			if cursor > 2:
				cursor = 2

		elif key =="left":
			cursor -= 1
			if cursor < 0:
				cursor = 0

		if month > 12:
			month = 12

		if month < 1:
			month = 1

		if year < 1:
			year = 1

		if day > calendar.monthrange(year, month)[1]:
			day = calendar.monthrange(year, month)[1]
		elif day < 1:
			day = 1

def mainMenu():
	menus = ["current Month", "jump to Date", "Exit"]
	position = 0
	cursor = " * "
	noCursor = "   "

	while True:
		os.system('clear')
		for i in range(len(menus)):
			if i == position:
				print(cursor + menus[i])
			else:
				print(noCursor + menus[i])

		key = keyboardScanner()

		if key == "up":
			position -= 1
			if position < 0:
				position = 0

		elif key == "down":
			position += 1
			if position > len(menus) - 1:
				position = len(menus) - 1

		elif key == "enter":
			if position == 1:
				day, month, year = getDate()
				rt = jumpToDate(day, month, year)
			elif position == 0:
				currentMonth()
			elif position == 2:
				sys.exit(0)

		elif key == "q":
			sys.exit(0)

if not os.path.exists(SAVE_DIRECTORY):
	os.makedirs(SAVE_DIRECTORY)

mainMenu()
