from gcsa.google_calendar import GoogleCalendar
from datetime import datetime, timedelta
import calendar

gc = GoogleCalendar("katzen.sind.lecker69@gmail.com")

now = datetime.now()

start_of_month = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
lastDay = calendar.monthrange(now.year, now.month)[1]
end_of_month = now.replace(day=lastDay, hour=23, minute=59, second=59, microsecond=999999)

events = gc.get_events(time_min=start_of_month, time_max=end_of_month)

for event in events:
	status = event.other.get('status', 'confirmed')
	if status != 'cancelled':
		start = event.start.strftime('%A, %d.%m.%Y %H:%M') if isinstance(event.start, datetime) else event.start.strftime('%A, %d.%m.%Y')
		print(f"{start} – {event.summary}")
