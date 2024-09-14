import pandas as pd
from pymongo.collection import Collection

polishAreaFileName = 'Areas.xlsx'
voivodeshipColName = 'voivodeships'
powiatyColName = 'powiaty'
gminyColName = 'gminy'
citiesColName = 'cities'

translatorsFileName = 'Translators.xlsx'
translatorsColName = 'translators'

def createDropCollection(mydb, collectionName):
  if collectionName in mydb.list_collection_names():
    mydb[collectionName].drop()
  else:
    mydb.create_collection(collectionName)

def returnObjectIdFromCollectionByName(nameToFind, collection: Collection):
  object = collection.find_one({'name': nameToFind.replace('[a]', '').replace('m.st. ', '').strip().lower()})
  if (object == None): raise Exception("there is no such object as " + nameToFind + " in " + collection.name) 
  
  return str(object['_id'])

def returnDictAndHeadersFromDf(fileName, collectionName):
  df = pd.read_excel(fileName, collectionName)
  dfDict = df.to_dict(orient='records')
  headers = list(df.columns)
  return dfDict, headers

def cleanStringToFloat(word):
  if isinstance(word, int): return word
  return float(word.replace(',', '.').replace(' ', '').strip())

def returnDict(self): 
  return {key:value for key, value in self.__dict__.items() if not key.startswith('__') and not callable(key)}
