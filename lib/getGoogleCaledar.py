from gcsa.google_calendar import GoogleCalendar
from datetime import datetime, timedelta

calendar = GoogleCalendar("katzen.sind.lecker69@gmail.com")

startDate = datetime.now()
endDate = startDate + timedelta(days=7)

events = calendar.get_events(time_min=startDate, time_max=endDate)

print(f"📆 Termine vom {startDate.date()} bis {endDate.date()}:\n")
for event in events:
	print(f"- {event.start.strftime('%A, %d.%m.%Y %H:%M')} – {event.summary}")
