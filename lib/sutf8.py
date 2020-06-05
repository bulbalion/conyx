import sys

def sutf8(string):
  try:
    if sys.version_info.major >= 3:
      return(string)
    else:
      return(string.encode('utf8'))
  except Exception as e:
    pass

