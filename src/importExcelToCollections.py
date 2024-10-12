from classes import City, Gmina, Powiat, Translator, Voivodeship
from pymongo.database import Database
from functions.clearDate import clearDate
from functions.clearNamesAndSurname import clearNamesAndSurname
from functions.clearLanguages import clearLanguages
from functions.clearAreas import clearAreas, returnDBAreasAsDict
from helpers import createDropCollection, returnDictAndHeadersFromDf, returnObjectIdFromCollectionByName, voivodeshipColName, powiatyColName, gminyColName, citiesColName
import pandas as pd

def mapFunction(collectionName, v, headers):
  name = v[headers[0]]
  area = v[headers[1]]
  population = v[headers[2]]

  if collectionName == voivodeshipColName:
    return Voivodeship(name, area, population)
  
  else:
    parent_id = v[headers[3]]

    if collectionName == powiatyColName:
      return Powiat(name, parent_id, area, population)
    elif collectionName == gminyColName:
      return Gmina(name, parent_id, area, population)
    elif collectionName == citiesColName:
      return City(name, parent_id, area, population)
    
def continueClause(v, headers):
  if (pd.isnull(v[headers[1]])): return True
  elif (isinstance(v[headers[1]], str) and 'wykreślon' in v[headers[1]]): return True
  elif (isinstance(v[headers[2]], str) and 'wykreślon' in v[headers[2]]): return True
  elif (pd.isnull(v[headers[5]])): return True
  elif (isinstance(v[headers[5]], str) and 'wykreślen' in v[headers[5]]): return True
  elif (pd.isnull(v[headers[8]])): return True
  else: return False

def insertDataFromExcel(fileName, mydb: Database, collectionName, collectionToFind = None):
  createDropCollection(mydb, collectionName)
  dfDict, headers = returnDictAndHeadersFromDf(fileName, collectionName)

  if collectionToFind != None:
    parentCollection = mydb[collectionToFind]
    for v in dfDict: v[headers[3]] = returnObjectIdFromCollectionByName(v[headers[3]], parentCollection)
  
  dictList = [mapFunction(collectionName, v, headers).dict() for v in dfDict]
  mydb[collectionName].insert_many(dictList)

def insertTranslatorsDataFromExcel(fileName, mydb: Database, collectionName, symbol):
  createDropCollection(mydb, collectionName)
  dfDict, headers = returnDictAndHeadersFromDf(fileName, collectionName)
  areasFromDBDict = returnDBAreasAsDict(mydb)

  for v in dfDict:
    if continueClause(v, headers): continue

    transl = Translator()
    transl.dataOfEntry = clearDate(v[headers[1]], symbol)
    transl.names, transl.surname = clearNamesAndSurname(v[headers[2]])
    transl.phone = v[headers[3]]
    transl.email = v[headers[4]]
    transl.levels_ids = clearLanguages(v[headers[5]])
    clearAreas(v[headers[6]], areasFromDBDict, v[headers[8]], mydb)
  
  # dictList = [mapFunction(collectionName, v, headers).dict() for v in dfDict]
  # mydb[collectionName].insert_many(dictList)