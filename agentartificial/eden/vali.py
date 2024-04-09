from vali.vali import Vali
from commune.module.module import Module
from agentartificial.AgentArtificial import AgentArtificial
from fastapi.responses import JSONResponse
import requests
import unittest
import json
module = Module

subspace = module.module('subspace')

class TestSpeech2Text(unittest.TestCase):
    def test(self, result, expected_results):
        """
        This function tests the equality of the result and expected_results using assertAlmostEqual.
        """
        return self.assertAlmostEqual(result, expected_results)
        

class Vali(Vali):
    def __init__(
        self,
        netuid=52,
        inference_url="https://proxy-agentartificial.ngrok.app",
        api_key="sk-1234"
        ):
        """
        A constructor method that initializes the class with default parameters for network, search, and netuid.
        """
        super().__init__()
        self.init(locals())
        self.url = inference_url
        self.api_key = api_key
        self.netuid = netuid
        self.current_network = self.network()
        self.agent = AgentArtificial()
        
    def score_module(self, module_dotpath="agentartificial.speech2text.Speech2Text", url="https://proxy-agentartificial.ngrok.app", body=None, headers=None):
        if headers is None:
            headers = {
                "application": "application/json",
                "Authorization": "Bearer sk-1234",
            }
        name = module_dotpath.split(".")[-1]
        testdata_response = self.run_generate(url, body, headers)
        expected_results = self.agent.registry[name]["expected_results"]
        return TestSpeech2Text().test(testdata_response, expected_results)

    def run_generate(
        self,
        url,
        body,
        headers
        ):
        try:
            response = requests.post(
                url=url, 
                json=body, 
                headers=headers, 
                timeout=5
            )
            if response.status_code == 200:
                return JSONResponse(
                    content=response.json(), 
                    status_code=response.status_code
                    )
        except Exception as e:
            return e
        return requests.get(self.url)

    def forward(
        self, 
        key: str,
        module_name: str,
        address="",
        network="main",
        namespace="agentartificial",
        virtual=False,
        verbose=True,
        prefix_match=True,
        return_future=False
        mode="http",
        ):
        mod = module.connect(
            network=network,
            namespace=namespace, 
            virtual=virtual,
            verbose=verbose, 
            prefix_match=prefix_match, 
            return_future=return_future,
            key=address,
            module=module.module(module_name)
            )
        full_result = {}
        for result in self.agent.execute(mod, key=key):
            full_result.update(result)
        return full_result
            