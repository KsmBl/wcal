#!/usr/bin/env python3
from datetime import datetime
import sys
import os

sys.dont_write_bytecode = True

# import custom libs
scriptDir = os.path.dirname(os.path.realpath(__file__))
libPath = os.path.join(scriptDir, 'lib')
sys.path.append(libPath)

from getConfig import getConfig, createConfigFile
from settingsMenu import settingsMenu
from askQuestion import askQuestion
from syncHandler import syncFiles
from chooseList import chooseList
from getDate import getDate
from jumpTo import *
from log import log

def mainMenu():
	menus = ["current Month", "jump to Date", "settings", "Exit", "sync files"]

	while True:
		position = 0

		# get current Day as header for chooseList()
		now = datetime.now()
		now_formated = now.strftime("%d.%m.%Y")
		day = now.strftime("%A")

		listItem = chooseList(menus, f" {now_formated} | {day}\n")

		if listItem == None:
			sys.exit(0)

		position = menus.index(listItem)

		if position == 0:
			rt = jumpToCurrentMonth()

		elif position == 1:
			day, month, year = getDate()
			rt = jumpToDate(day, month, year)

		elif position == 2:
			settingsMenu()

		elif position == 3:
			sys.exit(0)

		elif position == 4:
			rt = syncFiles()
			if rt[0] == 0:
				askQuestion("Files synced", ["OK"])
			else:
				askQuestion(rt[1], ["OK"])

createConfigFile()
SAVE_DIRECTORY = os.path.expanduser(getConfig("highlightSaveDirectory"))

if not os.path.exists(SAVE_DIRECTORY):
	log(0, "create save directory")
	os.makedirs(SAVE_DIRECTORY)

mainMenu()
