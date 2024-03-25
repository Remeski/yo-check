import numpy as np
import AI.Activations as Activations

np.random.seed(0)

class Layer:
  def __init__(self, n_input, n_output, activation=None, weights=None, biases=None):
    self.n_input = n_input
    self.n_output = n_output

    if activation:
      self.activation = activation
    else:
      self.activation = Activations.ReLU()

    if (weights is not None) and (np.array(weights).shape == (n_input, n_output)):
      self.weights = np.array(weights)
    else:
      self.weights = np.random.randn(n_input, n_output)

    if (biases is not None) and (np.array(biases).shape == (1, n_output)):
      self.biases = np.array(biases)
    else:
      self.biases = np.zeros((1,n_output))

  def forward(self, input):
    self.Z = np.dot(np.array(input), np.array(self.weights)) + np.array(self.biases) 
    self.output = self.activation.calc(self.Z)

# layers: [ { n: N_NODES, 
#             activation: ACTIVATION_FUNCTION,
#           }, ... ]
# The last layer in layers will be the output layer
class NeuralNetwork:
  def __init__(self, n_input, layers, file_path=None):
    self.n_input = n_input
    self.layers = layers
    if file_path is not None:
      self.load(file_path)
    else:
      self.network = []
      for i,l in enumerate(self.layers):
        input = self.n_input
        if i > 0:
          input = self.network[i-1].n_output
        layer = Layer(input, l["n"], activation=l.get("activation"))
        self.network.append(layer)
  
  def forward(self, input):
    self.input = input
    output = input
    for l in self.network:
      l.forward(output)
      output = l.output
    self.output = output

  def backprop(self, Y):
    dW = []
    dB = []

    N = len(Y)

    for l in self.network:
      dW.append(np.zeros(l.weights.shape))
      dB.append(np.zeros(l.weights.shape))

    ls = self.network

    delta = self.loss_prime(Y) * ls[-1].activation.prime(ls[-1].Z)
    dB[-1] = 1/N * np.sum(delta, axis=0)
    dW[-1] = 1/N * np.dot(ls[-2].output.T, delta)

    for i in range(2, len(self.network)):
      #                              n x 3                 n x 2         2 x 3                
      delta = ls[-i].activation.prime(ls[-i].Z) * np.dot(delta, ls[-i+1].weights.T)
      dB[-i] = 1/N * np.sum(delta, axis=0)
      dW[-i] = 1/N * np.dot(ls[-i-1].output.T, delta) 

    delta = ls[0].activation.prime(ls[0].Z) * np.dot(delta, ls[1].weights.T)
    dB[0] = 1/N * np.sum(delta, axis=0)
    dW[0] = 1/N * np.dot(np.array(self.input).T, delta)

    return dW, dB

  # y_hat is the expected result while y is the result from network
  def loss(self, Y):
    return 0.5*np.sum((self.output-Y)**2)

  def loss_prime(self,Y):
    return (self.output-Y)

  # Batch is a tuple ([X], [Y]) where [X] is a matrix thats rows are one set of inputs
  #                                   [Y] is a matrix thats rows are the sets expected output 
  def train(self, batch, eeta):
    X,Y = batch
    self.forward(X)
    self.cur_loss = self.loss(Y)
    dW, dB = self.backprop(Y)

    for l, dw, db in zip(self.network, dW, dB):
      l.weights -= eeta * dw
      l.biases -= eeta * db

  def run(self, input):
    self.forward(input)
    return self.output
  
  def test_loss(self, batch):
    self.forward(batch[0])
    return self.loss(batch[1])
  # 
  # def accuracy(self, Y):
  #   return 1/len(Y) * np.sum(self.output / Y)
  #
  # def test_accuracy(self, batch):
  #   self.forward(batch[0])
  #   return self.accuracy(batch[1])
  #

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
    for i,l in enumerate(self.layers):
      input = self.n_input 
      if i > 0:
        input = self.network[i-1].n_output
      layer = Layer(input, l.get("n"), activation=l.get("activation"), weights=npz["arr_" + str(2*i)], biases=npz["arr_" + str(2*i+1)])
      self.network.append(layer)

