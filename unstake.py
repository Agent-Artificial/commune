import argparse
import commune as c

# Set up command-line argument parsing
parser = argparse.ArgumentParser(
    description="Transfer all balance to a specific address."
)
parser.add_argument("--address", type=str, help="The address to transfer to.")
parser.add_argument(
    "--netuid", type=int, default=0, help="The network to use. Default is 0."
)
parser.add_argument(
    "--min", type=float, default=2.5, help="Min stake amount to left. Default is 1."
)

# Parse command-line arguments
args = parser.parse_args()
if not args.address:
    raise ValueError("Please specify the address to transfer to.")
netuid = args.netuid
wallet_addresses = c.keys()
[print(address) for address in wallet_addresses]

for address in wallet_addresses:
    if address in args.address:
        continue
    try:
        # Unstake all balance from the wallet
        staked = c.get_stake(address, update=True, netuid=netuid)
        print(f"Staked amount is {staked}")
        if staked > args.min:
            c.unstake(key=address, netuid=netuid, amount=staked - args.min)

        # Transfer all balance to the specific address
        balance = c.get_balance(address)
        print(f"Total balance is {balance}")

        if balance > args.min:
            c.transfer(args.address, balance - 2.5, address)

    except Exception as e:
        # Code that will run if the exception is raised
        print(f"An error occurred: {e}, Address: {address}")
