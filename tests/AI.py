import os
import numpy as np
import unittest
import math
import random
from numpy.random import bytes as randombytes
import AI.Core as AI
from AI.Activations import Linear, ReLU, Sigmoid

test_layers = [{"n": 3, "activation": ReLU()}, {"n": 5, "activation": ReLU()}, {"n": 1, "activation": Linear()}]

test_layers_sin = [{"n": 5, "activation": ReLU()}, {"n": 5, "activation": ReLU()}, {"n": 1, "activation": Linear()}]

test_layers_xor = [{"n": 5, "activation": ReLU()}, {"n": 5, "activation": ReLU()}, {"n": 1, "activation": Linear()}]

def batch_xor():
  return ([[0,0], [0,1], [1,0], [1,1]], [[0], [1], [1], [0]])


def batch_sin(n, _range=4): 
  X = []
  Y = []
  for _ in range(0,n+1):
    x = random.random() * random.randint(0, _range)
    X.append([x])
    Y.append([math.sin(x)])

  return (X, Y)

class TestAILayers(unittest.TestCase):

  def test_layer_forward(self):
    input = [[1,1], [2,2]]
    layer = AI.Layer(2, 3)
    weights = layer.weights
    biases = layer.biases

    try:
      layer.forward(input)
    except:
      self.fail("forward prop not working")

    self.assertTrue((layer.output == np.dot(input, weights) + biases).all())

class TestAINeuralNetwork(unittest.TestCase):
  # Just to test that nothing errors
  def test_with_sin(self, save=False):
    batch_size = 5
    training_iterations = 1000
    eeta = 0.1

    layers = test_layers_sin
    network = AI.NeuralNetwork(1, layers) 

    for _ in range(0, training_iterations):
      batch = batch_sin(batch_size)
      network.train(batch, eeta)

    loss = network.test_loss(batch_sin(batch_size))

    self.assertTrue(loss < 1)

    if save:
      network.store("sin_test")

  def test_with_xor(self, save=False):
    training_iterations = 100

    eeta = 0.1

    layers = test_layers_xor
    network = AI.NeuralNetwork(2, layers) 

    for _ in range(0, training_iterations):
      network.train(batch_xor(), eeta)

    loss = network.test_loss(batch_xor())

    self.assertTrue(loss < 1)

    if save:
      network.store("xor_test")


    
  def test_forward_prop(self):
    network = AI.NeuralNetwork(3, test_layers)
    input = [[1,2,3],[1,2,3],[1,2,3]]
    network.forward(input)
    output = network.output
    self.assertIsNotNone(output)


  def test_store_and_load(self):
    network = AI.NeuralNetwork(3, test_layers)
    try: 
      os.mkdir("/tmp/yo_check/")
    except:
      pass

    file_name = randombytes(10).hex()

    network.store(file_path=f"/tmp/yo_check/{file_name}")
    network2 = AI.NeuralNetwork(3, test_layers, file_path=f"/tmp/yo_check/{file_name}")

    os.remove(f"/tmp/yo_check/{file_name}.npz")

    self.assertEqual(len(network.network), len(network2.network))
    for l1,l2 in zip(network.network, network2.network):
      for w1,w2 in zip(l1.weights, l2.weights):
        self.assertTrue((w1 == w2).all())
      for b1,b2 in zip(l1.biases, l2.biases):
        self.assertTrue((b1 == b2).all())

class TestAIActivations(unittest.TestCase):
  def test_sigmoid(self):
    input = np.array([[math.log(1, math.e), math.log(2, math.e), math.log(3, math.e)], 
                      [math.log(4, math.e), math.log(5, math.e), math.log(6, math.e)]])
    expected = [[1/2,2/3,3/4], 
                [4/5,5/6,6/7]]

    expected_prime = [[1/4, 2/9, 3/16],
                      [4/25, 5/36, 6/49]]

    s = Sigmoid().calc(input)

    self.assertTrue((np.round(s,4) == np.round(expected,4)).all()) 

    s_prime = Sigmoid().prime(input)

    self.assertTrue((np.round(s_prime,3) == np.round(expected_prime,3)).all())

