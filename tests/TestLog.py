from unittest.mock import patch, mock_open
import unittest
import sys
import os

sys.dont_write_bytecode = True
sys.path.append("./../lib/")

from log import log

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
