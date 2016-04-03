"""The apple network:
   Detects the word apple and prints it."""
from network import Network

def printSeven(): return("7")

sensors = {"3","+","4","7"}

# network: detects the word "apple"
network = Network(sensors)

network.AddNode("DelayNode","D1")
network.AddConnection("3","D1")

network.AddNode("AndNode","And1")
network.AddConnection("D1","And1")
network.AddConnection("+","And1")

network.AddNode("DelayNode","D2")
network.AddConnection("And1","D2")

network.AddNode("AndNode","And2")
network.AddConnection("D2","And2")
network.AddConnection("4","And2")

a1 = network.AddNode("ActionNode","A1") # action A1: print 7 (reward = +1)
a1.reward = 1.0

network.expectedRewards[("And2","A1","7")] = 1.0

network.AddNode("MotorNode","M1")
network.AddMotorAction("M1",printSeven)
network.AddConnection("A1","M1")

a3 = network.AddNode("ActionNode","A2") # action A2: do nothing (reward = 0)
a3.reward = 0.0

network.AddDecision("And2","A1")
network.AddDecision("And2","A2")

network.AddPrediction("A1","7",1.0)

network.AddPrediction("A2","And2",0.125)
network.AddPrediction("A2","And1",0.125)
network.AddPrediction("A2","D2",0.125)
network.AddPrediction("A2","D1",0.125)

network.AddPrediction("A2","3",0.125)
network.AddPrediction("A2","+",0.125)
network.AddPrediction("A2","4",0.125)
network.AddPrediction("A2","7",0.125)

