from client import CommuneClient



def bowser():
    message = ''
    bowser = "5E6vrnMmcaB7ErhQJpnFqTqihohejafr9RFHA5Nxr8swnx4R"

    client = CommuneClient()

    keyname = "vali::project_management"
    key = client.km.key2ss58addresses[keyname]

    message.join(f'{key}\n')

    staketo = client.subspace.get_staketo(key)[key]
    message.join(f"Stake:  {staketo}\n")
    if staketo < 277:
        raise ValueError(f"Stake too low: {staketo}\nNeed at least 277")
    message.join(f"{client.subspace.unstake(amount=staketo - 277, dest=key, key=key, network='main')}\n")
    balance = client.getbalance(keyname, netuid=0)
    message.join(f"Total Balance: {balance}\n")
    split = float(balance) / 2
    message.join(f"Balance: {balance} / 2")
    message.join(f"= {split}")
    message.join(f"{client.subspace.transfer(amount=split - 2.5, dest=bowser, key=keyname)}")

    return message