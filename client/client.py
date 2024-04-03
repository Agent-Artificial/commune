import os
import asyncio
import commune as c
from commune.module import Module
from data_models import CRUD
from config import default_config



        

class CommuneCRUD(CRUD):
    def __init__(self):
        self.commune = c.Config(
            **default_config.model_dump()
        )
        self.module = Module()
        self.keys_hidden_path = "/home/bakobi/.commune/key/"
        self.keys = os.listdir(self.keys_hidden_path)
    def list_balances(self):
        balances = []
        for key in self.keys:
            if key.startswith("key2"):
                continue
            key = key.split(".")[0]
            name = self.module.address2name(key)
            balances.append({"name": name, "balance": self.module.balance(key)})
        return balances
            
    def list(self):
        return self.keys
        
    def get(self):
        return self.commune
    def create(self):
        return self.commune
    def update(self):
        return self.commune
    def delete(self):
        return self.commune

def main():
    client = CommuneCRUD()

    balances = client.list_balances()
    print([balances])

if __name__ =="__main__":
   main()