from gcsa.google_calendar import GoogleCalendar
from datetime import datetime, timedelta
from getConfig import getConfig
from getColor import allColors
import calendar

colorConvertion = {
	None : 3,
	"1" : 1,
	"2" : 4,
	"3" : 1,
	"4" : 6,
	"5" : 5,
	"6" : 6,
	"7" : 2,
	"8" : 0,
	"9" : 2,
	"10" : 4,
	"11" : 6,
}

# get all google calendar entrys for the current month
def getGoogleHighlights():
	email = getConfig("googleCalEmail")
	gc = GoogleCalendar(email)

	highlights = {}

	now = datetime.now()
	startOfMonth = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
	lastDay = calendar.monthrange(now.year, now.month)[1]
	endOfMonth = now.replace(day=lastDay, hour=23, minute=59, second=59, microsecond=999999)

	events = gc.get_events(time_min=startOfMonth, time_max=endOfMonth)

	for event in events:
		status = event.other.get('status', 'confirmed')
		if status == 'cancelled':
			continue

		startTime = event.start
		day_str = str(startTime.day)
		time_str = startTime.strftime("%H:%M")

		name = getattr(event, "summary", "Unbenannt")
		color = colorConvertion[getattr(event, "color_id", 0)]
	
		if day_str not in highlights:
			highlights[day_str] = {}

		highlights[day_str][time_str] = {
			"name": f"(G) {name}",
			"color": color
		}

	return highlights
