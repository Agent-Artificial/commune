from commune.model.agent.artificial import Artificial
from commune.subspace.subspace import Subspace
from pydantic import BaseModel
from pathlib import Path
import json
import yaml

subspace = Subspace()
import pbd

pbd.trace()


class LaunchConfig(BaseModel):
    module: str
    tag: str
    network: str
    port: int
    server_name: str
    refresh: bool
    wait_for_server: bool
    remote: bool
    tag_seperator: str
    max_workers: int
    public: bool
    key: str

def get_name(config: LaunchConfig, launch_number: int):
    config.tag = str(launch_number)
    config.module = f"""{config.module.replace(
        '{i}',str(launch_number)
        )}{config.tag_seperator}{config.tag}"""
    config.key = config.module
    config.server_name = config.module
    return config

def launch(config: LaunchConfig):
    result = subspace.serve(**config.model_dump())
    subspace.print(json.dumps(result))

def get_port(config: LaunchConfig, fleet_size: int):
    for i in range(fleet_size):
        if i == 0:
            return config
        else:
            config.port += i * 5
        config = get_name(config, i)
        launch(config)
        
def launch_module(module_string: str, fleet_size: int = 1):
    module_path = Path(
        f"commune/{module_string.replace('.py', '.yml')}"
    )
    yaml_config = yaml.safe_load(
        module_path.read_text(encoding='utf-8')
        )
    return get_port(
        LaunchConfig(**yaml_config), 
        fleet_size=fleet_size
    )
    
if __name__ == '__main__':
    module_string = "model/agent/artificial.py"
    fleet_size = 1
    
    