import numpy as np
import AI.Activations as Activations

np.random.seed(0)

class Layer:
  def __init__(self, n_input, n_output, activation="ReLU", weights=None, biases=None):
    self.n_input = n_input
    self.n_output = n_output

    self.activation = Activations.name_to_class[activation]()
    self.activation_name = activation

    if (weights is not None) and (np.array(weights).shape == (n_input, n_output)):
      self.weights = np.array(weights)
      
      self.weights = np.random.randn(n_input, n_output)

    if (biases is not None) and (np.array(biases).shape == (1, n_output)):
      self.biases = np.array(biases)
    else:
      self.biases = np.zeros((1,n_output))

  def forward(self, input):
    self.Z = np.dot(np.array(input), np.array(self.weights)) + np.array(self.biases) 
    self.output = self.activation.calc(self.Z)

# schema: { n_input: INPUT_NODES, 
#           layers: [ { n: N_NODES, 
#             activation: ACTIVATION_FUNCTION_NAME,
#           }, ...],
#         } 
# The last layer in layers will be the output layer
class NeuralNetwork:
  def __init__(self, schema, layers=None):
    self.schema = schema
    self.n_input = schema["n_input"]
    self.layers_schema = schema["layers"]
    if layers is not None and self.validate_layers(schema, layers):
      self.layers = layers
    else:
      self.layers = []
      for i,l in enumerate(self.layers_schema):
        input = self.n_input
        if i > 0:
          input = self.layers[i-1].n_output
        layer = Layer(input, l["n"], activation=l.get("activation"))
        self.layers.append(layer)

  def validate_layers(self, schema, layers):
    schema_layers = schema["layers"]
    if len(layers) != len(schema_layers):
      return False
    for ls, l in zip(schema_layers, layers): 
      if l.n_output != ls["n"]:
        return False
      if l.activation_name != ls.get("activation"):
        return False
    return True

  def forward(self, input):
    self.input = input
    output = input
    for l in self.layers:
      l.forward(output)
      output = l.output
    self.output = output

  def backprop(self, Y):
    dW = []
    dB = []

    N = len(Y)

    for l in self.layers:
      dW.append(np.zeros(l.weights.shape))
      dB.append(np.zeros(l.weights.shape))

    ls = self.layers

    delta = self.loss_prime(Y) * ls[-1].activation.prime(ls[-1].Z)
    dB[-1] = 1/N * np.sum(delta, axis=0)
    dW[-1] = 1/N * np.dot(ls[-2].output.T, delta)

    for i in range(2, len(self.layers)):
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
  def train(self, batch, eta):
    X,Y = batch
    self.forward(X)
    self.cur_loss = self.loss(Y)
    dW, dB = self.backprop(Y)

    for l, dw, db in zip(self.layers, dW, dB):
      l.weights -= eta * dw
      l.biases -= eta * db

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

  def store(self, file_path: str):
    file_path = file_path.rstrip(".npz")
    store_arrays = []
    for l in self.layers:
      store_arrays.append(l.weights)
      store_arrays.append(l.biases)
    np.savez(file_path, schema=self.schema, *store_arrays)


  @staticmethod
  def load_from_file(file_path: str):
    file_path = file_path if file_path.rfind(".npz") != -1 else file_path + ".npz"
    npz = np.load(file_path, allow_pickle=True)
    schema = npz["schema"][()]
    layers_schema = schema["layers"]

    layers = []
    if (len(npz.files) - 1) % 2 != 0:
      print("Loaded values seem to me corrupted")

    for i,l in enumerate(layers_schema):
      input = schema["n_input"]
      if i > 0:
        input = layers[i-1].n_output
      layer = Layer(input, l.get("n"), activation=l.get("activation"), weights=npz["arr_" + str(2*i)], biases=npz["arr_" + str(2*i+1)])
      layers.append(layer)

    return NeuralNetwork(schema, layers)
