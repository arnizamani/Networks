"""The apple network:
   Detects the word apple and prints it."""
from network import Network

def printApple(): return("apple")

def printElppa(): return("elppa")

def printApl(): return("apl")

def printA(): return("a")

sensors = {"a","p","l","e"}

# network: detects the word "apple"
network = Network(sensors)

network.AddNode("DelayNode","D1")
network.AddConnection("a","D1")

network.AddNode("AndNode","And1")
network.AddConnection("D1","And1")
network.AddConnection("p","And1")

network.AddNode("DelayNode","D2")
network.AddConnection("And1","D2")

network.AddNode("AndNode","And2")
network.AddConnection("D2","And2")
network.AddConnection("p","And2")

network.AddNode("DelayNode","D3")
network.AddConnection("And2","D3")

network.AddNode("AndNode","And3")
network.AddConnection("D3","And3")
network.AddConnection("l","And3")

network.AddNode("DelayNode","D4")
network.AddConnection("And3","D4")

network.AddNode("AndNode","And4")
network.AddConnection("D4","And4")
network.AddConnection("e","And4")

a1 = network.AddNode("ActionNode","A1") # action A1: print apple (reward = +1)
a1.reward = 100.0

#a2 = network.AddNode("ActionNode","A2") # action A2: print apple in reverse (reward = -1)
#a2.reward = -1.0

network.AddNode("MotorNode","M1")
network.AddMotorAction("M1",printApple)
network.AddConnection("A1","M1")

network.AddNode("MotorNode","M2")
network.AddMotorAction("M2",printElppa)
network.AddConnection("A2","M2")

a3 = network.AddNode("ActionNode","A3") # action A3: do nothing (reward = 0)
a3.reward = 0.0

network.AddDecision("And4","A1")
network.AddDecision("And4","A2")
network.AddDecision("And4","A3")

network.AddPrediction("A1","And4",0.0009765625)
network.AddPrediction("A1","And3",0.00390625)
network.AddPrediction("A1","And2",0.015625)
network.AddPrediction("A1","And1",0.0625) # 0.0830078125
network.AddPrediction("A1","a",0.229248046875)
network.AddPrediction("A1","p",0.229248046875)
network.AddPrediction("A1","l",0.229248046875)
network.AddPrediction("A1","e",0.229248046875)

#network.AddPrediction("A2","And4",0.0009765625)
#network.AddPrediction("A2","And3",0.00390625)
#network.AddPrediction("A2","And2",0.015625)
#network.AddPrediction("A2","And1",0.0625) # 0.0830078125
#network.AddPrediction("A2","a",0.229248046875)
#network.AddPrediction("A2","p",0.229248046875)
#network.AddPrediction("A2","l",0.229248046875)
#network.AddPrediction("A2","e",0.229248046875)

network.AddPrediction("A3","And4",0.0009765625)
network.AddPrediction("A3","And3",0.00390625)
network.AddPrediction("A3","And2",0.015625)
network.AddPrediction("A3","And1",0.0625) # 0.0830078125
network.AddPrediction("A3","a",0.229248046875)
network.AddPrediction("A3","p",0.229248046875)
network.AddPrediction("A3","l",0.229248046875)
network.AddPrediction("A3","e",0.229248046875)

"""
# Network: prints apl whenever sensor a,p,l are activated in order.
network = Network(sensors)

network.AddNode("DelayNode","D1")
network.AddConnection("a","D1")

network.AddNode("AndNode","And1")
network.AddConnection("D1","And1")
network.AddConnection("p","And1")

network.AddNode("DelayNode","D2")
network.AddConnection("And1","D2")

network.AddNode("AndNode","And2")
network.AddConnection("D2","And2")
network.AddConnection("l","And2")

network.AddNode("ActionNode","A1")
network.AddConnection("And2","A1")

network.AddNode("MotorNode","M1")
network.AddMotorAction("M1",printApl)
network.AddConnection("A1","M1")

#network.tick(set())

#network.tick({"c","m","p","a"})

#network.tick({"p","l","a"})

network.tick({"a"})
#network.tick(set())
#network.tick(set())
#network.tick(set())
network.tick({"p"})
#network.tick(set())
network.tick({"l"})
"""

"""
# Network 0: prints "apl" whenever all three sensors a,p,l are active together.
network0 = Network(sensors)

network0.AddNode(NodeType.AndNode,"And1")
network0.AddConnection("a","And1")
network0.AddConnection("p","And1")

network0.AddNode(NodeType.AndNode,"And2")
network0.AddConnection("And1","And2")
network0.AddConnection("l","And2")

network0.AddNode(NodeType.ActionNode,"A1")

network0.AddConnection("And2","A1")

network0.AddNode(NodeType.MotorNode,"M1")
network0.AddMotorAction("M1",printApl)
network0.AddConnection("A1","M1")

network0.tick(set())

network0.tick({"c","m","p","a"})

network0.tick({"p","m","l","a"})
"""

# Network 1: prints a whenever sensor a is active, nothing otherwise
"""
network1 = Network(sensors)

network1.AddNode(NodeType.ActionNode,"A1")

network1.AddNode(NodeType.MotorNode,"M1")
network1.AddMotorAction("M1",printA)

network1.AddConnection("a","A1")
network1.AddConnection("A1","M1")

network1.tick({"c","m","l","a"})

network1.tick({"l"})

network1.tick({"a"})
"""
