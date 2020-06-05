#!/usr/bin/python3
from youtube_search import YoutubeSearch
import sys
import json
import sys

def ytb_search(term):
  res = YoutubeSearch(term, max_results=10).to_json()
  return(res)

if __name__ == "__main__":
   search_qry=None
   if len(sys.argv)<2:
     search_qry=input("Vlozte retezec pro vyhledavani: ")
   else:
     search_qry=sys.argv[1]
   res=ytb_search(search_qry)
   res_dict=json.loads(res)
   for i in res_dict["videos"]:
     if len(i["link"])<=21:
       print(i["title"][:28].ljust(28)+"| "+"https://youtube.com"+i["link"])
