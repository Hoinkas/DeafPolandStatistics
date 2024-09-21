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
    transl.levels_ids = clearLanguages(v[headers[5]], v)

    try:
      clearAreas(v[headers[6]], areasFromDBDict, v[headers[8]], mydb)
    except ValueError as e:
      print(e)
      continue
  
  # dictList = [mapFunction(collectionName, v, headers).dict() for v in dfDict]
  # mydb[collectionName].insert_many(dictList)

def clearDate(dateToMap, symbol):
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

def clearAreas(areas, areasFromDBDict, counter, mydb):
  areasList = re.sub('[^A-Za-z0-9ęąśłżźćńó -]+', ' ', areas.lower())
  areasList = areasList.split(' ')
  areasList = list(filter(None, areasList))
  areasList = mergeTwoNamesCities(areasList)

  areasDict = returnAreasDict(areasList, areasFromDBDict)
  filteredAreasDict = returnFilteredAreasDict(areasDict)

  if (int(counter) == len(filteredAreasDict)): return filteredAreasDict
  else:
    print('-------------------')
    print(areasList)
    for e in areasDict: print(e['main'], returnNameFromId(e, mydb))
    raise Exception(areas + ' - not all areas were found: ' + str(len(filteredAreasDict)) + ' instead of ' + str(int(counter)))

def returnDBAreasAsDict(db):
  voivodeships = db[voivodeshipColName].find()
  powiaty = db[powiatyColName].find()
  gminy = db[gminyColName].find()
  cities = db[citiesColName].find()

  areaDict = {voivodeshipColName: [{'_id': str(v['_id']), 'name': v['name']} for v in voivodeships],
              powiatyColName: [{'_id': str(p['_id']), 'name': p['name'], 'voivodeship_id': p['voivodeship_id']} for p in powiaty],
              gminyColName: [{'_id': str(g['_id']), 'name': g['name'], 'powiat_id': g['powiat_id']} for g in gminy],
              citiesColName: [{'_id': str(c['_id']), 'name': c['name'], 'powiat_id': c['powiat_id']} for c in cities]}
  
  return areaDict

def continueClause(v, headers):
  if (pd.isnull(v[headers[1]])): return True
  elif (isinstance(v[headers[1]], str) and 'wykreślon' in v[headers[1]]): return True
  elif (isinstance(v[headers[2]], str) and 'wykreślon' in v[headers[2]]): return True
  elif (pd.isnull(v[headers[5]])): return True
  elif (isinstance(v[headers[5]], str) and 'wykreślen' in v[headers[5]]): return True
  elif (pd.isnull(v[headers[8]])): return True
  else: return False

def returnDictFromArea(area, areaType, areasFromDBDict):
  if areaType == Areas.Voivodeship: 
    return {'main': Areas.Voivodeship, 'voivodeship_id': area['_id'], 'powiat_id': None, 'gmina_id': None, 'city_id': None}
  elif areaType == Areas.Powiat:
    voivodeship_id = next(v['_id'] for v in areasFromDBDict[voivodeshipColName] if v['_id'] == area['voivodeship_id'])
    return {'main': Areas.Powiat, 'voivodeship_id': voivodeship_id, 'powiat_id': area['_id'], 'gmina_id': None, 'city_id': None}
  elif areaType == Areas.Gmina:
    voivodeship_id = next(p['voivodeship_id'] for p in areasFromDBDict[powiatyColName] if p['_id'] == area['powiat_id'])
    return {'main': Areas.Gmina, 'voivodeship_id': voivodeship_id, 'powiat_id': area['powiat_id'], 'gmina_id': area['_id'], 'city_id': None}
  elif areaType == Areas.City:
    voivodeship_id = next(p['voivodeship_id'] for p in areasFromDBDict[powiatyColName] if p['_id'] == area['powiat_id'])
    return {'main': Areas.City, 'voivodeship_id': voivodeship_id, 'powiat_id': area['powiat_id'], 'gmina_id': None, 'city_id': area['_id']}
  else: TypeError('No such area type')

def returnNameFromId(area, mydb):
  type = area['main']
  id = ''
  collection = None

  if type == Areas.Voivodeship:
    id = area['voivodeship_id']
    collection = mydb[voivodeshipColName].find()
  elif type == Areas.Powiat:
    id = area['powiat_id']
    collection = mydb[powiatyColName].find()
  elif type == Areas.Gmina:
    id = area['gmina_id']
    collection = mydb[gminyColName].find()
  elif type == Areas.City:
    id = area['city_id']
    collection = mydb[citiesColName].find()

  return next(v['name'] for v in collection if str(v['_id']) == id)

def returnAreasDict(areasList, areasFromDBDict):
  areasDict = []

  for area in areasList:
    voivodeship = next((v for v in areasFromDBDict[voivodeshipColName] if area == v['name']), None)
    print(area, voivodeship)
    if voivodeship: 
      findAnyMention = next((a for a in areasDict if a['voivodeship_id'] == voivodeship['_id']), None)
      if findAnyMention: continue

      areasDict.append(returnDictFromArea(voivodeship, Areas.Voivodeship, areasFromDBDict))
      continue

    if area == 'jastrzębski': area = 'jastrzębie-zdrój'
    powiat = next((p for p in areasFromDBDict[powiatyColName] if area == p['name']), None)
    # print(area, powiat)
    if powiat:
      findAnyMention = next((a for a in areasDict if a['powiat_id'] == powiat['_id']), None)
      if findAnyMention: continue

      areasDict.append(returnDictFromArea(powiat, Areas.Powiat, areasFromDBDict))
      continue

    gmina = next((g for g in areasFromDBDict[gminyColName] if area == g['name']), None)
    # print(area, gmina)
    if gmina:
      findAnyMention = next((a for a in areasDict if a['gmina_id'] == gmina['_id']), None)
      if findAnyMention: continue
      
      areasDict.append(returnDictFromArea(gmina, Areas.Gmina, areasFromDBDict))
      continue

    city = next((c for c in areasFromDBDict[citiesColName] if area == c['name']), None)
    # print(area, city)
    if city:
      findAnyMention = next((a for a in areasDict if a['city_id'] == city['_id']), None)
      if findAnyMention: continue
      
      areasDict.append(returnDictFromArea(city, Areas.City, areasFromDBDict))
      continue

  return areasDict

def returnFilteredAreasDict(areasDict):
  filteredAreasDict = []
  areasDictSecond = areasDict.copy()

  for area in areasDict:
    areasDictSecond.remove(area)
    
    if area['main'] == Areas.Voivodeship:
      findAnyMention = next((a for a in areasDictSecond if a['voivodeship_id'] == area['voivodeship_id']), None)
      if not findAnyMention: filteredAreasDict.append(area)
    elif area['main'] == Areas.Powiat:
      findAnyMention = next((a for a in areasDictSecond if a['powiat_id'] == area['powiat_id']), None)
      if not findAnyMention: filteredAreasDict.append(area)
    elif area['main'] == Areas.Gmina:
      findAnyMention = next((a for a in areasDictSecond if a['gmina_id'] == area['gmina_id']), None)
      if not findAnyMention: filteredAreasDict.append(area)
    elif area['main'] == Areas.City:
      findAnyMention = next((a for a in areasDictSecond if a['city_id'] == area['city_id']), None)
      if not findAnyMention: filteredAreasDict.append(area)

  return filteredAreasDict

def mergeTwoNamesCities(areasList):
  listOfMerged = ['tarnowskie góry', 'dąbrowa górnicza', 'ruda śląska', 'piekary śląskie', 'sokołów podlaski']
  listOfErrored = ['jastrzębie-zdrój']
  listOfAdditional = ['gminy', 'miasto', 'powiat', 'województwo', 'woj.', 'm', 'st', 'pow', 'miasta']
  listOfChanged = [{'from': 'jastrzębski', 'to': 'jastrzębie-zdrój'}, {'from': 'śląsk', 'to': 'śląskie'}, {'from': 'kraj', 'to': 'polska'}]

  for city in listOfMerged:
    splittedCity = city.split(' ')
    if splittedCity[0] in areasList and splittedCity[1] in areasList:
      areasList.remove(splittedCity[0])
      areasList.remove(splittedCity[1])
      areasList.append(city)

  for city in listOfErrored:
    splittedCity = city.split('-')
    if splittedCity[0] in areasList and splittedCity[1] in areasList:
      areasList.remove(splittedCity[0])
      areasList.remove(splittedCity[1])
      areasList.append(city)

  for city in listOfAdditional:
    if city in areasList:
      areasList.remove(city)

  for city in listOfChanged:
    if city['from'] in areasList:
      areasList.remove(city['from'])
      areasList.append(city['to'])

  return areasList