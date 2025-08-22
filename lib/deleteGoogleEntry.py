from gcsa.google_calendar import GoogleCalendar
from getConfig import getConfig

# get all google calendar entrys for the current month
def deleteGoogleEntry(eventId):
	email = getConfig("googleCalEmail")
	gc = GoogleCalendar(email)
	gc.delete_event(eventId)
	return "reloadDay"
