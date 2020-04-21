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
# version 0.1.0
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

import curses
import locale
import sys
import functools

def tuiScrollContent(filename, filecontent, encoding="utf-8"):
  try:
    global stdscr
    stdscr = curses.initscr()
    curses.noecho()
    curses.cbreak()
    curses.curs_set(0)
    stdscr.keypad(1)
    rows, columns = stdscr.getmaxyx()
    stdscr.border()
    bottom_menu = "CONYX " + filename # u"(n) Next line | (p) Previous line | (n) Next page | (p) Previous page | (q) Quit".encode(encoding).center(columns - 4)
    stdscr.addstr(rows - 1, 2, bottom_menu, curses.A_REVERSE)
    out = stdscr.subwin(rows - 2, columns - 2, 1, 1)
    out_rows, out_columns = out.getmaxyx()
    out_rows -= 1
    #lines = map(lambda x: x + " " * (out_columns - len(x)), reduce(lambda x, y: x + y, [[x[i:i+out_columns] for i in xrange(0, len(x), out_columns)] for x in filecontent.expandtabs(4).splitlines()])) # Python2
    lines = list(map(lambda x: x + " " * (out_columns - len(x)), functools.reduce(lambda x, y: x + y, [[x[i:i+out_columns] for i in range(0, len(x), out_columns)] for x in filecontent.expandtabs(4).splitlines()]))) # v0.1.9
    stdscr.refresh()
    line = 0
    while 1:
      top_menu = (u"Lines %d to %d of %d of %s" % (line + 1, min(len(lines), line + out_rows), len(lines), filename)).encode(encoding).center(columns - 4) 
      stdscr.addstr(0, 2, top_menu, curses.A_REVERSE)
      out.addstr(0, 0, "".join(lines[line:line+out_rows]))
      stdscr.refresh()
      out.refresh()
      c = stdscr.getch()
      if c == ord("q"):
        stdscr.clear()
        stdscr.refresh()
        break
      elif c == curses.KEY_DOWN or c == ord("j"):
        if len(lines) - line > out_rows:
          line += 1
      elif c == curses.KEY_UP or c == ord("k"):
        if line > 0:
          line -= 1
      elif c == curses.KEY_RIGHT:
        if len(lines) - line >= 2 * out_rows:
          line += out_rows
      elif c == curses.KEY_LEFT:
        if line >= out_rows:
          line -= out_rows
  finally:
    #curses.nocbreak(); stdscr.keypad(0); curses.echo(); curses.curs_set(1)
    curses.endwin()

def readFile(filename):
  file = open(filename, "r")
  lines = file.readlines()
  str = '' 
  for i in range(len(lines)):
    str += lines[i] + ' '
  return(str)

def ScrollableWindow(filename):
  encoding = locale.getpreferredencoding()
  tuiScrollContent(filename,readFile(filename), encoding)

def tuiFile(filename):
  #locale.setlocale(locale.LC_ALL, '')
  ScrollableWindow(filename)

#tuiFile('tuiFile.py')
