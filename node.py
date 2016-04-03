# -*- coding: utf-8 -*-
"""
Created 17 Feb 2016

@author: Abdul Rahim Nizamani
"""

#from enum import Enum, unique

#@unique
#class NodeType(Enum):
#    """Enumeration listing the types of nodes"""
    #BasicNode  = 1
    #SensorNode = 2
    #ActionNode = 3
    #MotorNode  = 4
    #AndNode    = 5
    #OrNode     = 6
    #NotNode    = 7
    #AbstractionNode = 8
#    DelayNode  = 9

class Node(object):
    """Base class for a node in the transparent network.
       Other classes extend this class for specific node types."""
    def __init__(self,name=""):
        self.type = "BasicNode"
        self.name = name
        self.incoming = set()
        self.outgoing = set()
        self.actions = set() # set of possible actions (decision edges)
        self.activated = False
        self.network = None
        self.tick = 0

    def UpdateActivation(self,tick):
    # If this node was already processed, return the current activity
    # Update the node's activation
    # Update current tick and return the activation
        self.tick = tick
        return self.activated

    def DeActivate(self):
        self.activated = False
