from unittest.mock import patch
import unittest
import sys

sys.dont_write_bytecode = True
sys.path.append("./../lib/")

import deleteEntry as de

class TestDeleteEntry(unittest.TestCase):

	@patch('deleteEntry.writeJson')
	def testDeleteEntryNormal(self, mock_writeJson):
		highlights = {
			"2025-08-06": {
				"1": "Highlight A",
				"2": "Highlight B"
			}
		}

		result = de.deleteEntry("1", highlights, "2025-08-06", "/fake/path.json")

		# Prüfen, dass der Eintrag gelöscht wurde
		self.assertNotIn("1", highlights["2025-08-06"])
		self.assertIn("2", highlights["2025-08-06"])

		# writeJson sollte 1x aufgerufen werden (kein "reloadDay")
		self.assertEqual(mock_writeJson.call_count, 1)
		self.assertIsNone(result)

	@patch('deleteEntry.writeJson')
	def testDeleteEntryDayEmpty(self, mock_writeJson):
		highlights = {
			"2025-08-06": {
				"1": "Highlight A"
			}
		}

		result = de.deleteEntry("1", highlights, "2025-08-06", "/fake/path.json")

		self.assertNotIn("2025-08-06", highlights)

		self.assertEqual(mock_writeJson.call_count, 2)
		self.assertEqual(result, "reloadDay")
