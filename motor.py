# -*- coding: utf-8 -*-
"""
Created 17 Feb 2016

@author: Abdul Rahim Nizamani
"""

from node import Node

class MotorNode(Node):
    """A motor node performs some action in the external environment."""
    def __init__(self,name,action=None):
        super(MotorNode, self).__init__(name)
        self.type = "MotorNode"
        self.action = action

    def AddAction(self,action):
        self.action = action

    def UpdateActivation(self,tick):
    # If this node was already processed, return the current activity
        if(self.tick==tick):
            return self.activated
    # Update the node's activation
        incomingNodes = map((lambda x: Node.network.nodes[x].UpdateActivation(tick)) ,self.incoming)
        if(incomingNodes and len(incomingNodes) > 0):
            self.activated  = any(incomingNodes)
            #if self.activated: print("Node " + self.name + " activated.")
        else:
            self.activated = False
        if self.action is not None and self.activated:
            output = self.action()
            if(Node.network.result is not None):
                Node.network.result.append(output)
            else:Node.network.result = [output]
    # Update current tick and return the activation
        self.tick = tick
        return self.activated

    def Activate(self):
        """Activate the motor manually, from an action node that was activated by the MDP."""
        self.activated = True
        if self.action is not None and self.activated:
            output = self.action()
        if(Node.network.result is not None):
            Node.network.result.append(output)
        else:Node.network.result = [output]