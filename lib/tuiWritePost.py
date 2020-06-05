import sys, os, traceback
if ('CONYX') in os.environ:
  sys.path.insert(0, (os.environ['CONYX']+'/lib'))
import curses
from curses.textpad import Textbox, rectangle
from inputBox import inputBox
from ugetch import ugetch
from nyx_send_message import nyx_send_message
from sutf8 import sutf8

def tuiWritePost(stdscr,width,height,tui_klub_id):
  try:
    stdscr.refresh()
    curses.cbreak()
    stdscr.addstr(0,3,"Tvuj prispevek: [ alt+1 napoveda sl ]")
    footer="-=[ klavesy: CTRL+G (odesli), CTRL+X (zrus), ALT+1 ]=-" 
    if len(footer)>=width-1:
      footer="-=[ ^G, ^X, ALT+1 ]=-" 
    stdscr.addstr(height-1,0,footer)
    height, width = stdscr.getmaxyx()
    x=2;y=2;h=height-y;w=width-x;
    rectangle(stdscr,y-1,x-1,h,w)
    editwin = curses.newwin(h-1-1,w-2,y,x)
    stdscr.refresh()
    box=inputBox(editwin)
    text=box.edit(None,"YES")
    try:
      if (text!=""): 
        curses.nocbreak()
        orig_text=text
        tmp=orig_text.strip().split('\n')
        text=""
        for i in tmp:
          text+=i
          if (len(i)!=width-4):
            text+='\n'
        if (nyx_send_message(tui_klub_id,text)==0):
          stdscr.addstr(0, 0, " "*width)
          stdscr.addstr(0, 0, "*** Prispevek odeslan do klubu: " + sutf8(str(tui_klub_id)))
        else:
          stdscr.addstr(0, 0, " "*width)
          stdscr.addstr(0, 0, "!   Chyba pri odesilani prispevku do klubu")
        #stdscr.getch()
        ugetch(stdscr)
        curses.cbreak()
    except Exception:
      stdscr.addstr(0, 0, "Nepodarilo se odeslat prispevek")
      traceback.print_exc(file=sys.stdout)
      ugetch(stdscr)
    stdscr.refresh()
    stdscr.clear()
  except Exception:
    traceback.print_exc(file=sys.stdout)
    input("Zmackni Enter ...")
    print("Problem pri ziskani cisla klubu.")



