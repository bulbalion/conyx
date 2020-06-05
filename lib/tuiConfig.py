# encoding=utf-8
#   ____ ___  _   ___   ____  __
#  / ___/ _ \| \ | \ \ / /\ \/ /
# | |  | | | |  \| |\ V /  \  /
# | |__| |_| | |\  | | |   /  \
#  \____\___/|_| \_| |_|  /_/\_\
#
# Console Nyx Client
#
# Conyx Text User Interface Main Menu Library
#
# version 0.2.3
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
# + Added configuration of Conyx colorization 
#

import curses
import sys, os, traceback
import locale
import sys
import re
if ('CONYX') in os.environ:
  sys.path.insert(0, (os.environ['CONYX']+'/lib'))

from conyxDBQuery import conyxDBQuery
from conyxOps import *
from conyxDBLast import conyxDBLast
from ugetch import ugetch

def getConfig(key):
  cols,rows=conyxDBQuery('select value from config where key = "%s"' % key)
  return(rows)

def updateConfig(key, value):
  conyxDBGenDML('update config set value = "%s" where key="%s"' % (value, key,))

def tuiConfig():
  screen = curses.initscr()
  height,width=screen.getmaxyx()
  tmp=[] 
  curses.noecho()
  curses.cbreak()
  curses.start_color()
  screen.keypad(1)
  curses.init_pair(1,curses.COLOR_BLACK,curses.COLOR_CYAN)
  highlightText=curses.color_pair(1)
  normalText=curses.A_NORMAL
  max_row=height-2
  x=0
  while x!=ord("q"):
    box=curses.newwin(max_row+2,width,0,0)
    box.addstr(0,0,"*** KONFIGURACE ***", highlightText )
    box.addstr(height-1,0,"-=[ klavesy 0-4 ]=-", highlightText )
    cols,rows=conyxDBQuery("select key, description, value from config order by rowid asc")

    nlen=0
    rn=0
    for i in rows:
      if (len(str(i[1])) > nlen): nlen = len(str(i[1]))
      box.addstr(rn+2,0,"["+str(rn)+"] "+str(i[1])+" ")
      rn+=1
    rn=0
    for i in rows:
      if (i[0]=="rodicovsky_zamek"):
        if (i[2]=="1"):
          box.addstr(rn+2,nlen+5," -> " + "Zapnuty")
        else:
          box.addstr(rn+2,nlen+5," -> " + "Vypnuty")
      elif (i[0]=="rodicovsky_zamek_heslo"):
        box.addstr(rn+2,nlen+5," -> " + (len(str(i[2]))*"*"))
      else:
        box.addstr(rn+2,nlen+5," -> "+str(i[2]))

      rn+=1

    #if (x==ord("0")):
    #  if (rows[0][2]=="0"):
    #    conyxDBGenDML('update config set value = "1" where key="rodicovsky_zamek"')
    #  if (rows[0][2]=="1"):
    #    conyxDBGenDML('update config set value = "0" where key="rodicovsky_zamek"')
    #  box.addstr(height-2,0,"*** PROVEDENA ZMENA *** "+str(rows[0][2]), highlightText )

    if (x==ord("0")):
      pass_prompt="*** ZADEJ HESLO: " 
      box.addstr(height-2,0,pass_prompt)
      input_pass=""
      input_pass_display=""
      screen.refresh()
      box.refresh()
      while x!=ord('\n'):
        #x = screen.getch()
        x = ugetch(screen)
        if ((x>=ord("a") and x<=ord("Z")) or (x>=ord("0") and x<=ord("9"))):
          input_pass+=chr(x)
          input_pass_display+="*"
          box.addstr(height-2,0,pass_prompt+input_pass_display)
          screen.refresh()
          box.refresh()
        input_pass=input_pass.strip()
      if (input_pass==rows[1][2]):
        box.addstr(height-4,0,"ZADANO HESLO SOUHLASI, MENIM STAV ZAMKU...")
        if (rows[0][2]=="0"):
          conyxDBGenDML('update config set value = "1" where key="rodicovsky_zamek"')
          box.addstr(height-2,0,"*** RODICOVSKY ZAMEK ZAPNUT *** ", highlightText )
        if (rows[0][2]=="1"):
          conyxDBGenDML('update config set value = "0" where key="rodicovsky_zamek"')
          box.addstr(height-2,0,"*** RODICOVSKY ZAMEK VYPNUT *** ", highlightText )
      else:
        box.addstr(height-4,0,"ZADANO HESLO NESOUHLASI.")

    if (x==ord("2")):
      pass_prompt="*** ZADEJ HESLO: " 
      club_prompt="ZADEJ SCHVALENY KLUB: "
      box.addstr(height-2,0,pass_prompt)
      input_pass=""
      input_pass_display=""
      allowed_club=""
      screen.refresh()
      box.refresh()
      while x!=ord('\n'):
        #x = screen.getch()
        x = ugetch(screen)
        if ((x>=ord("a") and x<=ord("Z")) or (x>=ord("0") and x<=ord("9"))):
          input_pass+=chr(x)
          input_pass_display+="*"
          box.addstr(height-2,0,pass_prompt+input_pass_display)
          screen.refresh()
          box.refresh()
        input_pass=input_pass.strip()
      if (input_pass==rows[1][2]):
        box.addstr(height-4,0,club_prompt)
        screen.refresh()
        box.refresh()
        x=0
        while x!=ord('\n'):
          #x = screen.getch()
          x = ugetch(screen)
          if ((x>=ord("0") and x<=ord("9"))):
            allowed_club+=chr(x)
            box.addstr(height-4,0,club_prompt+allowed_club)
            screen.refresh()
            box.refresh()
        allowed_club=allowed_club.strip()
        conyxDBGenDML('update config set value = "%s" where key="rodicovsky_zamek_klub"' % allowed_club)
        box.addstr(height-2,0,"*** RODIC SCHVALIL KLUB *** "+str(allowed_club), highlightText )
        conyxDBLast(allowed_club)
      else:
        box.addstr(height-4,0,"ZADANO HESLO NESOUHLASI")
  
    if (x==ord("3")):
      rows=getConfig("barvicky")
      colors_allowed_comment=""
      if (rows[0][0]=='A'):
        colors_allowed_comment="NE"
        colors_allowed='N'
      else:
        colors_allowed_comment="ANO"
        colors_allowed='A'
      updateConfig("barvicky",colors_allowed)
      box.addstr(height-3,0,"UPRAVENA KONFIGURACE ZOBRAZENI BAREV NA %s" % colors_allowed_comment)

    if (x==ord("4")):
      upload_prompt="ZADEJ ZDROJOVY ADRESAR PRO ODESILANE SOUBORY: "
      rows=getConfig("soubory")
      upload_dir=str(getConfig('soubory')[0][0])
      box.addstr(height-4,0,upload_prompt+" "+upload_dir)
      screen.refresh()
      box.refresh()
      x=0
      while x!=ord('\n'):
        x = ugetch(screen)
        if x in (curses.KEY_BACKSPACE,263,127):
          if len(upload_dir)>0: upload_dir=upload_dir[:-1]
          box.addstr(height-4,0,upload_prompt+(" "*(width-1)))
          box.addstr(height-4,0,upload_prompt+" "+upload_dir)
        else:
          upload_dir+=chr(x)
        box.addstr(height-4,0,upload_prompt+" "+upload_dir)
        screen.refresh()
        box.refresh()
      upload_dir=upload_dir.strip()
      conyxDBGenDML('update config set value = "%s" where key="soubory"' % upload_dir)
      box.addstr(height-2,0,"*** NASTAVEN ADRESAR PRO ODESILANE SOUBORY *** "+str(upload_dir), highlightText )
       
    screen.refresh()
    box.refresh()
    x = screen.getch()
  
  curses.endwin()

