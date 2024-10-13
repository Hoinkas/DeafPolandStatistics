import datetime
from src.functions.clearDate import clearDate

class TestClass:
  symbol = '-'
  data = [{'input': '2012-07-20', 'output': datetime.date(2012, 7, 20)},
          {'input': '16.07.2012r.', 'output': datetime.date(2012, 7, 16)},
          {'input': '18.02.2022 r.', 'output': datetime.date(2022, 2, 18)},
          {'input': '03/16/2023', 'output': datetime.date(2023, 3, 16)},
          {'input': '12.12.2019', 'output': datetime.date(2019, 12, 12)}]

  def test(self):
    for d in self.data:
      assert clearDate(d['input'], self.symbol) == d['output']