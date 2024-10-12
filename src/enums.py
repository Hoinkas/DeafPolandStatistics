from enum import Enum

class Langauages(Enum):
  PJM = 'PJM'
  SJM = 'SJM'
  SKOGN = 'SKOGN'

class Levels(Enum):
  Podstawowy = 'podstawowy'
  Średnio_zaawansowany = 'średnio zaawansowany'
  Zaawansowany = 'zaawansowany'

class Areas(Enum):
  Voivodeship = 'voivodeship'
  Powiat = 'powiat'
  Gmina = 'gmina'
  City = 'city'