# -*- coding: utf-8 -*-
"""
Created 17 Feb 2016

@author: Abdul Rahim Nizamani

Todo:
Rule selection

Demonstration:
Decision edges
MDP and deciding actions
Update Q function from received rewards
Abstraction nodes
"""

import numpy as np
import mdptoolbox
import mdptoolbox.example

from network import *

#from Apple import network
#from AppleEnv import AppleEnv

#

#from Addition import network
#from AdditionEnv import AdditionEnv


#env = AppleEnv(network)
#env.Begin(20000)

#print("Total Reward:   " + str(network.totalReward))
#print("Total Examples: " + str(env.examples))
#print("Total Score:    " + str(env.score))
#if env.examples != 0:
#    print("Percent correct:" + str(env.score / float(env.examples) * 100.0))

#print(env.network.workingMemory)


#for a in range(0,len(env.network.vi.Q)):
#    print(env.network.states[a] + ": \t" + str(env.network.vi.Q[a]))



sensors = {"0","1","2","3","4","5","6","7","8","9","+","*"}

network = Network(sensors)

abs1 = network.AddNode("AbstractionNode","Abs1")
abs1.pattern = ["x","*","0"]

abs2 = network.AddNode("AbstractionNode","Abs2")
abs2.pattern = ["x","+","y"]

abs3 = network.AddNode("AbstractionNode","Abs3")
abs3.pattern = ["x","+","0"]

network.AddNode("ActionNode","A1") # action A1: print 0
network.AddConnection("Abs1","A1")
network.AddNode("ActionNode","A2") # action A2: print y+x
network.AddConnection("Abs2","A2")
network.AddNode("ActionNode","A3") # action A2: print y+x
network.AddConnection("Abs3","A3")

network.AddNode("MotorNode","M1")
network.AddConnection("A1","M1")

network.AddNode("MotorNode","M2")
network.AddConnection("A2","M2")

network.AddNode("MotorNode","M3")
network.AddConnection("A3","M3")

def printZero():
    node = network.nodes["Abs1"]
    bd = node.binding
    wm = node.wm
    wm2 = list(reversed(Node.network.workingMemory[0:len(node.pattern)]))
    if bd.has_key("x") and wm == wm2[0:len(wm)]:
        for i in range(0,len(wm)): network.workingMemory.pop(0)
        network.workingMemory.insert(0,"0")
        print(network.workingMemory)
def printYX():
    node = network.nodes["Abs2"]
    bd = node.binding
    wm = node.wm
    wm2 = list(reversed(Node.network.workingMemory[0:len(node.pattern)]))
    if bd.has_key("x") and bd.has_key("y") and wm == wm2[0:len(wm)]:
        for i in range(0,len(wm)): network.workingMemory.pop(0)
        network.workingMemory.insert(0,bd["y"])
        network.workingMemory.insert(0,"+")
        network.workingMemory.insert(0,bd["x"])
        print(network.workingMemory)

def printX0():
    node = network.nodes["Abs3"]
    bd = node.binding
    wm = node.wm
    wm2 = list(reversed(Node.network.workingMemory[0:len(node.pattern)]))
    if bd.has_key("x") and wm == wm2[0:len(wm)]:
        for i in range(0,len(wm)): network.workingMemory.pop(0)
        network.workingMemory.insert(0,bd["x"])
        print(network.workingMemory)

network.AddMotorAction("M1",printZero)
network.AddMotorAction("M2",printYX)
network.AddMotorAction("M3",printX0)

network.Tick({"3"})
network.Tick({"1"})

network.Tick({"8"})
network.Tick({"+"})
network.Tick({"0"})
network.Tick(set())
