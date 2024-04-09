from commune.module import Module
from commune.subspace.subspace import Subspace

subspace = Subspace()


class Subnet(Module):

    def emissions(self, netuid = 0, network = "main", block=None, update=True, **kwargs):

        return subspace.query_vector('Emission', network=network, netuid=netuid, block=block, update=update, **kwargs)