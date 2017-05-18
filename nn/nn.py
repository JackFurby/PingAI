import numpy as np
import scipy.special
import random

class NeuralNetwork(object):
	def __init__(self, weights):
		self.weights = [np.matrix(weighting) for weighting in weights]
	
	def calculate_output_layer(self, input_layer):
		layer_values = np.matrix([input_layer])
		for layer_weights in self.weights:
			layer_values = layer_values * layer_weights
			layer_values = scipy.special.expit(layer_values)
		return layer_values
	
	def mutate(self, factor):
		mutation = np.vectorize(lambda x: x * random.uniform(1 - factor, 1 + factor))
		self.weights = [mutation(layer_weights) for layer_weights in self.weights]

def random_weights(topology, weight_range):
	weights = []
	for num_in, num_out in zip(topology[:-1], topology[1:]):
		layer_weights = [[random.uniform(-weight_range, weight_range) for x in range(num_out)] for y in range(num_in)]
		weights.append(layer_weights)
	return weights
