# -*- coding: utf-8 -*-
"""
Created 17 Feb 2016

@author: Abdul Rahim Nizamani
"""

from node import Node

def snd ((x,y)):
    return y

class DelayNode(Node):
    """A delay node activates when its incoming node activated the last moment."""
    def __init__(self,name):
        super(DelayNode, self).__init__(name)
        self.type = "DelayNode"
        self.pendingActivation = False

    def UpdateActivation(self,tick):
    # If this node was already processed, return the current activity
        if(self.tick==tick):
            return self.activated
    # Update the node's activation
        self.activated = self.pendingActivation and Node.network.attention == list(self.incoming)[0]
        incomingNodes = map((lambda x: (x,Node.network.nodes[x].UpdateActivation(tick))) ,self.incoming)
        if(incomingNodes and len(incomingNodes) == 1):
            self.pendingActivation = any(map(snd,incomingNodes)) # \
                                     # and Node.network.attention == list(self.incoming)[0]
            #if self.pendingActivation:
                #print("Delay node " + self.name + " received activation.")
                #print(self.name + " " + str(incomingNodes))
                #print(self.name + " " + str(incomingNodes))
        else: self.pendingActivation = False
    # Update current tick and return the activation
        self.tick = tick
        return self.activated
