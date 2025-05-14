import cupy as cp
import numpy
from .Layer import Layer
import Setting as S

# Input data is the length of the sensory lines
# Output data: [full left, left, center, right, full right]
# There are 

class Brain:
    def __init__(self,amount_of_sensory_lines, Genes=None):
        self.layers = []
        # The sensory lines is the input data for the neural network
        self.inputSize = amount_of_sensory_lines
        # Options to controll the car
        self.output_options= ["full_left", "left", "center", "right", "full_right"]
        self.outputSize = len(self.output_options)
        self.neuronLayer = [self.inputSize] + [layer for layer in S.hidden_layers] + [self.outputSize] 
        # Creating the hidden layers:
        # When there are inherited genes
        if Genes:
            self.ChildConstruction(self.neuronsLayer, Genes)
        
        # When it is created randomly
        else:
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

    # Constructing the brain according to a given gene input
    def ChildConstruction(self,neuronsLayer,genes):
        index = 0
        for layer in genes:
            new_layer = Layer(neuronsLayer[index], neuronsLayer[index+1])
            for gene in layer:
                weights = cp.array(gene["weights"])
                print(index, weights.__len__())
                biases = cp.array(gene["biases"])
                new_layer.weights = weights
                new_layer.biases = biases
            self.layers.append(new_layer)
            index+=1
    
    # Function to save all the layer data of the brain.
    def SavingSperm(self):
        layerdata = []
        for layer in self.layers:
                # First convert cupy array to numpy array
                weights = cp.asnumpy(layer.weights)
                bias = cp.asnumpy(layer.biases)
                genes = [{
                    "weights": layer.weights.tolist(),
                    "biases": layer.biases.tolist()
                }]
                layerdata.append(genes)
 
        return layerdata