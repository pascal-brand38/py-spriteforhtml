# MIT License
# Copyright (c) 2023 Pascal Brand
#
# Sort subimages list
# - the one that have posHor are placed before
# - depending on the strategy,
#   - 'auto':
#       updated in 'hor' if the largest dimension of all subimages is its height
#               in 'ver otherwise
#   - 'hor': the taller subimages first, then the wider
#   - 'ver': the wider subimages first, then the taller
#   - 'square': the bigger (number of pixels) ones first

import functools

def _compare(i1, i2):
  if i1.get('posHor') is not None:
    if i2.get('posHor') is not None:
      return 0, None, None, None, None    # i1 and i2 can be interchanged
    else:
      return -1, None, None, None, None   # i1 is before i2

  if i2.get('posHor') is not None:
    return +1, None, None, None, None   # i2 is before i1

  w1, h1 = i1['pil'].size
  w2, h2 = i2['pil'].size
  return None, w1, h1, w2, h2

def _compareHor(i1, i2):
  r, w1, h1, w2, h2 = _compare(i1, i2)
  if r is not None:
    return r
  if (h1 > h2):
    return -1
  if (h1 < h2):
    return +1
  return w2 - w1

def _compareVer(i1, i2):
  r, w1, h1, w2, h2 = _compare(i1, i2)
  if r is not None:
    return r
  if (w1 > w2):
    return -1
  if (w1 < w2):
    return +1
  return h2 - h1

def _compareSquare(i1, i2):
  r, w1, h1, w2, h2 = _compare(i1, i2)
  if r is not None:
    return r
  return w2*h2 - w1*h1

# Calling
def sortSubimages(json_db):
  _setStrategy(json_db)
  cmp = None
  if json_db['strategy'] == 'hor':
    cmp = _compareHor
  elif json_db['strategy'] == 'ver':
    cmp = _compareVer
  elif json_db['strategy'] == 'square':
    cmp = _compareSquare
  json_db['subimages'].sort(key=functools.cmp_to_key(cmp))


def _setStrategy(json_db):
  if json_db.get('strategy') is None:
    json_db['strategy'] = 'auto'
  if json_db['strategy'] == 'auto':
    w = -1
    h = -1
    for subimage in json_db['subimages']:
      w1, h1 = subimage['pil'].size
      w = max(w, w1)
      h = max(h, h1)
      if (w < h):
        json_db['strategy'] = 'hor'
      else:
        json_db['strategy'] = 'ver'
