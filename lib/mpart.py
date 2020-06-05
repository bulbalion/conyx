boundary = 'DiZiZbndrY'

def guessMimeType(fname_type):
  mime_type='application/octet-stream'
  fname_atoms=fname_type.split('.')
  fext=fname_atoms[:-1]
  if (fext=='png'):
    mime_type='image/png'
  elif (fext=='gif'):
    mime_type='image/gif'
  elif (fext=='bmp'):
    mime_type='image/bmp'
  elif (fext=='ico'):
    mime_type='image/ico'
  elif (fext=='jpg' or fext == 'jpeg'):
    mime_type='image/jpg'
  elif (fext == 'svg'):
    mime_type='image/svg+xml'
  elif (fext == 'tiff'):
    mime_type='image/tiff'
  elif (fext=='zip'):
    mime_type='application/zip'
  elif (fext=='gzip'):
    mime_type='application/gzip'
  elif (fext=='ttf'):
    mime_type='font/ttf'
  elif (fext=='otf'):
    mime_type='font/otf'
  elif (fext=='pdf'):
    mime_type='application/pdf'
  elif (fext=='mp3'):
    mime_type='audio/mpeg'
  elif (fext=='ogg'):
    mime_type='audio/ogg'
  elif (fext=='midi'):
    mime_type='audio/midi'
  elif (fext=='mpeg'):
    mime_type='video/mpeg'
  elif (fext=='txt'):
    mime_type='text/plain'
  elif (fext=='css'):
    mime_type='text/css'
  elif (fext=='csv'):
    mime_type='text/csv'
  elif (fext=='html' or fext=='htm'):
    mime_type='text/html'
  elif (fext=='js'):
    mime_type='text/javascript'
  elif (fext=='json'):
    mime_type='application/json'
  return(mime_type)
   
def mpart(auth_nick, token, p_disc_key, p_message, p_attachment):
  import base64
  newline = '\r\n'
  s_attachment=""
  if not (p_attachment is None):
    print("Ctu prilohu")
    f = open(p_attachment, "rb")
    s_attachment=f.read()
    f.close()
    mime_type=guessMimeType(p_attachment)
  body = newline \
  + '--' + boundary + newline \
  + 'Content-Disposition: form-data; name="auth_nick"' + newline \
  + newline \
  + auth_nick + newline \
  + '--' + boundary + newline \
  + 'Content-Disposition: form-data; name="auth_token"' + newline \
  + newline \
  + token + newline \
  + '--' + boundary + newline \
  + 'Content-Disposition: form-data; name="id"' + newline \
  + newline \
  + str(p_disc_key) + newline \
  + '--' + boundary + newline \
  + 'Content-Disposition: form-data; name="l"' + newline \
  + newline \
  + 'discussion' + newline \
  + '--' + boundary + newline \
  + 'Content-Disposition: form-data; name="l2"' + newline \
  + newline \
  + 'send' + newline \
  + '--' + boundary + newline \
  + 'Content-Disposition: form-data; name="message"' + newline \
  + newline \

  if (type(p_message)==list):
    body += ' '.join(p_message) + newline
  else:
    body += p_message + newline

  separator = '--' + boundary + newline
  footer = newline + '--' + boundary + '--'

  res=None
  if (p_attachment):
    attach_header= 'Content-Disposition: form-data; name="attachment"; filename="'+p_attachment+'"' + newline \
    + 'Content-Type: '+mime_type+ newline \
    + newline
    res=body.encode('utf8')+\
        separator.encode('utf8')+\
        attach_header.encode('utf8')+\
        s_attachment+\
        footer.encode('utf8') 
  else:
    res=body.encode('utf8')+footer.encode('utf8') 
  return(res)

