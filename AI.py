from ytl import pisterajat
from abitreenit import poll_scores
from AIr.core import NeuralNetwork 
from AIr.train import Trainer
import argparse
import pickle
import os
import fnmatch
import statistics

vuodet = ["2023S", "2023K", "2022S", "2022K", "2021S", "2021K", "2021S", "2020K"]

arvosanat = ["L", "E", "M", "C", "B", "A", "i"]

order = ["millainen", "fiilis"] 

parser = argparse.ArgumentParser(prog='yo-AI')

parser.add_argument("komento")
parser.add_argument("-a", "--aine")
parser.add_argument("-v", "--vuosi")

def get_learning_example(aine, vuosi, input_only=False, maksimi_pisteet=120):
  d = []
  rajat = []
  scores = poll_scores(aine, vuosi, minimal=True)
  if not input_only:
    for arvosana in arvosanat:
      raja = pisterajat(aine, [vuosi], arvosana)["raw"][vuosi] 
      rajat.append(round(raja/maksimi_pisteet, 6))
  for key in order:
    d = [*d, *scores[key].values()]
  return (d, rajat)

def get_learning_data(aineet, maksimi_pisteet=120):
  data = []
  answers = []
  vars = {}
  for aine in aineet:
    sum = {
      "L": 0,
      "E": 0,
      "M": 0,
      "C": 0,
      "B": 0,
      "A": 0,
      "i": 0
    }
    rajat = {
      "L": [],
      "E": [],
      "M": [],
      "C": [],
      "B": [],
      "A": [],
      "i": []
    }
    n = 0
    for vuosi in vuodet:
      try:
        d = []
        scores = poll_scores(aine, vuosi, minimal=True)
        for arvosana in arvosanat:
          raja = pisterajat(aine, [vuosi], arvosana)["raw"][vuosi] 
          sum[arvosana] += raja
          rajat[arvosana].append(raja)
        for key in order:
          d = [*d, *scores[key].values()]
        n += 1
        data.append(d)
      except Exception as err: 
        print(f"Error at {aine} {vuosi}")
        print(err)
        with open(".recovered_data.pcl", 'wb') as f:
          pickle.dump(data, f)


    if n == 0:
      continue

    means = {}
    for arvosana in sum:
      means[arvosana] = sum[arvosana] / n

    mu = statistics.mean(means.values())
    sigma = statistics.stdev(means.values())

    vars[aine] = {"mu": mu, "sigma": sigma}

    for i in range(0, n):
      a = []
      for arvosana in arvosanat:
        a.append(round((rajat[arvosana][i] - mu)/sigma, 6))
      answers.append(a)

  return data,answers,vars

aine_model_dict = {
  "MAA": "MAA-FY-fiilis-millainen.npz",
  "FY": "MAA-FY-fiilis-millainen.npz",
  "KE": "KE-fiilis-millainen.npz",
  "YH": "YH-fiilis-millainen.npz"
}

base_path = "ai_models/"

output_order = ["L", "E", "M", "C", "B", "A", "i"]


def find(pattern, path):
  results = []
  for root, _, files in os.walk(path):
    for name in files:
      if fnmatch.fnmatch(name, pattern):
        results.append(os.path.join(root, name))
  return results

def latest(results):
  if len(results) < 1:
    return None
  latest = results[0]
  for res in results:
    if int(res.rstrip(".npz")[-3:]) > int(latest.rstrip(".npz")[-3:]):
      latest = res
  return latest

def run(aine, vuosi):
  file_name = latest(find("*" + aine + "*", base_path))

  if file_name is None:
    print("Not yet implemented")
    return

  print(f"Using model {file_name}")

  nn = NeuralNetwork.load_from_file(file_name)

  input = get_learning_example(aine, vuosi, input_only=True)[0]

  prediction = nn.run(input)

  vars = {}
  with open(find("*" + aine + "*", ".cache/")[0], 'rb') as f:
    _,_,vars = pickle.load(f)
  
  for n,p in zip(output_order, prediction[0]):
        print(f"{n}: {p*vars[aine]['sigma']+vars[aine]['mu']}")

schema = lambda dataset: {"n_input": len(dataset[0][0]), "layers": [{ "n": 100, "activation": "LeakyReLU" },{ "n": 50, "activation": "Sigmoid" }, {"n": len(dataset[1][0]), "activation": "Linear"}]}

def train(aineet, file_path):
  data = ()

  try:
    os.mkdir(".cache")
  except:
    pass

  cached_path =f".cache/{'-'.join(aineet)}.pkl" 

  if os.path.isfile(cached_path):
    with open(cached_path, "rb") as f:
      data = pickle.load(f)
  else:
    data = get_learning_data(aineet)
    with open(cached_path, 'wb') as f:
      pickle.dump(data, f)

  dataset = (data[0],data[1])
  trainer = Trainer(schema=schema(dataset), file_path=file_path)
  trainer.train(dataset, noise=0.03, epoch=10000, mini_batch_size=10)


args = parser.parse_args()

if args.komento == "opeta":
  name = latest(find(args.aine.upper().replace(",", "-") + "*", "ai_models/"))
  train(args.aine.split(","), name if name is not None else base_path + args.aine.upper().replace(",", "-") + "-fiilis-millainen")
if args.komento == "laske":
  run(args.aine, args.vuosi)

