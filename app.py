import pymongo, os
from src.importExcelToCollections import *

os.environ['MONGO_URI'] = 'mongodb://localhost:27017'

myclient = pymongo.MongoClient(os.environ['MONGO_URI'])
mydb = myclient["DeafStatistics"]

# Check if the collection exists, create it if it doesn't, delete if it does

from src.helpers import *

fixedPolishAreaFileName = mapExcelFilePath(polishAreaFileName)
fixedTranslatorsFileName = mapExcelFilePath(translatorsFileName)

# insertDataFromExcel(fixedPolishAreaFileName, mydb, voivodeshipColName)
# insertDataFromExcel(fixedPolishAreaFileName, mydb, powiatyColName, voivodeshipColName)
# insertDataFromExcel(fixedPolishAreaFileName, mydb, gminyColName, powiatyColName)
# insertDataFromExcel(fixedPolishAreaFileName, mydb, citiesColName, powiatyColName)
# for g in list(mydb[gminyColName].find()):
#   print(g)

symbol = '.' # Previous symbol to fasten the process of cleaning the date
insertTranslatorsDataFromExcel(fixedTranslatorsFileName, mydb, translatorsColName, symbol)