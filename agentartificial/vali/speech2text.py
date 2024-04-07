from commune.vali.vali import Vali
from commune.module.module import Module
import requests
import unittest
module = Module

subspace = module.module('subspace')

class TestSpeech2Text(unittest.TestCase):
    def test(self, result, expected_results):
        """
        This function tests the equality of the result and expected_results using assertAlmostEqual.
        """
        return self.assertAlmostEqual(result, expected_results)
        

class ValiSpeech2Text(Vali):
    def __init__(
        self,
        network="local",
        search="miner",
        netuid=52
        ):
        """
        A constructor method that initializes the class with default parameters for network, search, and netuid.
        """
        super().__init__()
        self.init(locals())
        self.url = "https://vali-speech2text-agentartificial.ngrok.dev/"

    def score_module(self, module_dotpath="agentartificial.speech2text.Speech2Text"):
        """
        Generate the speech data, forward it to the specified module for processing, and test the results.
        
        Parameters:
            module_dotpath (str): The dot path of the module to forward the speech data to.
        
        Returns:
            bool: The result of the test between the processed data and the expected results.
        """
        testdata_response = self.generate_speech()
        testdata = testdata_response.json()["data"]
        if isinstance(module_dotpath, str):
            result = self.forward(testdata["test"], module_dotpath)
        expected_results = testdata["expected_results"]
        return TestSpeech2Text().test(result, expected_results)


    def generate_speech(self):
        """
        This function generates a speech by sending a GET request to the specified URL.
        """
        return requests.get(self.url)

    def get_registry(self):
        """
        A method to retrieve the registry using a GET request to the specified URL.
        """
        return requests.get(self.url)

    def forward(
        self, 
        data, 
        module_dotpath="agentartificial.speech2text.Speech2Text",
        ):
        """
        A function that forwards data to a specified module for processing.
        
        Parameters:
            data: The input data to be forwarded.
            module_dotpath: The dot path of the module to connect to (default is "agentartificial.speech2text.Speech2Text").
        
        Returns:
            The generated output from the specified module.
        """
        mod = module.connect(module_dotpath, network="local", namespace="agentartificial", virtual=False, verbose= False, prefix_match =False, return_future=False)
        return mod.generate("speech2text", data=data)