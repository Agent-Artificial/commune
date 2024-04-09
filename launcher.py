from client import CommuneClient
from pydantic import BaseModel
from typing import Any
import json


client = CommuneClient()


def update_subnet():
    client.update_subnet(
        ImmunityPeriod=100, 
        MinAllowedWeights=128, 
        MaxAllowedWeights=18446744073709551615,
        MaxAllowedUids=500,
        MinStake=1000,
        Founder="5F4c6WjExFshz3QQ4U6xtEXqUyPFV2P66Z5ZBQpvSyCFnuHE",
        FounderShare=20,
        IncentiveRatio=50,
        TrustRatio=10,
        VoteThresholdSubnet=1,
        VoteModeSubnet="authority",
        MaxWeightAge=18446744073709551615,
        SubnetNames="agentartificial",
        MaxStake=18446744073709551615,
        Tempo=100,
        key="agentartificial"
    )

def unstake(
    module='5F4c6WjExFshz3QQ4U6xtEXqUyPFV2P66Z5ZBQpvSyCFnuHE', 
    amount=500, 
    key='vali::project_management', 

    ):
    client.subspace.unstake(
        module,
        amount,
        key
    )

def balance_transfer():
    client.balance_transfer(
        500,
        '5F4c6WjExFshz3QQ4U6xtEXqUyPFV2P66Z5ZBQpvSyCFnuHE'
    )


class RegistrationConfig:
    def __init__(
        self,
        name: str,
        address: str,
        stake: int,
        subnet: str,
        key: str,
        module_key: str,
        network: str,
        wait_for_inclusion: Any,
        wait_for_finalization: Any,
        ):
        self.name=name
        self.address=address
        self.stake=stake
        self.subnet=subnet
        self.key=key
        self.module_key=module_key
        self.network=network
        self.wait_for_inclusion=wait_for_inclusion
        self.wait_for_finalization=wait_for_finalization

    def json(self):
        return {
            "name": self.name,
            "address": self.address,
            "stake": self.stake,
            "subnet": self.subnet,
            "key": self.key,
            "module_key": self.module_key,
            "network": self.network,
            "wait_for_inclusion": self.wait_for_inclusion,
            "wait_for_finalization": self.wait_for_finalization
        }
    
# client.subspace.serve(
    # # module="agentartificial::subnet",
    # tag="agentartificial::subnet",
    # network="local",
# )


subnet_config = RegistrationConfig(
    name="agentartificial::subnet",
    address="5FjBk4E6srWB8AecW2vNGCS7azhzBahxRn8ZuV6U1rzp2RUt",
    stake=277,
    subnet="agentartificial",
    key="agentartificial::subnet",
    module_key="module",
    network="main",
    wait_for_inclusion=True,
    wait_for_finalization=True
)

# client.subspace.serve(
    # module="agentartificial.vali::vali",
    # tag="agentartificial.vali::vali",
    # network="local",
#)
vali_config = RegistrationConfig(
    name="agentartificial.vali::vali",
    address="5CJ7pux7fuwafX3QQTsYBp66aadz5mjiQSVxbDyKP6VzhrpE",
    stake=5200,
    subnet="agentartificial",
    key="agentartificial.vali::vali",
    module_key="module",
    network="main",
    wait_for_inclusion=True,
    wait_for_finalization=True
)

# client.subspace.serve(
    # module="agentartificial.module::module",
    # tag="agentartificial.module::module",
    # network="local",
# )
module_config = RegistrationConfig(
    name="agentartificial.module::module",
    address="5HNKeskmc2zK4pHJGj98hmrzgpKdYu23enVaVwvofAwbidpF",
    stake=300,
    subnet="agentartificial",
    key="agentartificial.module::module",
    module_key="module",
    network="main",
    wait_for_inclusion=True,
    wait_for_finalization=True
)

def register(
    name,
    address,
    stake,
    subnet,
    key,
    module_key,
    network,
    wait_for_inclusion,
    wait_for_finalization
    ):
    client.register_module(
        keyname=name,
        address=address,
        stake=stake,
        subnet=subnet,
        key=key,
        module_key=module_key,
        network=network,
        wait_for_inclusion=wait_for_inclusion,
        wait_for_finalization=wait_for_finalization
    )

#register(**vali_config.json())
#register(**module_config.json())
#register(**subnet_config.json())


def regfleet(
    tagname="agentartificial::fitzgerald", 
    stake=300,
    subnet='agentartificial',
    address="5HVoPviTiQ8haEL6XCyCzM5vANHT361EWU6wgCfnqYdSSAMT",
    module_key="module",
    network='main',
    wait_for_inclusion=True,
    wait_for_finalization=True
    ):

    for i in range(1):
        output = client.subspace.serve(
            module=module_key,
            tag=tagname,
            network=network,
            )

        # Getting the address
        address_full = output['address']

        # Splitting the address into IP and port
        ip_address, port = address_full.split(':')

        # Printing the results
        print(f"Serving on:\nIP Address: {ip_address}, Port: {port}")

        register(
            name=f"{tagname}::module{i}",
            address=address_full,
            stake=stake,
            subnet=subnet,
            key=module_key,
            module_key=address,
            network=network,
            wait_for_inclusion=wait_for_inclusion,
            wait_for_finalization=wait_for_finalization
        )


def serve(
    modulekey="eden", 
    tagname="agentartificial.eden", 
    network="main"
    ):
    for _ in range(10):
        output = client.subspace.serve(
            module=modulekey,
            tag=tagname,
            network=network,
            )


def launch(
    tagname="agentartificial::fitzgerald", 
    stake=300,
    subnet='agentartificial',
    address="",
    module_key="module",
    network='main',
    wait_for_inclusion=True,
    wait_for_finalization=True,
    name="module"
):
    output = client.subspace.serve(
    module=module_key,
    tag=tagname,
    network=network,
    name=name
    )

    # Getting the address
    address_full = output['address']
    
    # Splitting the address into IP and port
    ip_address, port = address_full.split(':')
    
    # Printing the results
    print(f"Serving on:\nIP Address: {ip_address}, Port: {port}")
    
    register(
        name=f"{tagname}::{name}",
        address=address_full,
        stake=stake,
        subnet=subnet,
        key=module_key,
        module_key=address,
        network=network,
        wait_for_inclusion=wait_for_inclusion,
        wait_for_finalization=wait_for_finalization
    )

launch()