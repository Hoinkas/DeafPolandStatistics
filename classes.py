from helpers import *

class Translator():
  def __init__(
      self,
      name, 
      surname, 
      # dataOfEntry, 
      certificate, 
      voivodeships_ids,
      powiaty_ids,
      cities_ids,
      expiryDate,
      sources_ids,
      ):
    self.name = name
    self.surname = surname
    # self.dataOfEntry = dataOfEntry
    self.certificate = certificate
    self.voivodeships_ids = voivodeships_ids
    self.powiaty_ids = powiaty_ids
    self.cities_ids = cities_ids
    self.expiryDate = expiryDate
    self.sources_ids = sources_ids

  def dict(self):
    return returnDict(self)
  
class Voivodeship():
  def __init__(self, name, areaKm2, population):
    self.name = name.strip().lower()
    self.areaKm2 = cleanStringToFloat(areaKm2)
    self.population = cleanStringToFloat(population)

  def dict(self):
    return returnDict(self)

class Powiat(Voivodeship):
  def __init__(self, name, voivodeship_id, areaKm2, population):
    if 'powiat ' in name: self.name = name.replace('powiat ', '').strip().lower()
    else: self.name = name.strip().lower()
    self.voivodeship_id = voivodeship_id
    self.areaKm2 = cleanStringToFloat(areaKm2)
    self.population = cleanStringToFloat(population)
  
class Gmina(Voivodeship):
  def __init__(self, name, powiat_id, areaKm2, population):
    if 'gmina ' in name: self.name = name.replace('gmina ', '').strip().lower()
    else: self.name = name.strip().lower()
    self.powiat_id = powiat_id
    self.areaKm2 = cleanStringToFloat(areaKm2)
    self.population = cleanStringToFloat(population)
  
class City(Voivodeship):
  def __init__(self, name, gmina_id, areaKm2, population):
    self.name = name.strip().lower()
    self.gmina_id = gmina_id
    self.areaKm2 = areaKm2
    self.population = population