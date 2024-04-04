from pathlib import Path
from rich.console import Console
from data_models import CommuneConfig
from dotenv import load_dotenv
import os

path = Path(__file__).parent.resolve()

default_config = CommuneConfig(
    cost=1,
    description="description of the module",
    base_module="module",
    encrypted_prefix="ENCRYPTED",
    git_url="https://github.com/commune-ai/commune.git",
    homepath=Path("/home/bakobi/commune/"),
    root_module_class="c",
    default_port_range=[50050, 50149],
    default_ip="0.0.0.0",
    address="0.0.0.0:8888",
    root_path=path,
    libpath=path / "data",
    datapath=path / "data",
    modules_path=path / "modules",
    repo_path=path,
    library_name="commune",
    pwd=os.getenv("PWD"),
    console=Console(),
    helper_functions=[
        'info',
        'schema',
        'server_name',
        'is_admin',
        'namespace',
        'code',
        'whitelist', 
        'blacklist',
        'fns'
        ],
    whitelist=[],
    blacklist=[],
    server_mode="http",
    default_network="local",
    cache={},
    home=Path("~/"),
    __ss58_format__=42,
)