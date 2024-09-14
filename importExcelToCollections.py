from classes import *
from pymongo.database import Database
from helpers import *

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

def insertDataFromExcel(fileName, mydb: Database, collectionName, collectionToFind = None):
  createDropCollection(mydb, collectionName)
  dfDict, headers = returnDictAndHeadersFromDf(fileName, collectionName)

  if collectionToFind != None:
    parentCollection = mydb[collectionToFind]
    for v in dfDict:
      v[headers[3]] = returnObjectIdFromCollectionByName(v[headers[3], parentCollection])
  
  dictList = [mapFunction(collectionName, v, headers).dict() for v in dfDict]
  mydb[collectionName].insert_many(dictList)