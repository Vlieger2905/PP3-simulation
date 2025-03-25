import cupy as cp
import numpy
from .Layer import Layer

# Input data is the length of the sensory lines
# Output data: [full left, left, center, right, full right]
# There are 

class Brain:
    def __init__(self,amount_of_sensory_lines):
        self.layers = []
        # Saves the data of the layers
        self.layerdata = []
        # The sensory lines is the input data for the neural network
        self.inputSize = amount_of_sensory_lines
        # Options to controll the car
        self.output_options= ["full_left", "left", "center", "right", "full_right"]
        self.outputSize = len(self.output_options)
        self.neuronLayer =[self.inputSize,32,64,32,self.outputSize]
        # Creating the hidden layers:
        for i in range(0,len(self.neuronLayer)-1):
            self.layers.append(Layer(self.neuronLayer[i],self.neuronLayer[i+1]))
        

    def thinking(self, input):
        current_input = cp.array(input)
        for layer in self.layers:
            current_input = layer.update(current_input)
        # Get the index with the highest value
        index = int(cp.argmax(current_input))
        # Get the corresponding output option
        output = self.output_options[index]
        return output

# # Test the brain
# brain = Brain(32)
# brain.thinking(cp.random.rand(32))




