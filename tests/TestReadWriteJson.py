from unittest.mock import patch, mock_open
import unittest
import sys
import os

sys.dont_write_bytecode = True
sys.path.append("./../lib/")

import readWriteJson as rwj

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
