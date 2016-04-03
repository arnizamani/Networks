# -*- coding: utf-8 -*-
"""
Created 17 Feb 2016

@author: Abdul Rahim Nizamani
"""

from node import Node

class SensorNode(Node):
    """A sensor node receives activation from external environment."""
    def __init__(self,name):
        super(SensorNode, self).__init__(name)
        self.type = "SensorNode"

    def UpdateActivation(self,tick):
    # If this node was already processed, return the current activation
        if(self.tick==tick):
            return self.activated
    # Update the node's activation
        self.activated = (self.name in Node.network.activeSensors)
    # Update current tick and return the activation
        self.tick = tick
        return self.activated
