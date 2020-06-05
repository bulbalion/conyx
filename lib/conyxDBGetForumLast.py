from conyxDBQuery import conyxDBQuery

def conyxDBGetForumLast():
  cols , rows = conyxDBQuery('select id from current')
  return(str(rows[0][0]))

