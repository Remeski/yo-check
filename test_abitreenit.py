import unittest
import abitreenit

class TestAbitreenit(unittest.TestCase):

  def get_polls(self):
    should_be = {'Millainen maantieteen koe mielestäsi oli?\n': {'Helppo': 98, 'Juuri sopiva': 369, 'Melko vaativa': 349, 'Ihan liian vaikea': 70, 'Ei mikään edellisistä, kerro kommenteissa ↓': 45}, 'Uskon saavani arvosanakseni...\n': {'L': 81, 'E': 114, 'M': 207, 'C': 207, 'B': 81, 'A': 48, 'Pääsispä edes läpi...': 36, 'En uskalla edes arvata tai toivoa mitään.': 62}, 'Mikä on päällimmäinen fiilis?\n': {'Voittajafiilis!': 60, 'Positiivisesti yllättynyt.': 195, 'Ihan jees.': 402, 'Pettynyt.': 118, 'Ei mikään edellisistä, kerro kommenteissa ↓': 31}, 'Olin valmistautunut maantieteen kokeeseen...\n': {'Huolellisesti, aloitin jo hyvissä ajoin.': 158, 'Ihan hyvin.': 251, 'Viime tippaan jäi.': 149, 'Huonosti.': 77, 'En mitenkään.': 76}}
    polls = abitreenit.get_polls("MA", "2022K")
    self.assertIsNotNone(polls)
    self.assertEqual(polls, should_be)

  def parse_questions(self):
    polls = {'Millainen maantieteen koe mielestäsi oli?\n': {'Helppo': 98, 'Juuri sopiva': 369, 'Melko vaativa': 349, 'Ihan liian vaikea': 70, 'Ei mikään edellisistä, kerro kommenteissa ↓': 45}, 'Uskon saavani arvosanakseni...\n': {'L': 81, 'E': 114, 'M': 207, 'C': 207, 'B': 81, 'A': 48, 'Pääsispä edes läpi...': 36, 'En uskalla edes arvata tai toivoa mitään.': 62}, 'Mikä on päällimmäinen fiilis?\n': {'Voittajafiilis!': 60, 'Positiivisesti yllättynyt.': 195, 'Ihan jees.': 402, 'Pettynyt.': 118, 'Ei mikään edellisistä, kerro kommenteissa ↓': 31}, 'Olin valmistautunut maantieteen kokeeseen...\n': {'Huolellisesti, aloitin jo hyvissä ajoin.': 158, 'Ihan hyvin.': 251, 'Viime tippaan jäi.': 149, 'Huonosti.': 77, 'En mitenkään.': 76}}
    parsed = abitreenit.parse_questions(polls, minimal=True)

if __name__ == '__main__':
  unittest.main()
