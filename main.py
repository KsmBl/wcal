#!/usr/bin/env python3
from datetime import datetime
import time
import sys
import os

sys.dont_write_bytecode = True

# import custom libs
scriptDir = os.path.dirname(os.path.realpath(__file__))
libPath = os.path.join(scriptDir, 'lib')
sys.path.append(libPath)

from chooseList import chooseList
from getDate import getDate
from getConfig import *
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

createConfigFile()
SAVE_DIRECTORY = os.path.expanduser(getConfig("highlightSaveDirectory"))

if not os.path.exists(SAVE_DIRECTORY):
	os.makedirs(SAVE_DIRECTORY)

mainMenu()
