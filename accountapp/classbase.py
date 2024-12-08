import os, json


class GlobalJson:
  var1 = 'var1'
  def __init__(self, filename):
    self.filename = filename
    if os.path.isfile(self.filename):
      f = open(self.filename)
      array_data = json.load(f)

      dbc = ""
      section={}
      i=0
      for m in array_data.keys():
        if i==0:
          dbc='"'+f'{m}'+'"'+f':{m}'
          i+=1
        else:
          dbc+=','+'"'+f'{m}'+'"'+f':{m}'
          i+=1

      dbc='{'+dbc+'}'
      self.var1 =dbc