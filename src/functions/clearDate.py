import datetime

def clearDate(dateToMap, symbol):
  if (isinstance(dateToMap, datetime.datetime)): return dateToMap

  clearedDate = dateToMap.replace('r.', '').replace(' ', '').strip()
  if symbol not in clearedDate: symbol = next(obj for obj in clearedDate if not obj.isdigit())
  date = clearedDate.split(symbol)

  if (symbol == '-'): return datetime.date(int(date[0]), int(date[1]), int(date[2]))
  elif (symbol == '/'): return datetime.date(int(date[2]), int(date[0]), int(date[1]))
  else: return datetime.date(int(date[2]), int(date[1]), int(date[0]))