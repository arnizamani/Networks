# -*- coding: utf-8 -*-
"""
Created 17 Feb 2016

@author: Abdul Rahim Nizamani
"""

from network import Network
import random

class AppleEnv(object):
    """Apple environment feeds activation to the sensors in the Apple network"""
    def __init__(self,network):
        print("Initializing Environment...")
        self.network = network
        self.sensors = network.sensors
        self.history = []   # history of activated sensors
        self.score = 0      # total correct answers
        self.examples = 0   # total examples

    def Begin(self,count=0):
        """Start feeding activation to the sensors. Activate a single sensor randomly."""
        if(not self.sensors): raise SyntaxError
        if(count<=0): count=1000
        reward = 0.0
        while(count>0):
            active = random.choice(sorted(list(self.sensors)))
            self.network.Tick({active},reward)
            self.history.append(active)
            reward = 0.0
            result = filter(lambda x:x!="",self.network.result)
            if self.history is None:
                reward = 0.0
            else:
                if(result==["apple"]):
                    if list(reversed(self.history))[0:3] == list(reversed(["a","p","p","l","e"])):
                        reward = 100.0
                        self.score += 1
                    else: reward = -10.0
                else: reward = 0.0
                count -= 1
