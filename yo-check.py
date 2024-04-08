from ytl import pisterajat, aine_dict
import argparse

parser = argparse.ArgumentParser(prog='yo-raja-check', description='Laskea cool things about yo pisterajat!')

parser.add_argument('-v', '--vuodet', help="Format: VUOSILUKU(K | S),..., esim. 2024S,2024K", required=True)
parser.add_argument('-a', '--aine', help="Format: Lyhenne aineelle, esim. HI, YH, MAA (pitkä matematiikka) jne.", action="append", required=True)
parser.add_argument('arvosanat', help="Kyl sä tiiät mitä ne on L,E,M jne.")

args = parser.parse_args()

def parse_vuodet_string(vuodet_string: str):
  return [ x.strip() for x in vuodet_string.split(",") ]

vuodet = parse_vuodet_string(args.vuodet)

for aine in args.aine:
  print(f"{aine_dict[aine][0]}")
  for arvosana in args.arvosanat.split(","):
    p = pisterajat(aine, vuodet, arvosana)
    print(f"\t{arvosana}:n pisterajat")

    for v in p["raw"].keys():
      print(f"\t\t{v}: {p['raw'][v]}")

    print(f"\tKeskiarvo: {p['mean']}")
