# -*- coding: utf-8 -*-
"""
Created 17 Feb 2016

@author: Abdul Rahim Nizamani
"""

from node import Node

class NotNode(Node):
    """An And node activates whenever all of its incoming nodes are active."""
    def __init__(self,name):
        super(NotNode, self).__init__(name)
        self.type = "NotNode"

    def UpdateActivation(self,tick):
    # If this node was already processed, return the current activity
        if(self.tick==tick):
            return self.activated
    # Update the node's activation
        if(not self.incoming): raise LookupError
        if(len(self.incoming) is not 1): raise OverflowError
        # create a reference to the set of nodes in the network
        self.activated = not Node.network.nodes[list(self.incoming)[0]].UpdateActivation(tick)
    # Update current tick and return the activation
        self.tick = tick
        return self.activated
