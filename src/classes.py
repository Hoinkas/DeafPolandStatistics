from .helpers import *
import datetime

class Translator():
  def __init__(self):
    self.names = []
    self.surname = ''
    self.phone = ''
    self.email = ''
    self.dataOfEntry = datetime.datetime.now()
    self.certificate = ''
    self.voivodeships_ids = []
    self.powiaty_ids = []
    self.gminy_ids = []
    self.cities_ids = []
    self.expiryDate = datetime.datetime.now()
    self.sources_ids = []
    self.levels_ids = []

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
  def __init__(self, name, powiat_id, areaKm2, population):
    self.name = name.strip().lower()
    self.powiat_id = powiat_id
    self.areaKm2 = areaKm2
    self.population = population