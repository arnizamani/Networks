# -*- coding: utf-8 -*-
"""
Created 17 Feb 2016

@author: Abdul Rahim Nizamani
"""

from node import Node

def snd ((x,y)):
    return y

class AndNode(Node):
    """An And node activates whenever all of its incoming nodes are active."""
    def __init__(self,name):
        super(AndNode, self).__init__(name)
        self.type = "AndNode"

    def UpdateActivation(self,tick):
    # If this node was already processed, return the current activity
        if(self.tick==tick):
            return self.activated
    # Update the node's activation
        incomingNodes = map((lambda x: (x,Node.network.nodes[x].UpdateActivation(tick))) ,self.incoming)
        if(incomingNodes and len(incomingNodes) > 1):
            self.activated  = all(map(snd,incomingNodes))
        else:
            self.activated = False
    # Update current tick and return the activation
        self.tick = tick
        return self.activated
