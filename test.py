from unittest.mock import patch, mock_open, MagicMock
import unittest
import sys
import os

sys.path.append("./lib/")

import readWriteJson as rwj
import deleteEntry as de
import getConfig

class TestGetConfig(unittest.TestCase):

	@patch('getConfig.os.path.isfile', return_value=False)
	@patch('getConfig.os.makedirs')
	@patch('builtins.open', new_callable=mock_open)
	def test_create_config_file(self, mock_file, mockMakeDirs, mock_isfile):
		with patch('getConfig.os.path.join', return_value="/fake/path/config.ini"), \
			patch('getConfig.os.path.expanduser', side_effect=lambda x: x.replace("~", "/home/testuser")):

			getConfig.createConfigFile()

			mockMakeDirs.assert_called_once_with("/home/testuser/.config/wcal/", exist_ok=True)

			mock_file.assert_called_once_with("/fake/path/config.ini", 'w', encoding='utf-8')
			handle = mock_file()
			handle.write.assert_called_once()
 

	@patch('getConfig.configparser.ConfigParser')
	@patch('getConfig.os.path.expanduser', return_value="/home/testuser/.config/wcal/config.ini")
	def test_get_config(self, mock_expanduser, mockConfig_parser_class):
		mockConfig = MagicMock()
		mockConfig.__getitem__.return_value = {'someKey': 'someValue'}
		mockConfig_parser_class.return_value = mockConfig

		# simulate ["configs"]["someKey"]
		mockConfig.__getitem__.return_value = {'someKey': 'someValue'}

		getConfig.getConfig('someKey')
		mockConfig.read.assert_called_once_with("/home/testuser/.config/wcal/config.ini")
		mockConfig.__getitem__.assert_called_with("configs")


	@patch('getConfig.configparser.ConfigParser')
	@patch('getConfig.os.path.expanduser', return_value="/home/testuser/.config/wcal/config.ini")
	@patch('builtins.open', new_callable=mock_open)
	def test_set_config(self, mock_file, mock_expanduser, mockConfig_parser_class):
		mockConfig = MagicMock()
		mockConfig.sections.return_value = ["configs"]
		mockConfig_parser_class.return_value = mockConfig

		getConfig.setConfig("syncPort", "9999")

		mockConfig.read.assert_called_once_with("/home/testuser/.config/wcal/config.ini")
		mockConfig.set.assert_called_once_with("configs", "syncPort", "9999")
		mock_file.assert_called_once_with("/home/testuser/.config/wcal/config.ini", 'w')
		handle = mock_file()
		handle.write.assert_not_called()  # Because config.write() writes to file, not file.write directly
		mockConfig.write.assert_called_once_with(handle)


class TestDeleteEntry(unittest.TestCase):

	@patch('deleteEntry.writeJson')
	def test_delete_entry_normal(self, mock_writeJson):
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
	def test_delete_entry_day_empty(self, mock_writeJson):
		highlights = {
			"2025-08-06": {
				"1": "Highlight A"
			}
		}

		result = de.deleteEntry("1", highlights, "2025-08-06", "/fake/path.json")

		self.assertNotIn("2025-08-06", highlights)

		self.assertEqual(mock_writeJson.call_count, 2)
		self.assertEqual(result, "reloadDay")


class TestReadWriteJson(unittest.TestCase):

	@patch('readWriteJson.getConfig', return_value="~/mock/path")
	@patch('readWriteJson.os.path.exists', return_value=True)
	@patch('builtins.open', new_callable=mock_open, read_data='{"key": "value"}')
	@patch('readWriteJson.json.load', return_value={"key": "value"})
	def test_read_json_exists(self, mock_json_load, mock_open_file, mock_exists, mock_get_config):
		result = rwj.readJson("test.json")

		expected_path = os.path.expanduser("~/mock/path/test.json")
		mock_open_file.assert_called_once_with(expected_path)
		mock_json_load.assert_called_once()
		self.assertEqual(result, {"key": "value"})

	@patch('readWriteJson.getConfig', return_value="~/mock/path")
	@patch('readWriteJson.os.path.exists', return_value=False)
	def test_read_json_not_exists(self, mock_exists, mock_get_config):
		result = rwj.readJson("nonexistent.json")
		self.assertIsNone(result)

	@patch('readWriteJson.getConfig', return_value="~/mock/path")
	@patch('builtins.open', new_callable=mock_open)
	@patch('readWriteJson.json.dump')
	def test_write_json(self, mock_json_dump, mock_open_file, mock_get_config):
		data = {"key": "value"}

		rwj.writeJson(data, "output.json")

		expected_path = os.path.expanduser("~/mock/path/output.json")
		mock_open_file.assert_called_once_with(expected_path, "w", encoding="utf-8")
		mock_json_dump.assert_called_once_with(data, mock_open_file(), ensure_ascii=False, indent=2)


if __name__ == '__main__':
	unittest.main()
