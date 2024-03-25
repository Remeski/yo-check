from ytl import pisterajat
from abitreenit import poll_scores

vuodet = ["2023S", "2023K", "2022S", "2022K", "2021S", "2021K", "2021S"]

def get_learning_data(aine: str, arvosana: str):
  data = []
  answers = []
  for vuosi in vuodet:
    d = []
    raja = pisterajat(aine, [vuosi], arvosana)["raw"][vuosi] 
    scores = poll_scores(aine, vuosi, minimal=True).values()
    for score in scores:
      d = [*d, *list(score.values())]
    data.append(d)
    answers.append(raja)

  return data,answers

