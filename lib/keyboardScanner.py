import termios
import sys
import tty

import time

translationTable = {
	'\x1b[A' : "up",
	'\x1b[B' : "down",
	'\x1b[C' : "right",
	'\x1b[D' : "left"
}

def keyboardScanner():
	fd = sys.stdin.fileno()
	old_settings = termios.tcgetattr(fd)
	try:
		tty.setraw(fd)
		ch1 = sys.stdin.read(1)

		if ch1 == '\x1b':
			ch2 = sys.stdin.read(1)
			if ch2 == '[':
				ch3 = sys.stdin.read(1)
				return translationTable[f"{ch1}{ch2}{ch3}"]
			else:
				return None
		else:
			if ch1 in ('\r', '\n'):
				return 'enter'
			else:
				return ch1
	
	finally:
		termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
