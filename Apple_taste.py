"""The apple taste and hearing network:
   Detects the apple taste and hearing."""

from network import Network

def printApple(): print("apple")

sensors = {"Sw_High","So_Low","Bi_Low","ae","p","l"}

network = Network(sensors)

network.AddNode("AndNode","And1")
network.AddConnection("So_Low","And1")
network.AddConnection("Bi_Low","And1")

network.AddNode("AndNode","And2")
network.AddConnection("Sw_High","And2")
network.AddConnection("And1",   "And2")

network.AddNode("DelayNode","D1")
network.AddConnection("ae","D1")

network.AddNode("AndNode","And3")
network.AddConnection("D1","And3")
network.AddConnection("p", "And3")

network.AddNode("DelayNode","D2")
network.AddConnection("And3","D2")

network.AddNode("AndNode", "And4")
network.AddConnection("D2","And4")
network.AddConnection("l", "And4")

network.AddNode("AndNode", "And5")
network.AddConnection("And2","And5")
network.AddConnection("And4", "And5")

network.AddNode("ActionNode","Action1")
network.AddConnection("And5", "Action1")

network.AddNode("MotorNode","Motor1")
network.AddConnection("Action1","Motor1")

network.AddMotorAction("Motor1",printApple)

network.Tick({"ae"})
network.Tick(set())
network.Tick(set())
network.Tick({"p"})
network.Tick(set())
network.Tick(set())
network.Tick({"Sw_High","So_Low","Bi_Low","l"})
