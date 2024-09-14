import pymongo
from DeafPolandStatistics.importExcelToCollections import *

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["DeafStatistics"]

# Check if the collection exists, create it if it doesn't, delete if it does

from DeafPolandStatistics.helpers import *

# insertDataFromExcel(polishAreaFileName, mydb, voivodeshipColName)
# insertDataFromExcel(polishAreaFileName, mydb, powiatyColName)
# insertDataFromExcel(polishAreaFileName, mydb, gminyColName)
# insertDataFromExcel(polishAreaFileName, mydb, citiesColName)
insertTranslatorsDataFromExcel(translatorsFileName, mydb, translatorsColName)