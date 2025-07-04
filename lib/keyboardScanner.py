import keyboard

# waits until a key is pressed
def keyboardScanner():
	while True:
		event = keyboard.read_event()
		if event.event_type == keyboard.KEY_DOWN:
			return event.name
		else:
			continue
