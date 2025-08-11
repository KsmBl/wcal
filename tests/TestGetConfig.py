from unittest.mock import patch, mock_open, MagicMock
import unittest
import sys
import os

sys.dont_write_bytecode = True
sys.path.append("./../lib/")

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
		handle.write.assert_not_called()
		mockConfig.write.assert_called_once_with(handle)
