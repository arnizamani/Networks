# -*- coding: utf-8 -*-
"""
Created 17 Feb 2016

@author: Abdul Rahim Nizamani
"""

from node import Node

class OrNode(Node):
    """An Or node activates whenever any of its incoming nodes is active."""
    def __init__(self,name):
        super(OrNode, self).__init__(name)
        self.type = "OrNode"

#    def Activate(self,income=[]):
#        self.activated  = any(income)
        #print("Node " + self.name + ": " + str(self.activated))

    def UpdateActivation(self,tick):
    # If this node was already processed, return the current activity
        if(self.tick==tick):
            return self.activated
    # Update the node's activation
        incomingNodes = list(map((lambda x: Node.network.nodes[x].UpdateActivation()) ,self.incoming))
        if(incomingNodes and len(incomingNodes) > 1):
            self.activated  = any(incomingNodes)
            if self.activated:
                print("Node " + self.name + " activated.")
        else:
            self.activated = False
    # Update current tick and return the activation
        self.tick = tick
        return self.activated
