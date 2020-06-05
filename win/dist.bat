rem set PATH=%PATH%;c:\mingw\mingw64\bin
rem nuitka --show-progress --standalone --recurse-all tui.py
copy tui.py conyx.py
pyinstaller --onefile conyx.py
copy dist\conyx.exe c:\conyx.v.0.2.3.win\
