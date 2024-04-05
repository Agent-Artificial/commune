import requests
import base64
import json
import os
from requests import Response
from pathlib import Path
from pydantic import BaseModel, Field
from typing import Dict, List, Union, Optional, Any
from enum import Enum
from abc import ABC, abstractmethod


class Endpoints(Enum):
    TEXT_GENERATION="/text_generation"
    TEXT2SPEECH="/text2speech"
    TEXT2IMAGE="/text2image"
    TEXT2VIDEO="/text2video"
    SPEECH2TEXT="/speech2text"
    IMAGE2VIDEO="/image2video"
    EMBEDDINGS="/embeddings"

class Models(Enum):
    MIXTRAL='ollama/mixtral'
    MISTRAL='ollama/mistral'
    LLAVA="ollama/llava"
    BAKLLAVA="ollama/bakllava"
    CODE_LLAMA2="ollama/code-llama2"
    GEMA="ollama/gena"
    GROK="ollama/grok"
    MAMBA="ollama/mamba"

class Generator(BaseModel):
    base_url: str = Field(default="https://proxy-agentartificial.ngrok.app")
    model: Optional[Models] = Field(default=Models.MISTRAL)
    prompt: Optional[str] = Field(default="")
    data: Optional[str] = Field(default="")
    headers: Dict[str, str] = Field(default={"application json": "application/json"})

class InferenceGenerator(Generator, ABC):
    def __init__(
        self, 
        base_url,
        model, 
        prompt, 
        data, 
        headers
        ):
        self.base_url = base_url
        self.model = model
        self.prompt = prompt
        self.data = data
        self.headers = headers

    def class_config(self):
        self.__arb

    @abstractmethod
    def generate(self) -> Response:
        """Sends a request to generate inference"""

    @abstractmethod
    def construct_body(self) -> Dict[str, Any]:
        """Constructs the body of the request"""

    @abstractmethod
    def construct_headers(self) -> Dict[str, str]:
        """Constructs the headers of the request"""

    @abstractmethod
    def construct_url(self) -> str:
        """Constructs the url of the request"""
        
    @abstractmethod
    def parse_response(self, response: Response) -> Any:    
        """Parses the response"""

    def to_base64(self, data) -> str:
        return base64.b64encode(data.encode()).decode()

    def from_base64(self, data) -> str:
        return base64.b64decode(data).decode()

        