from pydantic import BaseModel
from typing import List, Dict, Optional, Union, Any
from pathlib import Path
from rich.console import Console
from dotenv import load_dotenv
from abc import ABC, abstractmethod

load_dotenv()

class CRUD(ABC):
    @abstractmethod
    def __init__(self):
        pass
    @abstractmethod
    async def list(self):
        pass
    @abstractmethod
    def get(self):
        pass
    @abstractmethod
    def create(self):
        pass
    @abstractmethod
    def update(self):
        pass
    @abstractmethod
    def delete(self):
        pass


path = Path(__file__).parent.resolve()

class CommuneConfig(BaseModel):
    cost: int
    description: str
    base_module: str
    encrypted_prefix: str
    git_url: str
    homepath: Union[str, Path]
    root_module_class: str
    default_port_range: List[int]
    default_ip: str
    address: str
    root_path: Union[str, Path]
    libpath: Union[str, Path]
    datapath: Union[str, Path]
    modules_path: Union[str, Path]
    repo_path: Union[str, Path]
    library_name: str
    pwd: Optional[str]
    console: Console
    helper_functions: List[str]
    whitelist: List[str]
    blacklist: List[str]
    server_mode: str
    default_network: str
    cache: Dict[Any, Any]
    home: Union[str, Path]
    __ss58_format__: int