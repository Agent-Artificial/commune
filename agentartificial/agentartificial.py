import commune as c
from commune.subspace.subspace import Subspace
class Agentartificial(c.Module):
    def __init__(self):
        super().__init__()
        self.registry = {}
        self.subspace = Subspace()

    def get_registry_entry(self, name):
        if name not in self.registry:
            with open("registry.json", "r", encoding="utf-8") as f:
                self.registry = json.loads(f.read())
        return self.registry[name]

    def register(self, module, url, body, headers):
        if entry := self.get_registry_entry(module["name"]):
            return self.registry[entry["name"]]
        result = requests.post(url, json=body, headers=headers)
        self.registry[module["name"]] = module
        self.registry[module["name"]]["sample_result"] = result.json()

        with open("registry.json", "a", encoding="utf-8") as f:
            f.write(json.dumps(module) + "\n")

        return self.registry[module["name"]]
            
    def call(self, name, **kwargs):
        registry_entry = self.get_registry_entry(name)
        return registry_entry["command"](**kwargs)

    def vote(self, weights, netuid=52):
        uids = []
        for _, module in self.registry.items():
            uids.extend(iter(module["uids"]))
        self.subspace.vote(
            uids=uids,
            weights=weights,
            netuid=netuid,
            key="keyname",
            network="main",
            update=True
        )