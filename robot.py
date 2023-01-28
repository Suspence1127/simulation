from motor import MOTOR
from sensor import SENSOR
import pybullet as p
import pyrosim.pyrosim as pyrosim
import pybullet_data
import constants as c
from pyrosim.neuralNetwork import NEURAL_NETWORK
import os

class ROBOT:
    def __init__(self, solutionID):
        self.solutionID = solutionID
        self.motor = dict()
        self.sensors = dict()
        self.robotId = p.loadURDF("body.urdf", [0, 0, 0.1])
        self.nn = NEURAL_NETWORK("brain" + str(solutionID) + ".nndf")
        os.system("del brain" + str(solutionID) + ".nndf")
        pyrosim.Prepare_To_Simulate(self.robotId)
        self.Prepare_To_Sense()
        self.Prepare_To_Act()
        pass

    def Prepare_To_Sense(self):
        for linkName in pyrosim.linkNamesToIndices:
            self.sensors[linkName] = SENSOR(linkName)
        pass

    def Sense(self, x):
        for linkName in pyrosim.linkNamesToIndices:
            self.sensors[linkName].Get_Value(x)
        pass

    def Prepare_To_Act(self):
        for jointName in pyrosim.jointNamesToIndices:
            self.motor[jointName] = MOTOR(jointName)
        pass

    def Act(self, x):
        for neuronName in self.nn.Get_Neuron_Names():
            if self.nn.Is_Motor_Neuron(neuronName):
                jointName = self.nn.Get_Motor_Neurons_Joint(neuronName)
                desiredAngle = self.nn.Get_Value_Of(neuronName)
                self.motor[jointName].Set_Value(self.robotId, desiredAngle)
        pass

    def Think(self):
        self.nn.Update()
        pass

    def Get_Fitness(self):
        stateOfLinkZero = p.getLinkState(self.robotId,0)
        positionOfLinkZero = stateOfLinkZero[0]
        xCordinateOfLinkZero = positionOfLinkZero[0]
        f = open("tmp" + str(self.solutionID) + ".txt", "w")
        f.write(str(xCordinateOfLinkZero))
        f.close()
        os.rename("tmp"+str(self.solutionID)+".txt" , "fitness"+str(self.solutionID)+".txt")
        pass
