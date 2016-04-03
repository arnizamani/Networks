# -*- coding: utf-8 -*-
"""
Created 17 Feb 2016

@author: Abdul Rahim Nizamani
"""

import numpy as np
import mdptoolbox
import random
from node import Node
from sensor import SensorNode
from action import ActionNode
from motor import MotorNode
from andnode import AndNode
from ornode import OrNode
from notnode import NotNode
from delay import DelayNode
from Abstraction import Abstraction

class Network(object):
    """A transparent network with a fixed set of sensors"""

    def __init__(self,sensors):
        print("Initializing Network...")
        self.time = 0
        self.nodes = {}    # a dictionary: node name : node
        self.edges = set() # a set of edges: (node name, node name)
        self.autoUpdate = False # if enabled, the network will grow automatically from sensory activation
        self.sensors = sensors
        self.attention = None
        self.activeSensors = set()
        self.result = [] # output of the network at each iteration
        self.totalReward = 0.0
        self.learningRate = 0.5
        self.discountFactor = 0.5 # 1.0 does not work
        self.lastAction = None # remember the last action
        self.lastState  = None # remember the last state (activated node)
        self.expectedRewards = {} # (state,action,state) = reward
        self.workingMemory = []
        Node.network = self

        for sensor in sensors:
            if sensor not in self.nodes.keys():
                self.nodes[sensor] = SensorNode(sensor)
                print("Sensor Node " + sensor + " created.")

    def AddNode(self,type,name,act=None):
        """Add a new node in the network"""
        if name in self.nodes.keys():
            raise SystemExit("Network.AddNode: node " + name + " already in network.")
        elif type is "SensorNode":
            raise SystemExit("Network.CreateNode: cannot create new sensors.")
        elif type is "ActionNode":
            self.nodes[name] = ActionNode(name)
        elif type is "MotorNode":
            self.nodes[name] = MotorNode(name,act)
        elif type is "AndNode":
            self.nodes[name] = AndNode(name)
        elif type is "OrNode":
            self.nodes[name] = OrNode(name)
        elif type is "NotNode":
            self.nodes[name] = NotNode(name)
        elif type is "DelayNode":
            self.nodes[name] = DelayNode(name)
        elif type is "AbstractionNode":
            self.nodes[name] = Abstraction(name)
        else:
            self.nodes[name] = Node(name)
        print(str(type) + ": node " + name + " created.")
        return self.nodes[name]

    def AddMotorAction(self,motor,action):
        if motor in self.nodes.keys():
            self.nodes[motor].AddAction(action)

    def AddConnection(self,inNode,outNode):
        if inNode in self.nodes.keys() and outNode in self.nodes.keys():
            if self.nodes[inNode].outgoing is None:
                self.nodes[inNode].outgoing = {outNode}
            else:
                self.nodes[inNode].outgoing.add(outNode)
            if self.nodes[outNode].incoming is None:
                self.nodes[outNode].incoming = {inNode}
            else:
                self.nodes[outNode].incoming.add(inNode)
        else:
            print("Connection not added between " + inNode + " and " + outNode + ".")

    def AddDecision(self,inNode,outNode):
        if inNode in self.nodes.keys() and outNode in self.nodes.keys():
            self.nodes[inNode].actions.add(outNode)
        else:
            print("Decision edge not added from " + inNode + " to " + outNode + ".")

    def AddPrediction(self,inNode,outNode,probability):
        if self.nodes.has_key(inNode) and self.nodes.has_key(outNode) and self.nodes[inNode].type is "ActionNode":
            self.nodes[inNode].predictions[outNode] = probability
        else: raise LookupError

    def CreateDecisionMdp(self):
        """Create an MDP from the decision edges"""
        print("Creating MDP")
        self.states = {}
        self.actions = {}
        self.rewards = []
        stateNodes = map(lambda x:x.name,\
                         filter(lambda x: x.type not in ["ActionNode","MotorNode"],self.nodes.values()) )
        actionNodes = map(lambda x:x.name,\
                         filter(lambda x: x.type is "ActionNode",self.nodes.values()))
        self.states = sorted(list(stateNodes))
        self.actions = sorted(list(actionNodes))
        if(len(self.states) < 2 or len(self.actions) < 1):
            print("Error: States and actions must be non-empty")

    # Transition probabilities
        self.P = []
        self.hasPredictions = False
        for n in range(0,len(self.actions)):
            actionNode = self.nodes[self.actions[n]]
            b = []
            for state1 in range(0,len(self.states)):
                a = []
                for state2 in range(0,len(self.states)):
                    if(actionNode.predictions.has_key(self.states[state2])):
                        a.append(actionNode.predictions[self.states[state2]])
                        hasPredictions = True
                    else: a.append(0.0)
                b.append(a)
            self.P.append(b)
    # Rewards matrix
        self.R = []
        for i in (range(0,len(self.actions))):
            b = []
            for j in (range(0,len(self.states))):
                a = []
                for k in (range(0,len(self.states))):
                    key = (self.states[j],self.actions[i],self.states[k])
                    if self.expectedRewards.has_key(key):
                        a.append(self.expectedRewards[key])
                    else: a.append(0.0)
                b.append(a)
            self.R.append(b)

        if self.hasPredictions:
            print("Number of states:  " + str(len(self.states)))
            print("Number of actions: " + str(len(self.actions)))
            print(np.array(self.R))
            self.vi = mdptoolbox.mdp.QLearning(np.array(self.P), np.array(self.R), self.discountFactor)
            self.vi.run()
        else:
            print("MDP not created. No prediction values available.")

    def Tick(self,activeSensors,reward=0.0):
        """Move the network to next time step: given set of active sensors"""
        if(self.time is 0): self.CreateDecisionMdp()
        self.time += 1
        self.totalReward += reward
        #print("   TIME STEP: " + str(self.time))
        self.activeSensors = activeSensors
    # Deactivate all nodes
        self.result = []
        for n in self.nodes.values():
            n.DeActivate()
    # Activate the node with attention
        if(self.attention is not None and self.nodes.has_key(self.attention)):
            self.nodes[self.attention].activated = True
            self.nodes[self.attention].tick = self.time
    # Propagate the activity through the network
        activeNodes = set()
        for n in self.nodes.values():
            active = n.UpdateActivation(self.time)
            if(active): activeNodes.add(n.name)
    # Find top active nodes
        topActive = []
        for n in activeNodes:
            out = map(lambda x:self.nodes[x].activated,self.nodes[n].outgoing)
            #out = self.nodes[n].outgoing
            if(self.nodes[n].type not in ["MotorNode","DelayNode","ActionNode"]\
               and not any(out)):
               topActive.append(n)
    # move the attention to one of the top active nodes
        self.MoveAttention(topActive)

    # update the Q-vector
        if self.lastAction != None and self.lastState != None:
            maxAction = max(list(self.vi.Q[self.states.index(self.attention)]))
            st = self.states.index(self.lastState)
            at = self.actions.index(self.lastAction)
            self.vi.Q[st][at] = self.vi.Q[st][at] +\
                         self.learningRate * (reward + (self.discountFactor * maxAction) - self.vi.Q[st][at])
    # take the action (transition to the next state)
        if(self.attention is not None and self.attention != "" and self.hasPredictions):
            self.ChooseAction()

            #maxAction = max(list(self.vi.Q[self.states[self.attention]]))
            #for st in range(0,len(self.vi.Q)):
            #    for at in range(0,len(self.vi.Q[st])):
            #        self.vi.Q[st][at] = self.vi.Q[st][at] +\
            #                self.learningRate * (reward + (self.discountFactor * maxAction) - self.vi.Q[st][at])


    def RemoveFromList(self,list1,element1):
        if not list1: return list1
        if element1 in list1:
            list1.remove(element1)
            return list1
        return list1

    def MoveAttention(self,topActive):
        if(topActive):
            #self.attention = topActive[0]
            active = self.RemoveFromList(topActive,self.attention)
            if(active):
                self.attention = active[0] # random.choice(topActive)
                self.workingMemory = [self.attention] + self.workingMemory[0:3]
                print(self.workingMemory)

    def ChooseAction(self):
        """The top active (attented) node chooses an action based on rewards."""
        self.lastAction = None
        self.lastState = None
        if(self.attention is None or self.attention == ""): return
    # find best action for the currently attended node
        actions = list(self.vi.Q[self.states.index(self.attention)])
        actionIndex = actions.index(max(actions))
        actionName = self.actions[actionIndex]
    # execute the best action for the currently attended node
        self.nodes[actionName].Activate()
        self.lastAction = actionName
        self.lastState = self.attention

    def CreateMdp(self):
        """Create an MDP from all the nodes"""
        self.states = {"":0}
        self.actions = {}
        self.rewards = []
        stateNodes = filter(lambda x: x.type not in ["ActionNode","MotorNode"],self.nodes.values())
        actionNodes = filter(lambda x: x.type is "ActionNode",self.nodes.values())
        for i in (range(1,len(stateNodes)+1)):
            self.states[stateNodes[i-1].name] = i
        for i in (range(0,len(actionNodes))):
            self.actions[i] = actionNodes[i].name
        if(len(self.states) < 2 or len(self.actions) < 1):
            print("Error: States and actions must be non-empty")
    # Transition probabilities: equal probabilities
        self.P = []
        for i in (range(0,len(self.actions))):
            b = []
            for j in (range(0,len(self.states))):
                a = []
                for k in (range(0,len(self.states))):
                    a.append(1.0/len(self.states))
                b.append(a)
            self.P.append(b)

    # Rewards
        self.R = []
        for i in (range(0,len(self.actions))):
            b = []
            for j in (range(0,len(self.states))):
                a = []
                for k in (range(0,len(self.states))):
                    a.append(actionNodes[i].reward)
                b.append(a)
            self.R.append(b)

        print("Number of states:  " + str(len(self.states)))
        print("Number of actions: " + str(len(self.actions)))
        self.vi = mdptoolbox.mdp.QLearning(np.array(self.P), np.array(self.R), 0.5)
        self.vi.run()
        print(self.vi.Q)
