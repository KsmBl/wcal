from pynput import keyboard
import time

# waits until a key is pressed
def keyboardScanner():
	keyPressed = {"key": None}

	def on_press(key):
		keyPressed["key"] = key
		return False

	with keyboard.Listener(on_press=on_press) as listener:
		listener.join()

	key = keyPressed["key"]

	if hasattr(key, 'char') and key.char is not None:
		return key.char
	else:
		return str(key)
