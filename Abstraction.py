# -*- coding: utf-8 -*-
"""
Created 16 Mar 2016

@author: Abdul Rahim Nizamani
"""

from node import Node

class Abstraction(Node):
    """An abstraction node represents a variable and takes any value from the WM."""
    def __init__(self,name,incoming=None,motors=None):
        super(Abstraction, self).__init__(name)
        self.type = "AbstractionNode"
        self.incoming = incoming
        self.pattern = [] # For example, pattern = ["x","+","y"]
        self.vars = ["x","y","z"]
        self.binding = {}
        self.wm = []

    def UpdateActivation(self,tick):
    # If this node was already processed, return the current activity
        if(self.tick==tick):
            return self.activated
    # Update the node's activation
        self.activated = self.Match()
    # Update current tick and return the activation
        self.tick = tick
        return self.activated

    def Match(self):
        self.binding.clear()
        if not self.pattern or not Node.network.workingMemory: return False
        l = len(self.pattern)
        wm = list(reversed(Node.network.workingMemory[0:l]))
        if l != len(wm): return False
        z = zip (self.pattern,wm)
        matched = all(map(lambda (x,y):x in self.vars or x==y,z))
        if not matched: return False
        matching = filter(lambda (x,y):x in self.vars,z)
        if matching == []: return False
        isunique = True
        binding = []
        uniqueVars = {}
        for (x,y) in matching:
            if x in uniqueVars.keys():
                isunique = y == uniqueVars[x]
            else:
                uniqueVars[x] = y
                binding.append((x,y))
        if not isunique: return False
        if binding == []: return False
        self.binding.update({x : y for (x,y) in binding})
        self.wm = wm
        return True
