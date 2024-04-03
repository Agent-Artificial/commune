from commune.module import Module 
import os
import json
from pathlib import Path
from pydantic import BaseModel
from typing import Optional, Dict, List, Any, Union
from abc import ABC, abstractmethod
from commune.subspace.subspace import Subspace
from manager.encryption import encrypt_json, decrypt_json
from getpass import getpass
from dotenv import load_dotenv


load_dotenv()

c = Module()
subspace = Subspace()


class KeyConfigModel(BaseModel):
    """
    A pydantic model for storing key configurations.
    """
    crypto_type: Union[str, int]
    """
    The cryptographic algorithm used to generate the key pair.
    """
    seed_hex: str
    """
    The seed used to generate the key pair in hexadecimal format.
    """
    derive_path: Optional[Union[Path, str]]
    """
    The derivation path used to derive the key pair from the seed, if applicable.
    """
    path: Union[Path, str]
    """
    The location of the key file.
    """
    ss58_format: Union[str, int]
    """
    The ss58 address format of the key.
    """
    public_key: str
    """
    The public key of the key pair in hexadecimal format.
    """
    private_key: str
    """
    The private key of the key pair in hexadecimal format.
    """
    mnemonic: str
    """
    The mnemonic seed phrase used to generate the key pair.
    """
    ss58_address: str
    """
    The ss58 address of the key.
    """


class AbstractKey(ABC):
    """Abstract base class for key objects."""

    @abstractmethod
    def __init__(self):
        """Abstract initializer."""

    @abstractmethod
    def key2address(self) -> Dict[str, str]:
        """Returns a dictionary with the name and ss58 address for the key."""

    @abstractmethod
    def key2mnemonic(self) -> Dict[str, str]:
        """Returns a dictionary with the name and mnemonic for the key. Requires authorization."""

    @abstractmethod
    def key2path(self) -> Dict[str, str]:
        """Returns a dictionary with the name and path for the key. Requires authorization."""

    @abstractmethod
    def module_information(self) -> float:
        """Returns the module information for the key."""


        
class CommuneKey(KeyConfigModel, AbstractKey):
    def __init__(
        self,
        crypto_type,
        seed_hex,
        derive_path,
        path,
        ss58_format,
        public_key,
        private_key,
        mnemonic,
        ss58_address,
        ):
        """
        Initializes the object with the given configuration parameters.

        Args:
            **kwargs: Arbitrary keyword arguments.

        Returns:
            None
        """
        super().__init__(
            crypto_type = crypto_type,
            seed_hex = seed_hex,
            derive_path = derive_path,
            path = str(path),
            ss58_format = ss58_format,
            public_key = public_key,
            private_key = private_key,
            mnemonic = mnemonic,
            ss58_address = ss58_address,
            )
        

    def key2address(self) -> Dict[str, str]:
        """
        Returns a dictionary mapping the name of the object to its corresponding SS58 address.

        :return: A dictionary with the object name as the key and the SS58 address as the value.
        :rtype: Dict[str, str]
        """
        return {
            self.name: self.ss58_address
        }

    def key2mnemonic(self) -> Dict[str, str]:
        """
        Generates a dictionary that maps the name of the object to its mnemonic.

        Returns:
            Dict[str, str]: A dictionary where the keys are the names of the object and the values are the corresponding mnemonics.
        """
        return {
            self.name: self.mnemonic
        }

    def key2path(self) -> Dict[str, str]:
        """
        Returns a dictionary mapping the name of the object to its path.

        :return: A dictionary with the object's name as the key and its path as the value.
        :rtype: Dict[str, str]
        """
        return {
            self.name: self.path
        }
    def staked_balance(self) -> float:
        return 0

    def module_information(self) -> float:
        return 0


class KeyRingManager:
    """
    Class for managing keys stored on the system.

    Attributes:
        keyring (Dict[str, Dict[str, str]]): A dictionary of keys and their corresponding data.
        key2ss58address (Dict[str, str]): A dictionary of keys and their corresponding SS58 addresses.
        key2mnemonic (Dict[str, str]): A dictionary of keys and their corresponding mnemonic phrases.
    """
    home = Path("~").expanduser()
    pwd = Path(home / "commune").absolute()
    key_path = Path(home/ ".commune" / "key").absolute()

    def __init__(self):
        self.keyring: Dict[str, CommuneKey] = {}
        self.key2ss58addresses: Dict[str, str] = {}
        self.key2mnemonics: Dict[str, str] = {}

    def load_keys(self, key_path: Path) -> None:
        """
        Load keys from the system.

        Args:
            password (str): The password to decrypt the keys with.
            path (str): The path to the key folder.
        """
        keypath = Path(key_path) or KeyRingManager.key_path
        self.parse_system_keys(keypath)

    def get_keys(self) -> Dict[str, str]:
        """
        Returns a dictionary of keys and their corresponding SS58 addresses.

        :return: A dictionary of keys and their corresponding SS58 addresses.
        :rtype: Dict[str, str]
        """
        return self.key2ss58addresses

    def parse_system_keys(self, key_path: Path) -> None:
        """
        Parse the keys stored on the system.

        Args:
            password (str): The password to decrypt the keys with.
            key_path (str): The path to the key folder.
        """
        keypath = Path(key_path) or KeyRingManager.key_path
        files = os.listdir(keypath)
        for file in files:
            filepath = Path(file)
            filename = filepath.name
            if filename == "info.json" or filename == "key2address.json":
                continue
            file_path = keypath / filename
            if file_path.suffix == ".json":
                try:
                    data = json.loads(file_path.read_text())
                    data = json.loads(data["data"])
                    key = CommuneKey(
                        path=data["path"],
                        crypto_type=data["crypto_type"] or 1,
                        ss58_address=data["ss58_address"] or "",
                        mnemonic=data["mnemonic"] or "",
                        derive_path=data["derive_path"],
                        private_key=data["private_key"] or "",
                        public_key=data["public_key"] or "",
                        seed_hex=data["seed_hex"] or "",
                        ss58_format=data["ss58_format"] or 42,
                    )
                except Exception as e:
                    raise ValueError(f"Failed to parse key {filename} due to {e}") from e

                self.keyring[filename] = key
                self.key2ss58addresses[filename] = key.ss58_address
                self.key2mnemonics[filename] = key.mnemonic

    def encrypt(self, keyname: str, password: str) -> Dict[str, str]:
        """
        Encrypt a key.

        Args:
            keyname (str): The name of the key to encrypt.
            password (str): The password to encrypt the key with.

        Returns:
            Dict[str, str]: The encrypted key.
        """
        key: CommuneKey = self.keyring[keyname]
        if isinstance(key, CommuneKey):
            json_key = key.model_dump()

        return encrypt_json(json_key, password)

    def decrypt(self, keyname: str, password: str) -> Dict[str, CommuneKey]:
        """
        Decrypt a key.

        Args:
            keyname (str): The name of the key to decrypt.
            password (str): The password to decrypt the key with.

        Returns:
            Dict[str, str]: The decrypted key.
        """
        full_key = self.keyring[keyname]
        if isinstance(full_key, dict):
            decrypted = decrypt_json(full_key[keyname], password)
            self.keyring[keyname] = CommuneKey(**decrypted)
        return {keyname: self.keyring[keyname]}



if __name__== "__main__":
    km = KeyRingManager()
    km.load_keys(Path("~").expanduser() / ".commune" / "key")
    #print(km.keyring)
    #print(km.key2ss58addresses)
    #print(km.key2mnemonics)