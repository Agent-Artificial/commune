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
    async def list(self):
        for key in self.keys:
            key = key.split(".")[0]
            print(key)
            await self.module.stats(key)

        
    def get(self):
        return self.commune
    def create(self):
        return self.commune
    def update(self):
        return self.commune
    def delete(self):
        return self.commune

async def main():
    client = CommuneCRUD()

    await client.list()

if __name__ =="__main__":
    asyncio.run(main())