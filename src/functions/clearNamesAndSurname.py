def clearNamesAndSurname(namesAndSurname):
  clearedNamesAndSurname = namesAndSurname.replace(',', '').replace(' – ','-').strip()
  listedNames = clearedNamesAndSurname.split(' ')

  if (len(listedNames) == 2): return [listedNames[0]], listedNames[1]
  return [listedNames[0], listedNames[1]], listedNames[2]