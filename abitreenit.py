import re
import requests

base_url = "https://yle.fi/aihe/abitreenit/"
exams_url = "https://tehtava.api.yle.fi/v1/public/exams.json?uuid="
answers_url = "https://tehtava.api.yle.fi/v1/public/polls?question_uuids="

aine_dict = {
  "MAA": "matematiikka",
  "MAB": "matematiikka",
  "AI": "aidinkieli", 
  "FY": "fysiikka",
  "KE": "kemia",
  "BI": "biologia",
  "TE": "terveystieto",
  "MA": "maantiede",
  "YH": "yhteiskuntaoppi",
  "HI": "historia",
  "PS": "psykologia",
  "FI": "filosofia",
  "US": "uskonto",
  "EN": "englanti",
  "RU": "ruotsi" 
}

aine_koe_dict = {
  "MAA": "pitkä oppimäärä",
  "MAB": "lyhyt oppimäärä",
  "AI": "aidinkieli", 
  "FY": "fysiikka",
  "KE": "kemia",
  "BI": "biologia",
  "TE": "terveystieto",
  "MA": "maantiede",
  "YH": "yhteiskuntaoppi",
  "HI": "historia",
  "PS": "psykologia",
  "FI": "filosofia",
  "US": "uskonto",
  "EN": "englanti",
  "RU": "ruotsi" 
}

question_keywords = {
  "millainen": ["millainen", "mielestäsi"],
  "fiilis": ["fiilis"],
  "arvosanani": ["uskon", "arvosanakseni"],
  "valmistautuminen": ["valmistautunut"]
}

def find_href_of_a(body: str, search_string: str):
  index = body.rfind(search_string) 
  start_index = 0
  for i in range(index, 0, -1):
    if body[i - 1] + body[i] == "<a":
      start_index = i + 1
      break
  elem = body[start_index:index]
  
  return re.search(r"href=\"(.*)\"", elem).group(1)

def aine_vuosi_to_search_string(aine: str, vuosi: str) -> str:
  vuosiluku = vuosi[:4]
  vuodenaika = vuosi[-1]
  search_string = vuosiluku
  if vuodenaika.upper() == "K":
    search_string += " kevät: "
  if vuodenaika.upper() == "S":
    search_string += " syksy: "
  search_string += aine_koe_dict[aine]
  return search_string

def get_url(aine: str, vuosi: str):
  aine_sivu = requests.get(base_url + aine_dict[aine]).text
  kaikki_kokeet_url = find_href_of_a(aine_sivu, "Katso kaikki yo-kokeet")
  kaikki_kokeet = requests.get(kaikki_kokeet_url).text
  return find_href_of_a(kaikki_kokeet, aine_vuosi_to_search_string(aine, vuosi))

def get_possible_exam_uuids(url: str):
  data = requests.get(url).text
  uuids = re.findall(r"<div.*(?:data-ydd-tehtava-exam-id|data-exam-id)=.\d\d-([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}).", data)
  return uuids

def get_exams_json(possible_uuids: list[str]):
  for uuid in possible_uuids: 
    url = exams_url + uuid
    exams = requests.get(url).json()["data"][0]
    if exams["exam_type"] != "poll":
      continue
    return exams["questions"]
  return None

def get_question_answers(question_uuid: str):
  url = answers_url + question_uuid
  answers = requests.get(url).json()["data"]
  obj = {}
  for answer in answers:
    obj[answer["option_id"]] = answer["count_option"]
  return obj

def parse_exams(questions):
  obj = {}
  for q in questions:
    q_uuid = q["uuid"]
    q_answers = get_question_answers(q_uuid)
    q_obj = {}
    for option in q["options"]:
      q_obj[option["text"]] = q_answers[str(option["id"])]
    obj[q["main_text"]] = q_obj
  return obj

def get_polls(aine: str, vuosi: str):
  koesivu_url = get_url(aine, vuosi)
  exam_uuid = get_possible_exam_uuids(koesivu_url)
  exams_json = get_exams_json(exam_uuid)
  return parse_exams(exams_json)

def calculate_kokelaat(polls: dict):
  max_kokelaat = 0
  for q in polls:
    temp = 0
    for ans in polls[q].values():
      temp += ans
    if temp > max_kokelaat:
      max_kokelaat = temp
  return max_kokelaat

def parse_questions(polls: dict, minimal=False):
  obj = {}
  for q in polls:
    q_name_actual: str = q.strip()
    q_name = "error"
    for qk in question_keywords:
      kws = question_keywords[qk]
      for kw in kws:
        if q_name_actual.lower().__contains__(kw):
          q_name = qk 
          break
    if minimal:
      obj[q_name] = dict((i + 1, v) for (i, v) in enumerate(polls[q].values())) 
    else:
      obj[q_name] = dict((k.lower(), v) for (k, v) in polls[q].items()) 
  return obj

def calculate_relative_scores(parsed_questions: dict):
  obj = {}
  for q in parsed_questions:
    q_obj = {}
    answers = parsed_questions[q]
    sum = 0
    for ans in answers.values():
      sum += ans
    for ans in answers:
      q_obj[ans] = round(answers[ans]/sum, 2) 
    obj[q] = q_obj
  return obj

