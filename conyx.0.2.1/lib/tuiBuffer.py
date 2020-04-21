# encoding=utf-8
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
# version 0.2.0
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

import sys, os, traceback
import sys, os, traceback
# reload(sys)
# sys.setdefaultencoding('utf8')
sys.path.insert(0, (os.environ['CONYX']+'/lib'))
import curses
import locale
import re
#from conyxDBQuery import conyxDBQuery
#from conyxOps import *
#from tuiBuffer import *

def sutf8(string):
  if sys.version_info.major >= 3:
    return(string)
  else:
    return(string.encode('utf8'))

def cleanHtml(text):
  cleanr = re.compile('<.*?>')
  cleantext = re.sub(cleanr,'', text)
  cleantext=cleantext.replace('\n',' ')
  cleantext=cleantext.replace('\r',' ')
  return(cleantext)

def tuiScrollContent(filename,lines):
  try:
    screen=curses.initscr()
    rows,columns=screen.getmaxyx()
    curses.noecho()
    curses.cbreak()
    curses.curs_set(0)
    screen.keypad(1)
    screen.clear()
    screen.refresh()
    clean=[]
    for i in lines:
      clean.append(cleanHtml(i))
    buffer=[]
    #print(clean)
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
      screen.refresh()
      try:
        for y in range(0,rows-1,1):
          buff_row=y+shift
          scr_row=y
          if (buff_row<len(buffer) and buff_row>0):
            screen.addstr(scr_row,0,sutf8(buffer[buff_row]))
            #screen.addstr(scr_row,0,str(buff_row) + '/' + str(len(buffer)))
      except:
        print("ERROR: " + "BUFF_ROW: " + str(y) + " SCR_ROW: " + str(scr_row))
      if c == curses.KEY_DOWN or c==ord("j"):
        if shift<len(buffer)-rows+1: 
          shift+=1
      elif c==ord("h"):
        shift=0
      elif c == curses.KEY_UP or c==ord("k"):
        if shift>0: shift-=1 
      elif c == curses.KEY_PPAGE or c==ord("u"):
        if shift-rows>0: 
          shift-=rows 
        else: 
          shift=0
      elif c == curses.KEY_NPAGE or c==ord("n"):
        if shift<rows-len(buffer)+1: 
          shift+=rows 
        else:
          shift=len(buffer)-rows+1
      elif c == ord("o"): # O - cti od prispevku
        curses.endwin()
        screen.refresh()
        c = screen.getch()
        return(-1)
        #res=conyxDBQuery('select min(id_prispevek) prid from prispevek_cache')
        #print(res)
        #zobrazDiskuzi(str(tui_klub_id),stdscr,1,res[1][0][0])
        #stdscr.clear()      

      screen.refresh()
      c = screen.getch()
  finally:
    curses.endwin()

def tuiBuffer(name,buffer):
  locale.setlocale(locale.LC_ALL, '')
  tuiScrollContent(name,buffer)
