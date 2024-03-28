from ytl import pisterajat
from abitreenit import poll_scores
from AIr.core import NeuralNetwork 

vuodet = ["2023S", "2023K", "2022S", "2022K", "2021S", "2021K", "2021S", "2020K"]

arvosanat = ["L", "E", "M", "C", "B", "A", "i"]

order = ["millainen", "fiilis"] 

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


def get_learning_data(aineet: str, maksimi_pisteet=120):
  data = []
  answers = []
  for aine in aineet:
    for vuosi in vuodet:
      d = []
      rajat = []
      scores = poll_scores(aine, vuosi, minimal=True)
      for arvosana in arvosanat:
        raja = pisterajat(aine, [vuosi], arvosana)["raw"][vuosi] 
        rajat.append(round(raja/maksimi_pisteet, 6))
      for key in order:
        d = [*d, *scores[key].values()]
      answers.append(rajat)
      data.append(d)
      print((data, answers))
      print("\n")

  return data,answers

def tmp():
    rajat = []
    for arvosana in arvosanat:
      raja = pisterajat("MAA", ["2019S"], arvosana)["raw"]["2019S"] 
      rajat.append(round(raja/120, 6))
    print(rajat)

aine_model_dict = {
  "MAA": "MAA-FY-fiilis-millainen.npz",
  "FY": "MAA-FY-fiilis-millainen.npz"
}

base_path = "/home/eeli/coding/projects/yo-check/ai_models/"

output_order = ["L", "E", "M", "C", "B", "A", "i"]



def predict(aine, vuosi):
  file_name = aine_model_dict.get(aine)
  if file_name is None:
    print("Not yet implemented")
    return
  nn = NeuralNetwork.load_from_file(base_path + file_name)

  input = get_learning_example(aine, vuosi, input_only=True)[0]

  prediction = nn.run(input)
  
  for n,p in zip(output_order, prediction[0]):
        print(f"{n}: {p*120}")

