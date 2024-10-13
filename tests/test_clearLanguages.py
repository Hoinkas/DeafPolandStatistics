from src.functions.clearLanguages import clearLanguages

class TestClass:
  symbol = '-'
  data = [{'input': 'PJM – zaawansowany SJM – zaawansowany SKOGN – poziom podstawowy ', 'output': [{'language': 'PJM', 'level': 'zaawansowany'}, {'language': 'SJM', 'level': 'zaawansowany'}, {'language': 'SKOGN', 'level': 'podstawowy'}]},
          {'input': 'PJM - zaawansowany SJM - zaawansowany', 'output': [{'language': 'PJM', 'level': 'zaawansowany'}, {'language': 'SJM', 'level': 'zaawansowany'}]},
          {'input': 'SJM  -  zaawansowany  ', 'output': [{'language': 'SJM', 'level': 'zaawansowany'}]},
          {'input': 'SJM - poziom zaawansowany', 'output': [{'language': 'SJM', 'level': 'zaawansowany'}]},
          {'input': 'SJM – średnio-zaawansowany, SKOGN - zaawansowany', 'output': [{'language': 'SJM', 'level': 'średnio zaawansowany'}, {'language': 'SKOGN', 'level': 'zaawansowany'}]}]

  def test(self):
    for d in self.data:
      assert clearLanguages(d['input']) == d['output']