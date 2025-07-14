#!/usr/bin/env python3
from datetime import datetime
import time
import sys
import os

sys.dont_write_bytecode = True

# import custom libs
sys.path.append(os.path.abspath("./lib/"))
from chooseList import chooseList
from getConfig import getConfig
from getDate import getDate
from jumpTo import *

def mainMenu():
	menus = ["current Month", "jump to Date", "Exit"]

	while True:
		position = 0
		listItem = chooseList(menus)

		if listItem == None:
			sys.exit(0)

		position = menus.index(listItem)

		if position == 1:
			day, month, year = getDate()
			rt = jumpToDate(day, month, year)

		elif position == 0:
			rt = jumpToCurrentMonth()

		elif position == 2:
			sys.exit(0)

SAVE_DIRECTORY = getConfig("highlightSaveDirectory")

if not os.path.exists(SAVE_DIRECTORY):
	os.makedirs(SAVE_DIRECTORY)

mainMenu()
