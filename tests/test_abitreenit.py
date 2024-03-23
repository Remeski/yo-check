import unittest
import abitreenit

class TestParsing(unittest.TestCase):

  polls = {'Millainen maantieteen koe mielestäsi oli?\n': {'Helppo': 98, 'Juuri sopiva': 369, 'Melko vaativa': 349, 'Ihan liian vaikea': 70, 'Ei mikään edellisistä, kerro kommenteissa ↓': 45}, 'Uskon saavani arvosanakseni...\n': {'L': 81, 'E': 114, 'M': 207, 'C': 207, 'B': 81, 'A': 48, 'Pääsispä edes läpi...': 36, 'En uskalla edes arvata tai toivoa mitään.': 62}, 'Mikä on päällimmäinen fiilis?\n': {'Voittajafiilis!': 60, 'Positiivisesti yllättynyt.': 195, 'Ihan jees.': 402, 'Pettynyt.': 118, 'Ei mikään edellisistä, kerro kommenteissa ↓': 31}, 'Olin valmistautunut maantieteen kokeeseen...\n': {'Huolellisesti, aloitin jo hyvissä ajoin.': 158, 'Ihan hyvin.': 251, 'Viime tippaan jäi.': 149, 'Huonosti.': 77, 'En mitenkään.': 76}}

  def test_parse_questions_minimal(self):
    assertion = {'millainen': {1: 98, 2: 369, 3: 349, 4: 70, 5: 45}, 'arvosanani': {1: 81, 2: 114, 3: 207, 4: 207, 5: 81, 6: 48, 7: 36, 8: 62}, 'fiilis': {1: 60, 2: 195, 3: 402, 4: 118, 5: 31}, 'valmistautuminen': {1: 158, 2: 251, 3: 149, 4: 77, 5: 76}} 
    parsed = abitreenit.parse_questions(self.polls, minimal=True)
    self.assertEqual(assertion, parsed)

  def test_parse_questions(self):
    assertion = {'millainen': {'helppo': 98, 'juuri sopiva': 369, 'melko vaativa': 349, 'ihan liian vaikea': 70, 'ei mikään edellisistä, kerro kommenteissa ↓': 45}, 'arvosanani': {'l': 81, 'e': 114, 'm': 207, 'c': 207, 'b': 81, 'a': 48, 'pääsispä edes läpi...': 36, 'en uskalla edes arvata tai toivoa mitään.': 62}, 'fiilis': {'voittajafiilis!': 60, 'positiivisesti yllättynyt.': 195, 'ihan jees.': 402, 'pettynyt.': 118, 'ei mikään edellisistä, kerro kommenteissa ↓': 31}, 'valmistautuminen': {'huolellisesti, aloitin jo hyvissä ajoin.': 158, 'ihan hyvin.': 251, 'viime tippaan jäi.': 149, 'huonosti.': 77, 'en mitenkään.': 76}}
    parsed = abitreenit.parse_questions(self.polls)
    self.assertEqual(assertion, parsed)

  def test_calculate_relative_scores(self):
    input = {'millainen': {1: 98, 2: 369, 3: 349, 4: 70, 5: 45}, 'arvosanani': {1: 81, 2: 114, 3: 207, 4: 207, 5: 81, 6: 48, 7: 36, 8: 62}, 'fiilis': {1: 60, 2: 195, 3: 402, 4: 118, 5: 31}, 'valmistautuminen': {1: 158, 2: 251, 3: 149, 4: 77, 5: 76}} 
    relative = abitreenit.calculate_relative_scores(input)
    assertion = {'millainen': {1: 0.105, 2: 0.396, 3: 0.375, 4: 0.075, 5: 0.048}, 'arvosanani': {1: 0.097, 2: 0.136, 3: 0.248, 4: 0.248, 5: 0.097, 6: 0.057, 7: 0.043, 8: 0.074}, 'fiilis': {1: 0.074, 2: 0.242, 3: 0.499, 4: 0.146, 5: 0.038}, 'valmistautuminen': {1: 0.222, 2: 0.353, 3: 0.21, 4: 0.108, 5: 0.107}}
    self.assertEqual(assertion, relative)

class TestPolls(unittest.TestCase):

  polls = {'Millainen maantieteen koe mielestäsi oli?\n': {'Helppo': 98, 'Juuri sopiva': 369, 'Melko vaativa': 349, 'Ihan liian vaikea': 70, 'Ei mikään edellisistä, kerro kommenteissa ↓': 45}, 'Uskon saavani arvosanakseni...\n': {'L': 81, 'E': 114, 'M': 207, 'C': 207, 'B': 81, 'A': 48, 'Pääsispä edes läpi...': 36, 'En uskalla edes arvata tai toivoa mitään.': 62}, 'Mikä on päällimmäinen fiilis?\n': {'Voittajafiilis!': 60, 'Positiivisesti yllättynyt.': 195, 'Ihan jees.': 402, 'Pettynyt.': 118, 'Ei mikään edellisistä, kerro kommenteissa ↓': 31}, 'Olin valmistautunut maantieteen kokeeseen...\n': {'Huolellisesti, aloitin jo hyvissä ajoin.': 158, 'Ihan hyvin.': 251, 'Viime tippaan jäi.': 149, 'Huonosti.': 77, 'En mitenkään.': 76}}

  def test_get_polls(self):
    test_polls = abitreenit.get_polls("MA", "2022K")
    self.assertIsNotNone(test_polls)
    self.assertEqual(test_polls, self.polls)

if __name__ == '__main__':
  unittest.main()
