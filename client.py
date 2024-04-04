from typing import Optional, Any
import commune as c
from commune.subspace.subspace import Subspace
from manager.key_objects import CommuneKey, KeyRingManager
from commune.module import Module
from loguru import logger

class CommuneClient:
    def __init__(self):
        self.c = c
        self.module = Module()
        self.subspace = Subspace()
        self.km = KeyRingManager()
        self.key = CommuneKey
        self.keynames = [key for key in self.km.key2ss58addresses.keys()]

    def getbalance(
        self, 
        key_name: Optional[str] = None,
        ss58key: Optional[str] = None,
        ):
        if not ss58key and not key_name:
            logger.warning("No key name or ss58key provided")
            return None
        if not ss58key:
            ss58key = self.km.keyring[key_name].ss58_address # type: ignore
        return self.subspace.get_balance(ss58key)
        
    def get_all_balances(self):
        for name in self.keynames:
            if str(name).startswith("5"):
                balance = self.getbalance(name)
                print(name, balance)
            else:
                key = self.km.keyring[name].ss58_address
                balance = self.getbalance(name, key)
                print(name, balance)
        return True
        

    def get_key(self, keyname: str):
        return self.km.keyring[keyname]

    def balance_transfer(self, amount, to_key, from_key, network=None, nonce=None):
        self.subspace.transfer(amount=amount, dest=to_key, key=from_key, network=network, nonce=nonce)

    def get_stake(self, keyname: str):
        return self.subspace.get_stake(keyname)

    def get_all_stake(self):
        for name, address in self.km.key2ss58addresses.items():
            stake = self.get_stake(address)
            print(name, stake)

if __name__ == "__main__":
    client = CommuneClient()
    keynames = client.km.keynames
    keyname = keynames[1]
#
    address = client.km.key2ss58addresses[keyname]
#
    #balance = client.subspace.get_balance(address)
    #stake = client.get_stake(address)
    print("Balances")
    client.get_all_balances()
    print("Stake")
    client.get_all_stake()

    
    