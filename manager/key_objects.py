from commune.module import Module 
import os
import json
from pathlib import Path
from pydantic import BaseModel
from typing import Optional, Dict, Union, Callable, Any
from abc import ABC, abstractmethod
from commune.subspace.subspace import Subspace
from manager.encryption import encrypt_json, decrypt_json
from dotenv import load_dotenv


load_dotenv()

c = Module()
subspace = Subspace()


class KeyConfigModel(BaseModel):
    crypto_type: Union[str, int]
    seed_hex: str
    derive_path: Optional[Union[Path, str]]
    path: Union[Path, str]
    ss58_format: Union[str, int]
    public_key: str
    private_key: str
    mnemonic: str
    ss58_address: str


class AbstractKey(ABC):

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
        ) -> None:
        """
        Initialize the class with the provided parameters.

        Parameters:
            crypto_type (str): The type of cryptocurrency.
            seed_hex (str): The seed in hexadecimal format.
            derive_path (str): The derivation path.
            path (str): The path.
            ss58_format (str): The ss58 format.
            public_key (str): The public key.
            private_key (str): The private key.
            mnemonic (str): The mnemonic.
            ss58_address (str): The ss58 address.

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
        
    def get_name(self) -> str:
        """
        A function that returns the name of the key.
        Returns:
            str: The name of the key.
        """
        return str(self.path).split("/")[-1].split(".")[0]
        

    def key2address(self) -> Dict[str, str]:
        """
        A function that generates a dictionary mapping the name to the SS58 address.
        Returns a dictionary with the name as key and SS58 address as value.
        """
        return {str(self.get_name): self.ss58_address}

    def key2mnemonic(self) -> Dict[str, str]:
        """
        A function that converts a key to a mnemonic and returns a dictionary with the key as the name and the mnemonic as the value.
        :return: A dictionary containing the key as the name and the mnemonic as the value.
        :rtype: Dict[str, str]
        """
        return {str(self.get_name): self.mnemonic}

    def key2path(self) -> Dict[str, Union[Path,str]]:
        """
        Generate a dictionary mapping the name to the path.
        Returns:
            Dict[str, Union[Path, str]]: A dictionary with the name as key and path as value.
        """
        return {str(self.get_name): self.path}
    
    def staked_balance(self) -> float:
        """
        A function that calculates the staked balance of the user.

        :return: a float representing the staked balance
        """
        return 0

    def module_information(self) -> float:
        """
        Retrieve information about the module.
        """
        return 0


class KeyRingManager:
    home = Path("~").expanduser()
    pwd = Path(home / "commune").absolute()
    key_path = Path(home/ ".commune" / "key").absolute()

    def __init__(self):
        """
        Initializes the class instance by setting up dictionaries for keyring, ss58 addresses, and mnemonics.
        Parses system keys from the specified key path and initializes keynames.
        """
        self.keyring: Dict[str, CommuneKey] = {}
        self.key2ss58addresses: Dict[str, str] = {}
        self.key2mnemonics: Dict[str, str] = {}
        self.parse_system_keys(self.key_path)
        self.keynames = [key for key in self.key2ss58addresses.keys()]

    def load_keys(self, key_path: Path) -> None:
        """
        Loads keys from the specified key path or from the default key path.
        
        :param key_path: The path to the keys.
        :return: None
        """
        keypath = Path(key_path) or KeyRingManager.key_path
        self.parse_system_keys(keypath)

    def get_keys(self) -> Dict[str, str]:
        """
        Return a dictionary of keys and their corresponding SS58 addresses.
        """
        return self.key2ss58addresses

    def parse_system_keys(self, key_path: Path) -> None:
        """
        Parse system keys from the given key_path. Update keyring mappings.
        :param key_path: Path to the directory containing system keys.
        :return: None
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
        A function that encrypts data using a specified keyname and password.
        
        Parameters:
            keyname (str): The name of the key to be used for encryption.
            password (str): The password to encrypt the data.
        
        Returns:
            Dict[str, str]: A dictionary containing the encrypted data.
        """
        key: CommuneKey = self.keyring[keyname]
        if isinstance(key, CommuneKey):
            json_key = key.model_dump()

        return encrypt_json(json_key, password)

    def decrypt(self, keyname: str, password: str) -> Dict[str, CommuneKey]:
        """
        Decrypts a specific key in the keyring using the provided password.

        Parameters:
            keyname (str): The name of the key to decrypt.
            password (str): The password used for decryption.

        Returns:
            Dict[str, CommuneKey]: A dictionary containing the decrypted key.
        """
        full_key = self.keyring[keyname]
        if isinstance(full_key, dict):
            decrypted = decrypt_json(full_key[keyname], password)
            self.keyring[keyname] = CommuneKey(**decrypted)
        return {keyname: self.keyring[keyname]}



if __name__== "__main__":
    km = KeyRingManager()
    #km.load_keys(Path("~").expanduser() / ".commune" / "key")
    #print(km.keyring)
    #print(km.keynames)
    #print(km.key2ss58addresses)
    #print(km.key2mnemonics)
    