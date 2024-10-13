from src.functions.clearNamesAndSurname import clearNamesAndSurname

class TestClass:
  data = [{'input': 'Anna Regina Irasiak', 'output': (['Anna', 'Regina'], 'Irasiak')},
          {'input': 'Adam, Franciszek Pilecki ', 'output': (['Adam', 'Franciszek'], 'Pilecki')},
          {'input': 'Karolina Kurek ', 'output': (['Karolina'], 'Kurek')},
          {'input': 'Monika Inglot – Werner', 'output': (['Monika'], 'Inglot-Werner')},
          {'input': 'Edyta, Janina Lala – Koczy  ', 'output': (['Edyta', 'Janina'], 'Lala-Koczy')}]

  def test(self):
    for d in self.data:
      assert clearNamesAndSurname(d['input']) == d['output']