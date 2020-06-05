import curses
import locale
import sys

locale.setlocale(locale.LC_ALL, '')    # set your locale

scr = curses.initscr()
scr.clear()
scr.addstr(0, 0, u'\u3042'.encode('utf-8'))
if (sys.version_info[0] < 3):
  ch=scr.getch()
else:
  ch=scr.get_wch()
scr.refresh()
curses.endwin()
