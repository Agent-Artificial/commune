from typing import Optional, Any
import commune as c
from commune.subspace.subspace import Subspace
from manager.key_objects import CommuneKey, KeyRingManager
from commune.module import Module

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
        address = None
        
        if not key_name:
            address = ss58key
            
        if key_name:
            if key_name.startswith("5"):
                address = key_name
            else:
                key = self.km.keyring[key_name]
                address = key.ss58_address
                
        if ss58key:
            address = ss58key
            
        if not address:
            raise ValueError("address is required")

        if address in self.km.key2ss58addresses.values():
            return {"keyname": ss58key, "balance":self.subspace.get_balance(
                key=address)}
        else:
            return {"keyname": ss58key, "balance":"Error: Key Not Found"}

    def getbalances(self):
        balances = {}
        for name in self.keynames:
            key = self.km.keyring[name].ss58_address
            balances[name] = self.getbalance(key)

        return balances

    def get_key(self, keyname: str):
        return self.km.keyring[keyname]

    def balance_transfer(self, amount, to_key, from_key, network=None, nonce=None):
        self.subspace.transfer(amount=amount, dest=to_key, key=from_key, network=network, nonce=nonce)

if __name__ == "__main__":
    client = CommuneClient()
    keynames = client.km.keynames
    keyname = keynames[1]
    address = client.km.key2ss58addresses[keyname]
    balance = client.subspace.get_balance(address)
    print(balance)
    