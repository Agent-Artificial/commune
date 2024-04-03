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
        self.keynames = [key for key in self.km.keyring.keys()]

    def getbalance(
        self, 
        key_name: Optional[str] = None,
        ss58key: Optional[str] = None,
        ):
        for keyname in self.keynames:
            if key_name:
                ss58key = self.km.keyring[keyname].ss58_address
            if not ss58key:
                raise ValueError("ss58key is required")
            key = self.km.keyring[keyname]
            if ss58key == key.ss58_address:
                return {"keyname": keyname, "balance":self.subspace.get_balance(
                    key=ss58key)}
            else:
                continue
        return {"keyname": ss58key, "balance": "key not found"}

    def getbalances(self):
        balances = {}
        for name in self.keynames:
            key = self.km.keyring[name].ss58_address
            balances[name] = self.getbalance(key)

        return balances

    def get_key(self, keyname: str):
        return self.km.keyring[keyname]

    def balance_transfer(self, to_key, from_key):
        return self.module.transfer

async def main():
    bow = CommuneClient()
    return bow.getbalances()
        

if __name__ == "__main__":
    bow = CommuneClient()
    keynames = [key for key in bow.km.keyring.keys()]
    key = bow.km.keyring[keynames[0]]
    balance = bow.getbalance(ss58key=key.ss58_address)
    print(balance)