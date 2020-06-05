# encoding=utf-8
from youtube_search import YoutubeSearch
import sys
import json
import sys

import curses
actual_char='>'
import sys, os, traceback
from sutf8 import sutf8

def ytb_search(term,width,height):
  res = YoutubeSearch(term, max_results=height-1).to_json()
  res_dict=json.loads(res)
  strings=[]
  for i in res_dict["videos"]:
    #if len(i["link"])<=10:
    strings.append((i["title"][:width-5].ljust(width-5),"https://youtube.com"+i["link"]))
  return(strings)

def hlp_ytb_dialog(strings=""):
  screen = curses.initscr()
  curses.start_color()
  curses.noecho()
  row_num = len(strings)
  height,width=screen.getmaxyx()
  row_num = len(strings)
  height,width=screen.getmaxyx()
  curses.init_pair(1,curses.COLOR_BLACK,curses.COLOR_CYAN)
  hiTe=curses.color_pair(1)
  noTe=curses.A_NORMAL
  max_row=height-3
  box=curses.newwin(max_row-1,width-4,2,2)
  screen.refresh()
  box.refresh()

  x = None 
  page=0
  shift=0
  position=0
  while x != ord('q'): # dokud neni stisknuta klavesa 'q'
    if x==curses.KEY_DOWN or x==ord('j'):
      if (position%max_row<max_row-1 and position<row_num-1): 
        position=position+1
    elif x == ord('s'):
      y=None
      term=""
      while y!=ord('\n'):
        box.addstr(0,0,(" "*(width-6)))
        box.addstr(0,0,"Term: "+str(term))
        screen.refresh()
        box.refresh()
        y=screen.getch()
        if y in (curses.KEY_BACKSPACE,263,127):
          term=term[:-1]
        else:
          term+=chr(y)
      if (len(term)>0):
        term=term[:-1]
      strings=ytb_search(term,width,max_row)
      row_num = len(strings)
      box.refresh()
      screen.refresh()
    elif x == curses.KEY_UP or x==ord('k'):
      if (position%max_row>0 and position>0): position = position - 1
    elif x == ord("\n"):
      #box.erase()
      #box.addstr(0,0,"Selected: "+str(strings[position][0]))
      #box.addstr(1,0,"Link: "+str(strings[position][1]))
      #box.refresh()
      #screen.refresh()
      return(strings[position][1])
  
    box.erase()

    for i in range(0,max_row):
      if row_num == 0:
        box.addstr(0,1,"[s] pro vyhledani na YTB",hiTe)
      elif i+shift==row_num:
        break
      else:
        if (i+shift==position):
          box.addstr(i,2,actual_char+" "+sutf8(strings[i+shift][0][:width-10]), hiTe)
        else:
          box.addstr(i,2,"  "+sutf8(strings[i+shift][0][:width-10]),noTe)
  
    footer="[ Klavesy: j,k,s,q,ENTER shift: "+str(shift) + " i: " + str(i) + " pos: " + str(position)
    if height <= 50:
      footer="[ Klavesy: j,k,s,q,ENTER ]"
    box.addstr(max_row-2,0,footer,noTe)
    screen.refresh()
    box.refresh()
    x = screen.getch()

# DEBUG
#res=hlp_ytb_dialog("")
#curses.endwin()
#print(res)

