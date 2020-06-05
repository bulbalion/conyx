from os import listdir, sep, path
import re
import sys

def ls(path,fext):
  f = []
  for fname in listdir(path):
    f.append(path+sep+fname)
  f.sort()
  return(f)

#print(ls('.','py'))
