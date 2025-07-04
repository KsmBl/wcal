import math

# print month with cursor and highlights and headers
def printMonth(startDay, monthLength, highlight, cursor, header1, header2):
	# calculate amount of weeks
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
