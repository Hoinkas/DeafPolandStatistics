from classes import *
from pymongo.database import Database
from helpers import *
import datetime
import pandas as pd
import re
from enums import *

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
      v[headers[3]] = returnObjectIdFromCollectionByName(v[headers[3]], parentCollection)
  
  dictList = [mapFunction(collectionName, v, headers).dict() for v in dfDict]
  mydb[collectionName].insert_many(dictList)

def insertTranslatorsDataFromExcel(fileName, mydb: Database, collectionName):
  createDropCollection(mydb, collectionName)
  dfDict, headers = returnDictAndHeadersFromDf(fileName, collectionName)

  for v in dfDict:
    if (pd.isnull(v[headers[1]])): continue
    elif (isinstance(v[headers[1]], str) and 'wykreślon' in v[headers[1]]): continue
    elif (isinstance(v[headers[2]], str) and 'wykreślon' in v[headers[2]]): continue
    elif (pd.isnull(v[headers[5]])): continue
    elif (isinstance(v[headers[5]], str) and 'wykreślen' in v[headers[5]]): continue

    transl = Translator()
    transl.dataOfEntry = clearDate(v[headers[1]])
    transl.names, transl.surname = clearNamesAndSurname(v[headers[2]])
    transl.phone = v[headers[3]]
    transl.email = v[headers[4]]
    transl.levels_ids = clearLanguages(v[headers[5]], v)
    clearAreas(v[headers[6]])
  
  # dictList = [mapFunction(collectionName, v, headers).dict() for v in dfDict]
  # mydb[collectionName].insert_many(dictList)

symbol = '' # Previous symbol to fasten the process of clearing the date
def clearDate(dateToMap):
  if (isinstance(dateToMap, datetime.datetime)): return dateToMap

  clearedDate = dateToMap.replace('r.', '').replace(' ', '').strip()
  if symbol not in clearedDate: symbol = next(obj for obj in clearedDate if not obj.isdigit())
  date = clearedDate.split(symbol)

  return datetime.date(int(date[2]), int(date[1]), int(date[0]))

def clearNamesAndSurname(namesAndSurname):
  clearedNamesAndSurname = namesAndSurname.replace(',', '').strip()
  listedNames = clearedNamesAndSurname.split(' ')

  if (len(listedNames) == 2): return [listedNames[0]], listedNames[1]
  return [listedNames[0], listedNames[1]], listedNames[2]

def clearLanguages(languages, v):
  availableLanguges = [e.value for e in Langauages]
  languagesToCheck = [o for o in availableLanguges if o in languages]

  if (len(languagesToCheck) == 1):
    firstIndex = languages.index(languagesToCheck[0])
    
    return returnDictLanguageAndLevel(languages, languagesToCheck, firstIndex)
  
  pairs = []
  for indexL in range(len(languagesToCheck) - 1):
    firstIndex = languages.index(languagesToCheck[indexL])
    secondIndex = languages.index(languagesToCheck[indexL+1])
    langLevelDict = returnDictLanguageAndLevel(languages, languagesToCheck, firstIndex, secondIndex, indexL)

    pairs.append(langLevelDict)
    
  return(pairs)
    
def clearLevel(level):
  availableLevels = [e.value for e in Levels]
  level = re.sub(r'[.,;]', '', level.strip().lower()).replace('poziom ', '')

  return next(l for l in availableLevels if level in availableLevels)

def returnDictLanguageAndLevel(languages, languagesToCheck, firstIndex, secondIndex = -1, indexL = 0):
  level = ''
  if (secondIndex == -1):
    level = languages[firstIndex + len(languagesToCheck[indexL]) : ]
  else:
    level = languages[firstIndex + len(languagesToCheck[indexL]) : secondIndex]
  level= re.sub(r'\s*[-–]\s*', ' ', level.strip())
  level = clearLevel(level)

  return {'langauge': languages[indexL], 'level': level}

def clearAreas(areas):
  print(areas)