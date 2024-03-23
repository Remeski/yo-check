import pisterajat
import abitreenit
import argparse

parser = argparse.ArgumentParser(prog='yo-raja-check', description='Laskea cool things about yo pisterajat!')

parser.add_argument('-v', '--vuodet', help="Format: (VUOSILUKU(K | S),...) , esim. 2024S,2024K", required=True)
parser.add_argument('-a', '--aine', action="append", required=True)
parser.add_argument('arvosanat', help="Kyl sä tiiät mitä ne on L,E,M jne.")

args = parser.parse_args()

def parse_vuodet_string(vuodet_string: str):
  return [ x.strip() for x in vuodet_string.split(",") ]

vuodet = parse_vuodet_string(args.vuodet)

for aine in args.aine:
  print(abitreenit.get_polls(aine, vuodet[0]))
  print(f"{pisterajat.aine_dict[aine][0]}")
  for arvosana in args.arvosanat.split(","):
    print(pisterajat.pisterajat(arvosana, aine, vuodet))
