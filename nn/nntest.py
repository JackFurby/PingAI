import nn

network = nn.NeuralNetwork(nn.random_weights([2, 3, 2], 1))
network.mutate(0.1)

print(network.calculate_output_layer([0.5, 0.5]))
