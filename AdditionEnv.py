# -*- coding: utf-8 -*-
"""
Created 17 Feb 2016

@author: Abdul Rahim Nizamani
"""

from network import Network
import random

class AdditionEnv(object):
    """Environment feeds activation to the sensors in the network"""
    def __init__(self,network):
        print("Initializing Environment...")
        self.network = network
        self.sensors = network.sensors
        self.history = [] # history of activated sensors
        self.score = 0      # total correct answers
        self.examples = 0   # total examples

    def Begin(self,count=0):
        """Start feeding activation to the sensors. Activate a single sensor randomly."""
        if(not self.sensors): raise SyntaxError
        if(count<=0): count=1000
        reward = 0.0
        active = random.choice(sorted(list(self.sensors)))
        while(count>0):
            result = filter(lambda x:x!="",self.network.result)
            self.network.Tick({active},reward)
            reward = 0.0
            if not self.history:
                reward = 0.0
            else:
                if list(reversed(self.history))[0:3] == list(reversed(["3","+","4"])):
                    self.examples += 1
                #print(list(reversed(self.history))[0])
                if(result==["7"]):
                    if list(reversed(self.history))[0:3] == list(reversed(["3","+","4"])):
                        reward = 100.0
                        self.score += 1
                    else: reward = -10.0
                else:
                    if list(reversed(self.history))[0:3] == list(reversed(["3","+","4"])):
                        reward = -100.0
                    else: reward = 0.0
            if result==["7"] and list(reversed(self.history))[0:3] == list(reversed(["3","+","4"])):
                active = "7"
            else:
                #active = random.choice(sorted(list(self.sensors)))
                active = random.choice(["3","+","4"])
            count -= 1
            self.history.append(active)
