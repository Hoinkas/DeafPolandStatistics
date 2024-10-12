import re
from enums import Langauages, Levels

def clearLanguages(languages):
  availableLanguges = [e.value for e in Langauages]
  languagesToCheck = [o for o in availableLanguges if o in languages]

  if (len(languagesToCheck) == 1):
    firstIndex = languages.index(languagesToCheck[0])

    return [returnDictLanguageAndLevel(languages, languagesToCheck, firstIndex)]
  
  pairs = []
  for indexL in range(len(languagesToCheck)):
    firstIndex = languages.index(languagesToCheck[indexL])
    
    secondIndex = -1

    if (indexL + 1 < len(languagesToCheck)):
      secondIndex = languages.index(languagesToCheck[indexL+1])

    langLevelDict = returnDictLanguageAndLevel(languages, languagesToCheck, firstIndex, secondIndex, indexL)

    pairs.append(langLevelDict)
    
  return(pairs)
    
def clearLevel(level):
  level= re.sub(r'\s*[-–]\s*', ' ', level.strip())
  availableLevels = [e.value for e in Levels]
  level = re.sub(r'[.,;]', '', level.strip().lower()).replace('poziom ', '')

  if (level in availableLevels):
    return level
  else:
    raise Exception('Level not found')

def returnDictLanguageAndLevel(languages, languagesToCheck, firstIndex, secondIndex = -1, indexL = 0):
  level = ''
  if (secondIndex == -1):
    level = languages[firstIndex + len(languagesToCheck[indexL]) : ]
  else:
    level = languages[firstIndex + len(languagesToCheck[indexL]) : secondIndex]

  level = clearLevel(level)

  # print(languages, languagesToCheck[indexL], '|||', level)

  return {'language': languagesToCheck[indexL], 'level': level}