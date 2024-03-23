import re
import requests

base_url = "https://yle.fi/aihe/abitreenit/" 

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


def get_polls(aine: str, vuosi: str):
  return get_url(aine, vuosi)

