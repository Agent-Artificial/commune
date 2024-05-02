import os
import json
import requests
from pathlib import Path
from typing import Generator, Any, List, Dict, Tuple
from substrateinterface import SubstrateInterface, Keypair
from eth_hash.auto import keccak
from dotenv import load_dotenv
from commune.subspace.subspace import Subspace

load_dotenv()

subspace = Subspace()
find_key = "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48"


def read_pathfile(folder: str):
    folderpath = Path(folder).expanduser().resolve()
    keypaths = folderpath.iterdir()
    for keypath in keypaths:
        with keypath.open() as f:
            yield json.load(f)["data"]


keys = read_pathfile("")


def check_key(keys: Generator[Any, Any, None]):
    staketos = []
    stakefroms = []
    staketo_balance = 0
    stakefrom_balance = 0
    key_map = {}

    for i, key in enumerate(keys):
        if "key2address" in key:
            continue
        if "ss58_address" not in key:
            continue
        print(key)
        key = json.loads(key)
        name = key["path"]
        address = key["ss58_address"]
        mnemonic = key["mnemonic"]
        seed = key["seed_hex"]
        public_key = key["public_key"]
        balance = subspace.get_balance(public_key)
        staketo: List[Tuple[str, float]] = subspace.get_staketo(address)
        stakefrom: List[Tuple[str, float]] = subspace.get_stakefrom(address)
        bittensor = check_bittensor_key(address)
        if len(staketo) >= 1 or len(stakefrom) >= 1 or balance >= 1:
            staketo_balance_list = [stake for stake in staketos]
            stakefrom_balance_list = [stake for stake in stakefroms]
            staketo_balance = sum(staketo_balance_list)
            stakefrom_balance = sum(stakefrom_balance_list)
            print(
                f"""
Name:          {name}
Address:       {address}
Balance:       {balance}
Stake To:      {staketo}
Stake From:    {stakefrom}
Balance found: {balance + staketo_balance + stakefrom_balance}
"""
            )
            if bittensor:
                print(f"Bittensor:     {bittensor}")
            h160_address = ss58_to_h160(seed)
            if find_key in h160_address:
                print(f"key found: {name} | {address}")
                return True
            key_map[f"{i}"] = {
                "name": name,
                "key": {
                    "h160_address": h160_address,
                    "address": address,
                    "mnemonic": mnemonic,
                    "balance": balance,
                    "staketo": staketo,
                    "stakefrom": stakefrom,
                    "bittensor": bittensor,
                },
            }
    save_path = Path(f"key_map.json")
    save_path.write_text(json.dumps(key_map))
    return save_path


def ss58_to_h160(seed):
    # Decode the SS58 address
    keypair = Keypair.create_from_seed(seed_hex=seed, crypto_type=1, ss58_format=42)

    # Extract the public key
    public_key = keypair.public_key

    # Hash the public key using Keccak-256
    keccak_hash = keccak.hasher(public_key)

    # Get the last 20 bytes for the H160 address
    h160_address = "0x" + keccak_hash[-20:].hex()

    return h160_address


def main(folder):
    keys = read_pathfile(folder)
    savepath = check_key(keys)
    print(savepath)


if __name__ == "__main__":
    # print(check_bittensor_key("86ff742ed74b091f88915857ebdc74da88e6bef031c12d8085cd86cd8efe8263"))
    # folder = "~/.commune/key"
    folder = input("Enter path to keys: ")
    main(folder)
