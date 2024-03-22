#!/usr/bin/env python3

import argparse
import sys
import functools
import requests

base_url = "https://www.ylioppilastutkinto.fi/fi/tutkinnon-suorittaminen/pisterajat/pisterajat-" 

aine_dict = {
  "MAA": "Matematiikka, pitkä oppimäärä",
  "MAB":"Matematiikka, lyhyt oppimäärä",
  "FY": "Fysiikka",
  "KE": "Kemia",
  "BI": "Biologia",
  "TE": "Terveystieto",
  "MA": "Maantiede",
  "YH": "Yhteiskuntaoppi",
  "HI": "Historia",
  "PS": "Psykologia",
  "FI": "Filosofia",
  "US": "Uskonto",
  "EN": "Englanti, pitkä oppimäärä",
  "RU": "Ruotsi, keskipitkä oppimäärä" 
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

parser = argparse.ArgumentParser(prog='yo-raja-check', description='Laskea cool things about yo pisterajat!')

vuodet = []

parser.add_argument('-v', '--vuodet', help="Format: (VUOSILUKU(K | S),...) , esim. 2024S,2024K", required=True)
parser.add_argument('-a', '--aine', required=True)
parser.add_argument('arvosana', help="Mitä sä haluut??")

args = parser.parse_args()

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

def parse_vuodet():
  global search_paths
  global vuodet
  vuodet_string = args.vuodet
  vuodet = [ x.strip() for x in vuodet_string.split(",") ]
  search_paths = [ convert_to_path(x) for x in vuodet ]

def get_piste_raja(url: str):
  data = requests.get(url)
  html = data.text
  start_index = html.rfind("<tbody>")
  end_index = html.rfind("</tbody>")
  table = html[start_index:end_index].split("<tbody>")[1]
  table_rows = [ x[8:] for x in table.split("</tr>") ]
  table_cols = [ x.split("</td><td>") for x in table_rows ]

  obj = {}
  for col in table_cols:
    # print(col[0].replace("<span>", "").replace("</span>", ""))
    obj[col[0].replace("<span>", "").replace("</span>", "")] = [ x.replace("</td>", "").replace("<span>", "").replace("</span>", "") for x in col[1:] ]

  name_in_obj = aine_dict[args.aine]
  return int(obj[name_in_obj][arvosana_map[args.arvosana]])


parse_vuodet()

search_urls = [ base_url + x for x in search_paths ]

piste_rajat = [ get_piste_raja(x) for x in search_urls ] 

keskiarvo = functools.reduce(lambda a, b: a+b, piste_rajat) / len(piste_rajat)

print(f"{aine_dict[args.aine]}")
print("\tPisterajat:")
for i, raja in enumerate(piste_rajat):
  print(f"\t\t{vuodet[i]}: {raja}")
print(f"\tKeskiarvo on: {keskiarvo}")
