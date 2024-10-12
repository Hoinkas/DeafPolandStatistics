import re
from enums import Areas
from helpers import voivodeshipColName, powiatyColName, gminyColName, citiesColName

def clearAreas(areas, areasFromDBDict, counter, mydb):
  areasList = re.sub('[^A-Za-z0-9ęąśłżźćńó -]+', ' ', areas.lower())
  areasList = areasList.split(' ')
  areasList = list(filter(None, areasList))
  areasList = mergeTwoNamesCities(areasList, mydb)

  areasDict = returnAreasDict(areasList, areasFromDBDict)
  filteredAreasDict = returnFilteredAreasDict(areasDict)

  if (int(counter) == len(filteredAreasDict)): return filteredAreasDict
  else:
    print('-------------------')
    print(areasList)
    for e in areasDict: print(e['main'], returnNameFromId(e, mydb), e)
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

def mergeTwoNamesCities(areasList, mydb):
  listOfTwoPartNames = returnTwoPartNamesFromWholeDB(mydb)
  # listOfTwoPartNames = ['tarnowskie góry', 'dąbrowa górnicza', 'ruda śląska', 'piekary śląskie', 'sokołów podlaski', 'jastrzębie-zdrój']
  listOfAdditional = ['gminy', 'miasto', 'powiat', 'województwo', 'woj.', 'm', 'st', 'pow', 'miasta']
  listOfChanged = [{'from': 'jastrzębski', 'to': 'jastrzębie-zdrój'}, {'from': 'śląsk', 'to': 'śląskie'}, {'from': 'kraj', 'to': 'polska'}]

  for city in listOfTwoPartNames:
    if city[0] in areasList and city[1] in areasList:
      areasList.remove(city[0])
      areasList.remove(city[1])
      areasList.append(city)

  for city in listOfAdditional:
    if city in areasList:
      areasList.remove(city)

  for city in listOfChanged:
    if city['from'] in areasList:
      areasList.remove(city['from'])
      areasList.append(city['to'])

  return areasList

def returnTwoPartNamesFromWholeDB(mydb):
  listOfPartNames = []
  listOfColNames = [citiesColName, gminyColName, powiatyColName, voivodeshipColName]

  for n in listOfColNames:
    foundElements = list(mydb[n].find({"name": {'$regex': "[ -]"}}))

    for element in foundElements:
      name = element['name']

      if ' ' in name: listOfPartNames.append(name.split(' '))
      if '-' in name: listOfPartNames.append(name.split('-'))

  return listOfPartNames