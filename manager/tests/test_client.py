import unittest
from client import CommuneClient
from manager.key_objects import KeyRingManager, CommuneKey
from typing import Dict
from loguru import logger


class TestCommuneClient(unittest.TestCase):
    def setUp(self):
        self.client = CommuneClient()

    def test_client(self):
        self.assertTrue(isinstance(self.client, CommuneClient))
        self.assertTrue(isinstance(self.client.keynames, list))
        self.assertTrue(isinstance(self.client.km.key2ss58addresses, dict))
        self.assertTrue(isinstance(self.client.km.key2mnemonics, dict))

    def test_getbalance(self):
        result = self.client.getbalance(self.client.km.keynames[1])
        self.assertTrue(result)
        self.assertEqual("vali::project_management.json", self.client.km.keynames[1])

    def test_getbalances(self):
        result = self.client.getbalances()
        self.assertTrue(result)
        self.assertTrue(isinstance(result, dict))
