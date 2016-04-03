# -*- coding: utf-8 -*-
"""
Created 17 Feb 2016

@author: Abdul Rahim Nizamani
"""

from node import Node

class ActionNode(Node):
    """An action node propagates activation to a set of motors/actuators."""
    def __init__(self,name,incoming=None,motors=None):
        super(ActionNode, self).__init__(name)
        self.type = "ActionNode"
        self.incoming = incoming
        self.predictions = {} # prediction edges with probabilities

    def UpdateActivation(self,tick):
    # If this node was already processed, return the current activity
        if(self.tick==tick):
            return self.activated
    # Update the node's activation
        if(self.incoming and len(self.incoming) > 0):
            incomingNodesAct = map((lambda x: Node.network.nodes[x].UpdateActivation(tick)) ,self.incoming)
            self.activated  = any(incomingNodesAct)
            #if self.activated: print("Node " + self.name + " activated.")
        else:
            self.activated = False
    # Update current tick and return the activation
        self.tick = tick
        return self.activated

    def Activate(self):
        """Activate the action node manually, based on MDP."""
        self.activated = True
        for i in range(0,len(self.outgoing)):
            Node.network.nodes[list(self.outgoing)[i]].Activate()
