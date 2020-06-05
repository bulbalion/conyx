# encoding=utf-8
import curses
import locale
import sys

locale.setlocale(locale.LC_ALL, '')    # set your locale

#scr = curses.initscr()
#scr.clear()
#scr.addstr(0, 0, u'\u3042'.encode('utf-8'))
# get char from curses screen
# when on Python3 it accepts wide chars
# when on Python2 it accepts only ASCII chars
def ugetch(scr):
  try:
    ch=None
    if (sys.version_info[0] < 3):
      ch=scr.getch()
    else:
      ch=scr.get_wch()
    ord(ch)
    return(ord(ch))
  except Exception as e:
    return(ch) 
