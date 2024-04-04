from pydantic import BaseModel
from typing import List, Dict, Optional, Union, Any, Literal, Callable, IO, Mapping
from pathlib import Path
from rich.console import Console
from rich.theme import Theme
from rich.style import StyleType
from rich.emoji import EmojiVariant
from dotenv import load_dotenv
from datetime import datetime
from abc import ABC, abstractmethod

load_dotenv()

FormatTimeCallable = Callable[[Union[int, float]], str]

class ConsoleSchema(BaseModel):
    class Config:
        arbitrary_types_allowed = True
    color_system: Optional[Literal["auto", "standard", "256", "truecolor", "windows"]]
    force_terminal: Optional[bool]
    force_jupyter: Optional[bool]
    force_interactive: Optional[bool]
    soft_wrap: bool
    theme: Optional[Theme]
    stderr: bool
    file: Optional[IO[bytearray]]
    quiet: bool
    width: Optional[int]
    height: Optional[int]
    style: Optional[StyleType]
    no_color: Optional[bool]
    tab_size: int
    record: bool
    markup: bool
    emoji: bool
    emoji_variant: Optional[EmojiVariant]
    highlight: bool
    log_time: bool
    log_path: bool
    log_time_format: Union[str, FormatTimeCallable]
    highlighter: Optional[str]
    legacy_windows: Optional[bool]
    safe_box: bool
    get_datetime: Optional[Callable[[], datetime]]
    get_time: Optional[Callable[[], float]]
    _environ: Optional[Mapping[str, str]]

class CommuneConsole(Console):   
    class Config:
        arbitrary_types_allowed = True     
    @classmethod
    def __get_pydantic_core_schema__(cls):
        return ConsoleSchema
        

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
    class Config:
        arbitrary_types_allowed = True
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