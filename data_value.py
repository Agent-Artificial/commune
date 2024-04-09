from client import CommuneClient
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
import pandas as pd
import uvicorn
import subprocess
import json
import io

VERSION='v1'

save_file = 'stats.xlsx'

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = CommuneClient()

@app.get(f'/{VERSION}/stats' + '/{netuid}')
def get_module_stats(netuid: str):
    """
    Get module data for a specific network ID.

    Args:
        netuid (str): The network ID for which mining data is requested.

    Returns:
        Response: A response containing the mining data in CSV format.
    """
    raw_data = client.subspace.stats(netuid=int(netuid), update=True)
    df = pd.DataFrame(raw_data)
    csv_data = df.to_csv(index=False)
    print(csv_data)
    return Response(content=csv_data, media_type='text/csv')


@app.get(f'/{VERSION}/balance' + '/{netuid}')
def get_balances(netuid: str):
    balances = []
    all_balances = client.get_all_balances(netuid=int(netuid))
    stakedtos = client.get_all_stake_to(netuid=int(netuid))
    stakedfroms = client.get_all_staked_from(netuid=int(netuid))
    for i, _ in enumerate(all_balances):
        print(all_balances[i])
        try:
            all_balances[i].append(stakedfroms[i])
            all_balances[i].append(stakedtos[i])
            balances.append(all_balances[i])
        except Exception as e:
            print(e)
    df = pd.DataFrame(balances)
    csv_data = df.to_csv(index=False)
    print(csv_data)
    return Response(content=csv_data, media_type='text/csv')


if __name__ == "__main__":
    uvicorn.run("data_value:app", host="0.0.0.0", port=7092, reload=True)