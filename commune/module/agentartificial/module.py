import requests
import json

from commune.module import Module
from agentartificial.data_models import InferenceGenerator, Models, Endpoints
from requests import Response
from typing import Dict, Any



class agent_module(InferenceGenerator, Module):
    description = "Description of what the module does."
    whitelist = [
        "forward",
        "run_generate"
        ]
    def __init__(
        self, 
        base_url="https://proxy-agentartificial.ngrok.app", 
        model=Models.MISTRAL, 
        prompt=None, 
        data=None, 
        headers={"application"}
        ):
        """
        Initialize the class with the provided base URL, model, prompt, data, and headers.

        :param base_url: The base URL to use, defaults to "https://proxy-agentartificial.ngrok.app"
        :param model: The model to use, defaults to Models.MISTRAL
        :param prompt: The prompt to use
        :param data: The data to use
        :param headers: The headers to use, defaults to {"application"}
        """
        super().__init__(
            base_url=str(base_url),
            model=model,
            prompt=prompt,
            data=data,
            headers=headers
            )

    def run_generate(self, endpoint: Endpoints=Endpoints.SPEECH2TEXT, ):
        """
        Generate a POST request to the given endpoint with the constructed URL, body, and headers, then parse and return the response.
        Parameters:
            endpoint: Endpoints - the endpoint for the request
        Returns:
            parsed response
        """
        response = requests.post(
            url=self.construct_url(),
            data=self.construct_body(),
            headers=self.construct_headers()
            )
        return self.parse_response(response)

    def construct_body(self, data=None, filename=None) -> Dict[str, Any]:
        """
        A function that constructs the body of something using the provided data and filename.

        Parameters:
            data (Any, optional): The data to be used in constructing the body. Defaults to None.
            filename (Any, optional): The filename to be used. Defaults to None.

        Returns:
            Dict[str, Any]: A dictionary containing the constructed body with 'data' and 'audio_filename' keys.
        """
        return {
            "data": data,
            "filename": filename
        }

    def construct_headers(self) -> Dict[str, str]:
        """
        Constructs and returns the headers dictionary.
        Returns:
            Dict[str, str]: The headers dictionary.
        """
        self.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.api_key}"
            }        
        return self.headers

    def construct_url(self) -> str:
        """
        A method to construct the URL using the base URL and a specific endpoint.
        Returns:
            str: The constructed URL as a string.
        """
        self.url = self.base_url + str(Endpoints.AGENT_MODULE)
        return self.url
        
    def parse_response(self, response: Response) -> Any:    
        """
        Parse the response data and return it as a JSON object.
        
        Args:
            response (Response): The response object to be parsed.
        
        Returns:
            Any: The parsed JSON object from the response.
        """
        return json.loads(response.text) if response.text else response.json()