import json
import unittest
from pathlib import Path
from dotenv import load_dotenv
import os
from manager.key_objects import KeyRingManager, CommuneKey

load_dotenv()


class TestKeyRingManager(unittest.TestCase):
    def setUp(self):
        self.km = KeyRingManager()

    def test_keyring_manager(self):
        self.assertTrue(isinstance(self.km, KeyRingManager))

    def test_keyring(self):
        expected_results = get_expected_results("kmKeyring")
        results = self.km.keyring
        self.assertEqual(str(results), expected_results)

    def test_keynames(self):
        expected_results = get_expected_results("kmKeynames")
        results = self.km.keynames
        self.assertEqual(str(results), expected_results)

    def test_key2address(self):
        expected_results = get_expected_results("kmKey2Addresses")
        results = self.km.key2ss58addresses
        self.assertEqual(str(results), expected_results)

    def test_mnemonics(self):
        expected_results = get_expected_results("kmMnemonics")
        results = self.km.key2mnemonics
        self.assertEqual(str(results), expected_results)

class TestCommuneKey(unittest.TestCase):
    def setUp(self):
        self.key = CommuneKey

    def test_key(self):
        results = self.key
        path = Path.home() / "commune" / "manager" / "tests" / "test.json"
        data = json.loads(path.read_text(encoding="utf-8"))["data"]
        expected_results = CommuneKey(**json.loads(data))
        results = self.key(**json.loads(data))
        self.assertTrue(isinstance(results, CommuneKey))
        self.assertEqual(results, expected_results)

def get_expected_results(result="kmKeyring"):
    result_object = {
        "kmKeyring": os.getenv("kmKeyring"),
        "kmKeynames": os.getenv("kmKeynames"),
        "kmKey2Addresses": os.getenv("kmKey2Addresses"),
        "kmMnemonics": os.getenv("kmMnemonics"),
        }
    return result_object[result]
    