import time

def uts2str(unix_timestamp):
  ret=time.strftime("%d.%m.%Y %H:%M", time.localtime(int(unix_timestamp)))
  return(ret)
