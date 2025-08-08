from unittest.mock import patch, mock_open, MagicMock
import unittest
import sys
import os

sys.dont_write_bytecode = True
sys.path.append("./lib/")

import readWriteJson as rwj
import deleteEntry as de
from log import log
import syncHandler
import getConfig

class TestGetConfig(unittest.TestCase):

	@patch('getConfig.os.path.isfile', return_value=False)
	@patch('getConfig.os.makedirs')
	@patch('builtins.open', new_callable=mock_open)
	def testCreateConfigFile(self, mock_file, mockMakeDirs, mock_isfile):
		with patch('getConfig.os.path.join', return_value="/fake/path/config.ini"), \
			patch('getConfig.os.path.expanduser', side_effect=lambda x: x.replace("~", "/home/testuser")):

			getConfig.createConfigFile()

			mockMakeDirs.assert_called_once_with("/home/testuser/.config/wcal/", exist_ok=True)

			mock_file.assert_called_once_with("/fake/path/config.ini", 'w', encoding='utf-8')
			handle = mock_file()
			handle.write.assert_called_once()
 

	@patch('getConfig.configparser.ConfigParser')
	@patch('getConfig.os.path.expanduser', return_value="/home/testuser/.config/wcal/config.ini")
	def testGetConfig(self, mock_expanduser, mockConfig_parser_class):
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
	def testSetConfig(self, mock_file, mock_expanduser, mockConfig_parser_class):
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


class TestReadWriteJson(unittest.TestCase):

	@patch('readWriteJson.getConfig', return_value="~/mock/path")
	@patch('readWriteJson.os.path.exists', return_value=True)
	@patch('builtins.open', new_callable=mock_open, read_data='{"key": "value"}')
	@patch('readWriteJson.json.load', return_value={"key": "value"})
	def testReadJsonExists(self, mock_json_load, mock_open_file, mock_exists, mock_get_config):
		result = rwj.readJson("test.json")

		expected_path = os.path.expanduser("~/mock/path/test.json")
		mock_open_file.assert_called_once_with(expected_path)
		mock_json_load.assert_called_once()
		self.assertEqual(result, {"key": "value"})

	@patch('readWriteJson.getConfig', return_value="~/mock/path")
	@patch('readWriteJson.os.path.exists', return_value=False)
	def testReadJsonNotExists(self, mock_exists, mock_get_config):
		result = rwj.readJson("nonexistent.json")
		self.assertIsNone(result)

	@patch('readWriteJson.getConfig', return_value="~/mock/path")
	@patch('builtins.open', new_callable=mock_open)
	@patch('readWriteJson.json.dump')
	def testWriteJson(self, mock_json_dump, mock_open_file, mock_get_config):
		data = {"key": "value"}

		rwj.writeJson(data, "output.json")

		expected_path = os.path.expanduser("~/mock/path/output.json")
		mock_open_file.assert_called_once_with(expected_path, "w", encoding="utf-8")
		mock_json_dump.assert_called_once_with(data, mock_open_file(), ensure_ascii=False, indent=2)


class TestSyncFiles(unittest.TestCase):

	@patch("syncHandler.getRequest")
	@patch("syncHandler.getConfig")
	@patch("syncHandler.log")
	def testRemoteServerUnreachable(self, mock_log, mock_getConfig, mock_getRequest):
		mock_getConfig.side_effect = lambda key: {
			"highlightSaveDirectory": "~/test/highlights",
			"syncIP": "127.0.0.1",
			"syncPort": "8000"
		}[key]
		mock_getRequest.side_effect = Exception("Connection failed")

		result = syncHandler.syncFiles()

		self.assertEqual(result, [1, "http://127.0.0.1:8000 not reachable"])
		mock_log.assert_called_with(1, "remote Server 'http://127.0.0.1:8000' not reachable")

	@patch("syncHandler.getRequest")
	@patch("syncHandler.getConfig")
	@patch("syncHandler.log")
	def testEverythingAlreadySynced(self, mock_log, mock_getConfig, mock_getRequest):
		mock_getConfig.side_effect = lambda key: {
			"highlightSaveDirectory": "~/test/highlights",
			"syncIP": "127.0.0.1",
			"syncPort": "8000"
		}[key]
		mock_getRequest.side_effect = [
			{"status": "pong"},
			{"hash": "abc123"},
		]

		with patch("syncHandler.getOwnWholeChecksum", return_value="abc123"):
			result = syncHandler.syncFiles()

		self.assertEqual(result, [0, "everything synced"])
		mock_log.assert_called_with(0, "everything synced")

	@patch("syncHandler.uploadFile")
	@patch("syncHandler.getAllFileNames")
	@patch("syncHandler.getAllOwnFileNames")
	@patch("syncHandler.getRequest")
	@patch("syncHandler.getConfig")
	@patch("syncHandler.log")
	def testLocalFilesNeedUpload(self, mock_log, mock_getConfig, mock_getRequest, mock_getOwnFiles, mock_getRemoteFiles, mock_upload):
		mock_getConfig.side_effect = lambda key: {
			"highlightSaveDirectory": "~/test/highlights",
			"syncIP": "127.0.0.1",
			"syncPort": "8000"
		}[key]

		mock_getRequest.side_effect = [
			{"status": "pong"},
			{"hash": "xyz"},
		]

		mock_getOwnFiles.return_value = ["file1.json", "file2.json"]
		mock_getRemoteFiles.return_value = ["file2.json"]
		mock_upload.return_value = [0, "uploaded"]

		with patch("syncHandler.getOwnWholeChecksum", return_value="abc"):
			result = syncHandler.syncFiles()

		self.assertEqual(result, [0, "everything synced"])


class TestLogFunction(unittest.TestCase):

	@patch("log.getConfig")
	@patch("log.time.time")
	@patch("log.os.path.exists")
	@patch("builtins.open", new_callable=mock_open)
	def test_log_writes_correct_content(self, mock_file, mock_exists, mock_time, mock_getConfig):
		mock_getConfig.return_value = "~/test_log.txt"
		mock_time.return_value = 1723123456.789  # Mocked timestamp
		mock_exists.return_value = False  # File doesn't exist

		log(0, "Test message")

		expected_path = os.path.expanduser("~/test_log.txt")

		mock_file.assert_any_call(expected_path, 'w')
		mock_file().write.assert_any_call("[timestamp][loglevel][message]\n")

		expected_timestamp = round(mock_time.return_value, 2)
		expected_line = f"[{expected_timestamp}][ INFO  ] : Test message\n"

		mock_file.assert_any_call(expected_path, 'a', encoding="utf-8")
		mock_file().write.assert_any_call(expected_line)

	@patch("log.getConfig")
	@patch("log.time.time")
	@patch("log.os.path.exists")
	@patch("builtins.open", new_callable=mock_open)
	def test_log_skips_header_if_exists(self, mock_file, mock_exists, mock_time, mock_getConfig):
		mock_getConfig.return_value = "~/test_log.txt"
		mock_time.return_value = 1234567.89
		mock_exists.return_value = True  # File exists, so no header

		log(2, "Error occurred")

		expected_path = os.path.expanduser("~/test_log.txt")
		expected_line = f"[{round(mock_time.return_value, 2)}][ ERROR ] : Error occurred\n"

		mock_file.assert_called_with(expected_path, 'a', encoding="utf-8")
		mock_file().write.assert_called_with(expected_line)


if __name__ == '__main__':
	unittest.main()
