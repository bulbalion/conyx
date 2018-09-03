#   ____ ___  _   ___   ____  __
#  / ___/ _ \| \ | \ \ / /\ \/ /
# | |  | | | |  \| |\ V /  \  /
# | |__| |_| | |\  | | |   /  \
#  \____\___/|_| \_| |_|  /_/\_\
#
# Console Nyx Client
#
# Conyx Database Library
#
# version 0.1.6
#
# You can do whatever You want with Conyx.
# But I don't take reponsbility nor even
# implied responsibility for the harm,
# damage, loss or anything negative
# You cause using Conyx.
#
# There is no service provided. The program
# is AS-IS and there is ABSOLUTELY no warranty
# provided.
#

# encoding=utf-8

import sys, os, traceback
import sys, os, traceback
reload(sys)
sys.setdefaultencoding('utf8')
sys.path.insert(0, (os.environ['CONYX']+'/lib'))
import curses
import locale
import re

def cleanHtml(text):
  cleanr = re.compile('<.*?>')
  cleantext = re.sub(cleanr,'', text)
  cleantext=cleantext.replace('\n','')
  cleantext=cleantext.replace('\r','')
  return cleantext


def tuiScrollContent(filename,lines):
  try:
    screen=curses.initscr()
    rows,columns=screen.getmaxyx()
    curses.noecho()
    curses.cbreak()
    curses.curs_set(0)
    screen.keypad(1)
    clean=[]
    for i in lines:
      clean.append(cleanHtml(i))
    buffer=[]
    for j in clean:
      if len(j)>columns:
        for i in range(0,len(j),columns):
          buffer.append(j[i:i+columns])
      else:
        buffer.append(j)
    c=""
    shift=len(buffer)-rows+1
    while c!=ord("q"):
      screen.clear()
      for y in range(0,rows-1):
        screen.addstr(y,0,buffer[y+shift])
      if c == curses.KEY_DOWN:
        if shift<=len(buffer)-rows: shift+=1
      elif c == curses.KEY_UP:
        if shift>0: shift-=1 
      screen.refresh()
      c = screen.getch()
  finally:
    curses.endwin()

def tuiBuffer(name,buffer):
  locale.setlocale(locale.LC_ALL, '')
  tuiScrollContent(name,buffer)
