import sys
import functools
import requests

base_url = "https://www.ylioppilastutkinto.fi/fi/tutkinnon-suorittaminen/pisterajat/pisterajat-" 

aine_dict = {
  "MAA": ["Matematiikka, pitkä oppimäärä", "Matematiikan koe, lyhyt oppimäärä"],
  "MAB": ["Matematiikka, lyhyt oppimäärä", "Matematiikan koe, pitkä oppimäärä"],
  "AI": ["Äidinkieli ja kirjallisuus, suomi", "Äidinkieli, suomi", "äidinkielen koe, suomi"],
  "FY": ["Fysiikka"],
  "KE": ["Kemia"],
  "BI": ["Biologia"],
  "TE": ["Terveystieto"],
  "MA": ["Maantiede"],
  "YH": ["Yhteiskuntaoppi"],
  "HI": ["Historia"],
  "PS": ["Psykologia"],
  "FI": ["Filosofia"],
  "US": ["Uskonto"],
  "EN": ["Englanti, pitkä oppimäärä"],
  "RU": ["Ruotsi, keskipitkä oppimäärä"] 
}

arvosana_map = {
    "L": 0,
    "E": 1,
    "M": 2,
    "C": 3,
    "B": 4,
    "A": 5,
    "i+": 6,
    "i": 7,
    "i-": 8,
}

search_paths = []

vuodet = []

def convert_to_path(vuosi_string: str):
  vuosi = vuosi_string[:4]
  vuodenaika = vuosi_string[4].upper()
  path = ""
  if vuodenaika == "K":
    path = "kevat"
  elif vuodenaika == "S":
    path = "syksy"
  else:
    print("somethings wrong you dingus", file=sys.stderr)

  path += "-" + vuosi
  return path

def vuodet_to_paths(vuodet: list[str]) -> list[str]:
  return [ convert_to_path(x) for x in vuodet ]

def find_arvosanat(pisteet: dict[str, list[str]], aine: str) -> list[str]:
  names_in_obj = aine_dict[aine]
  for name in names_in_obj:
    try: 
      arvosanat = pisteet[name]
      return arvosanat
    except KeyError:
      continue
  return ["0"]

def get_piste_raja(url: str, arvosana: str, aine: str):
  data = requests.get(url)
  html = data.text
  start_index = html.rfind("<tbody>")
  end_index = html.rfind("</tbody>")
  table = html[start_index:end_index].split("<tbody>")[1]
  table_rows = [ x[8:] for x in table.split("</tr>") ]
  table_cols = [ x.split("</td><td>") for x in table_rows ]

  obj = {}
  for col in table_cols:
    obj[col[0].replace("<span>", "").replace("</span>", "")] = [ x.replace("</td>", "").replace("<span>", "").replace("</span>", "") for x in col[1:] ]
  
  return int(find_arvosanat(obj, aine)[arvosana_map[arvosana]])

def pisterajat(aine: str, vuodet: list[str], arvosana: str) -> dict: 
  search_urls = [ base_url + x for x in vuodet_to_paths(vuodet) ]
  piste_rajat = [ get_piste_raja(x, arvosana, aine) for x in search_urls ] 
  keskiarvo = functools.reduce(lambda a, b: a+b, piste_rajat) / len(piste_rajat)

  obj = {}
  obj["raw"] = {}
  for i, raja in enumerate(piste_rajat):
    obj["raw"][vuodet[i]] = raja

  obj["mean"] = round(keskiarvo, 1)
  return obj

