import cupy as cp
import numpy


class Layer:
    def __init__(self, inputs, neurons):
        self.weights = cp.random.uniform(low=-1, high=1, size=(inputs, neurons)).astype(numpy.float32)
        self.biases = cp.random.uniform(low=-1, high=1, size=(1, neurons)).astype(numpy.float32)

    def feedforward(self, input):
        return cp.dot(input, self.weights) + self.biases
    
    def ReLu(self, input):
        return cp.maximum(0, input)

    def update(self, input):
        output = self.feedforward(input)
        output = self.ReLu(output)
        return output

