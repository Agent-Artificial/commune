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
        balances = []
        for name in self.keynames:
            if str(name).startswith("5"):
                balance = self.getbalance(name)
                print(name, balance)
            else:
                key = self.km.keyring[name].ss58_address
                balances.append(self.getbalance(name, key))
        return balances
        

    def get_key(self, keyname: str):
        return self.km.keyring[keyname]

    def balance_transfer(self, amount, to_key, from_key, network=None, nonce=None):
        self.subspace.transfer(amount=amount, dest=to_key, key=from_key, network=network, nonce=nonce)

    def get_stake_to(self, keyname: Optional[str]="", address: str="", netuid:Optional[int]=0):
        stake = self.subspace.get_stake_to(address, keyname, netuid or 0)
        return stake

    def get_all_stake_to(self, netuid=0):
        stakes = []
        for name, address in self.km.key2ss58addresses.items():
            stakes.append(
                self.get_stake_to(
                    name,
                    address,
                    netuid=netuid
                    )
                )
            return stakes

    def get_staked_from(self, keyname: Optional[str]="", address: str="", netuid:Optional[int]=0):
        stake = self.subspace.get_stake_from(address, keyname, None, netuid=0)
        return stake

    def get_all_staked_from(self, netuid=0):
        stakes = []
        for name, address in self.km.key2ss58addresses.items():
            stakes.append(self.get_staked_from(
                name,
                address,
                netuid=netuid
                ))
        return stakes

    def check_input_list(
        self, 
        address_list, 
        netuid=0,
        network='main'
        ):
        if isinstance(address_list, list):
            lines = address_list
        else:
            with open(address_list, "r", encoding="utf-8") as f:
                lines = f.readlines()
        addresses = []
        addy_list = []
        stake2list = []
        for key, address in self.km.key2ss58addresses.items():
            addresses.append(f"{key}: {address}\n")
            addy_list.append(address)
            stake2list.append(self.get_stake_to(key, address, netuid=netuid))
        address = "".join(addresses)
        balances = self.get_all_balances()
        stakefrom = self.get_all_staked_from()
        

        for i, address in enumerate(addresses):
            print(f"Key: {self.km.keynames[i]}")
            print(f"Address: {address}")
            print(f"Balance: {balances[i]}")
            print(f"Stake from: {stakefrom[i]}")
            print(f"stake to: {stake2list[i]}")
            print(f"-----------")
            
    def register_module(
        self, keyname: str, 
        address: str, 
        stake: int=277, 
        subnet: str="commune", 
        key: str="keyname",
        module_key: str="module", 
        network="main", 
        wait_for_inclusion: bool=True, 
        wait_for_finalization: bool=True
        ):
        print(f"""
name: {keyname} 
address: {address} 
stake: {stake} 
subnet: {subnet} 
key: {key} 
keyname: {keyname} 
network: {network} 
wait_for_inclusion: {wait_for_inclusion} 
wait_for_finalization: {wait_for_finalization} 
""")
        answer = input("Confirm your configuration? (y/n)")
        if answer not in ["y", "Y"]:
            print("Aborting registration")
            return
        
        response = self.subspace.register(
            name=keyname,
            address=address,
            stake=stake,
            subnet=subnet,
            key=key,
            keyname=module_key,
            network=network,
            wait_for_inclusion=wait_for_inclusion,
            wait_for_finalization=wait_for_finalization
            )
        print(response)

    def update_subnet(
        self,
        Tempo=100,
        ImmunityPeriod=100,
        MinAllowedWeights=1,
        MaxAllowedWeights=18446744073709551615,
        MaxAllowedUids=4096,
        MinStake=1,
        Founder="5F4c6WjExFshz3QQ4U6xtEXqUyPFV2P66Z5ZBQpvSyCFnuHE",
        FounderShare=20,
        IncentiveRatio=50,
        TrustRatio=10,
        VoteThresholdSubnet=1,
        VoteModeSubnet="authority",
        MaxWeightAge=18446744073709551615,
        SubnetNames="agentartificial",
        MaxStake=18446744073709551615,
    ):

        return self.subspace.update_subnet(
            netuid=52, 
            key="key", 
            params={
                'tempo': Tempo,
                'immunity_period': ImmunityPeriod,
                'min_allowed_weights': MinAllowedWeights,
                'max_allowed_weights': MaxAllowedWeights,
                'max_allowed_uids': MaxAllowedUids,
                'min_stake': MinStake,
                'founder': Founder,
                'founder_share': FounderShare,
                'incentive_ratio': IncentiveRatio,
                'trust_ratio': TrustRatio,
                'vote_threshold': VoteThresholdSubnet,
                'vote_mode': VoteModeSubnet,
                'max_weight_age': MaxWeightAge,
                'name': SubnetNames,
                'max_stake': MaxStake
            }
        )

    def vote(self, netuid, network, update, module_uids, voting_key):
        keyname = self.km.keynames[5]
        print(keyname)
        address = self.km.key2ss58addresses[keyname]
        print(address)
        weights = self.subspace.weights(
            netuid=netuid, 
            network=network, 
            update=update
        )
        result = self.subspace.vote(
            uids=[uid for uid in module_uids],
            weights=weights,
            netuid=netuid,
            key=voting_key,
            network=network
        )
        return result

if __name__ == "__main__":
    client = CommuneClient()
    client.subspace.cachefn("clear")
    # addresses = client.km.key2ss58addresses
    # for name, address in addresses.items():
        # print(name)
        # print(client.check_input_list([address]))
    # 
    #client.subspace.create_key(
    #    key="agentartificial::speech2text"
    #)

#    keys = client.km.keynames
#    print(keys)
#    addresses = client.km.key2ss58addresses 


#    print(addresses)
    
    #print(client.register_module(
    #   keyname = 'agentartificial::vali_speech2text',
    #   stake=300,
    #   subnet="agentartificial",
    #   key="module",
    #   address=client.km.key2ss58addresses['agentartificial::vali_speech2text'],
    #   module_key="5F4c6WjExFshz3QQ4U6xtEXqUyPFV2P66Z5ZBQpvSyCFnuHE",
    #   wait_for_finalization=True,
    #   wait_for_inclusion=True,
    #   network="main"
    #))
#
#    print(client.subspace.serve(module="agentartificial.speech2text.Speech2Text", port=4197, host= "199.126.197.240", max_workers=2))