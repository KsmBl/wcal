from unittest.mock import patch
import unittest
import sys

sys.dont_write_bytecode = True
sys.path.append("./../lib/")

import syncHandler

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
