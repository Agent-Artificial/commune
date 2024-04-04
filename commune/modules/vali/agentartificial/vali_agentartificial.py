#imports
import commune as c
import json


Vali = c.module('vali')



# Class
class ValiText(Vali):
    def __init__(self, config = None, **kwargs):
        """
        Initialize the class with the provided configuration and keyword arguments.

        Parameters:
            config (dict): The configuration settings for the class. Default is None.
            **kwargs: Additional keyword arguments.

        Returns:
            None
        """
        self.config = self.set_config(config, kwargs=kwargs)
        kwargs['start'] = False
        Vali.__init__(self, config=config, **kwargs)
        self.set_dataset( self.config.dataset )
        self.start()

    def start_dataset(dataset):
        """
        Get the file extension of a given dataset.

        Args:
            dataset (str): The name of the dataset.

        Returns:
            str: The file extension of the dataset.
        """
        dataset.split('.')[-1]
    def set_dataset(self, dataset:str , **kwargs):
        """
        Set the dataset for the object.

        Args:
            dataset (str): The name of the dataset.
            **kwargs: Additional keyword arguments.

        Returns:
            The dataset object.
        """
        if c.server_exists(dataset):
            self.dataset = c.connect(dataset)
        else:
            c.module('data.hf').serve(path=dataset.split('.')[-1])
            self.dataset = c.connect(dataset)
        return self.dataset

    def score_module(self, module='model.openai') -> int:
        """
        A function to score a module based on the provided input prompt.
        
        Args:
            module (str): The module to be scored. Default is 'model.openai'.
        
        Returns:
            dict: A dictionary containing the score information including weight, answer index, answers, output, and sample.
        """
        if isinstance(module, str):
            module = c.connect(module)
        module.info(timeout=1)
        sample = self.sample()
        prompt = f'COMPLETE THE JSON \n {sample} \n' + " GIVE THE ANSWER AS AN INDEX -> {answer_idx:int} ? \n ```json"
        output = module.generate(prompt, max_tokens=256)
        if isinstance(output, str):
            output = '{' + output.split('{')[-1].split('}')[0] + '}'
            c.print(output)
            output = json.loads(output)
        # if correct answer is in the choices
        if 'answer_idx' not in output:
            answer_idx = int(list(output.values())[0])
        else:
            answer_idx = int(output['answer_idx'])
        if answer_idx in answers:
            w = 1
        else:
            w = 0
        return {'w': w, 'answer_idx': answer_idx, 'answers': answers, 'output': output, 'sample': sample}

    def sample(self):
        """
        Generates a sample from the dataset.

        Returns:
            dict: A dictionary containing the sampled question, shuffled choices, and the correct answers.
        """
        # get sample
        sample = self.dataset.sample()
        sample = {
            'question': sample['question'],
            'choices': c.shuffle(sample['incorrect_answers'] + sample['correct_answers']),
            'answers': sample['correct_answers']
        }

        # shuffle choices 
        sample['choices'] = {i: choice for i, choice in enumerate(sample['choices'])}
        sample['answers'] = [i for i, choice in sample['choices'].items() if choice in sample['answers']]

        return sample


    
            

