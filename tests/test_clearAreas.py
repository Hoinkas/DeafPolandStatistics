from src.functions.clearAreas import clearAreas, returnDBAreasAsDict

class TestClass:
  data = [{'input': 'Częstochowa ', 'output': 'Częstochowa ', 'length': 1}]

  def test(self):
    for d in self.data:
      assert clearAreas(d['input'], d['length']) == d['output']