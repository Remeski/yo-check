import numpy as np

np.random.seed(0)

class Layer:
  def __init__(self, n_input, m_output, activation=None, weights=None, biases=None):

    if activation:
      self.activation = activation
    else:
      self.activation = lambda x : x

    if (weights is not None) and (np.array(weights).shape != (n_input, m_output)):
      self.weights = weights
    else:
      self.weights = np.random.random((n_input, m_output))

    if (biases is not None) and (np.array(biases).shape != (1, m_output)):
      self.biases = np.random.random((1, m_output))
    else:
      self.biases = np.random.random((1,m_output))

  def forward(self, input):
    Z = np.dot(np.array(input), np.array(self.weights)) + np.array(self.biases) 
    self.output = self.activation(Z)


def Activation_ReLU(X):
  return np.maximum(0, X)

# layers: [ { n: N_NODES, 
#             activation: ACTIVATION_FUNCTION,
#           }, ... ]
# The last layer in layers will be the output layer
class NeuralNetwork:
  def __init__(self, n_input, layers, file_path=None):
    self.n_input = n_input
    self.layer_schema = layers
    if file_path:
      self.load(file_path)
    else:
      self.network = []
      for i,l in enumerate(self.layer_schema):
        input = self.n_input
        if i > 0:
          input = self.network[i-1]["n"]
        layer = Layer(input, l["n"], activation=l.get("activation"))
        self.network.append(layer)
  
  def forward(self, input):
    output = input
    for l in self.network:
      l.forward(output)
      output = l.output
    return output

  def store(self, file_path="data"):
    store_arrays = []
    for l in self.network:
      store_arrays.append(l.weights)
      store_arrays.append(l.biases)
    np.savez(file_path, *store_arrays)

  def load(self, file_path="data"):
    npz = np.load(file_path + ".npz")
    if len(npz.files) % 2 != 0:
      print("Loaded values seem to me corrupt")
    self.network = []
    for i,l in enumerate(self.layer_schema):
      input = self.n_input 
      if i > 0:
        input = self.network[i-1]["n"]
      layer = Layer(input, l.get("n"), activation=l.get("activation"), weights=np.array(npz["arr_" + str(i)]), biases=np.array(npz["arr_" + str(i+1)]))
      self.network.append(layer)

# Test input
input = [[1,0,0], 
         [0,1,0],
         [0,0,1],
         [0,0,0]]

# n_input=4 and n_output=3 => 4*3 matrix
weights1 = [[1,1,3], 
            [2,2,4],
            [3,3,4]]
biases1 = [[0,0,0]]

layers = [{"n": 3, "activation": Activation_ReLU}]
network = NeuralNetwork(3, layers)
# network.store("data_ai")
# print(network.forward(input))
