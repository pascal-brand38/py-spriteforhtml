# MIT License
#
# Copyright (c) 2023 Pascal Brand

import os
import json
import shutil
from pathlib import Path
from PIL import Image

from ._sort import sortSubimages

def _error(e):
  raise Exception(e)


# utility function to get the full filename given a filename (absolute or relative) and the
# root directory of the sprite json desription file
def _getFullFilename(filename, root):
  if (os.path.isabs(filename)):
    return filename
  else:
    return root + '/' + filename


# checkJson
# check json structure, that is all the arguments that are mandatory
def _checkJson(json_db):
  subimages = json_db.get('subimages')
  if subimages is None:
    _error('Error in spriteforhtml.create.create_sprites: property "subimages" is missing')

  requiredKeys = [ 'filename']
  for subimage in subimages:
    for key in requiredKeys:
      if subimage.get(key) is None:
        _error('Error in spriteforhtml.create.create_sprites: in "subimages", property ' + key + ' is required')
      if subimage.get('posHor') is None and subimage.get('posVer') is not None:
        _error('Error in spriteforhtml.create.create_sprites: in "subimages", property posHor and posVer must be either both provided, either both absent')
      if subimage.get('posHor') is not None and subimage.get('posVer') is None:
        _error('Error in spriteforhtml.create.create_sprites: in "subimages", property posHor and posVer must be either both provided, either both absent')

  if json_db.get('spriteFilename') is None:
    _error('Error in spriteforhtml.create.create_sprites: property "spriteFilename" is missing')

  strategy = json_db.get('strategy')
  if strategy is not None:
    if (strategy not in [ 'auto', 'hor', 'ver', 'square']):
      _error('Error in spriteforhtml.create.create_sprites: "strategy" must be "auto", "hor", "ver" or "square"')


# Open sub images, and add them in the json_db to further usage
def _openSubimages(json_db, rootDir):
  for subimage in json_db['subimages']:
    name = _getFullFilename(subimage['filename'], rootDir)
    i = Image.open(name)
    subimage['pil'] = i

# check for subimage overlapping
def _getCoords(i):
  ax = i['posHor']
  bx = ax + i['pil'].width - 1
  ay = i['posVer']
  by = ay + i['pil'].height - 1
  return ax, bx, ay, by

def _isOutside(a1, b1, a2, b2):
  if (a2<a1) and (b2<a1):
    return True
  if (a2>b1) and (b2>b1):
    return True
  return False
  
def _checkUnitOverlapping(i1, i2):
  ax1, bx1, ay1, by1 = _getCoords(i1)
  ax2, bx2, ay2, by2 = _getCoords(i2)
  if (_isOutside(ax1, bx1, ax2, bx2)):
    return False
  if (_isOutside(ay1, by1, ay2, by2)):
    return False
  
  return True

def _checkOverlapping(subimages):
  for i1 in subimages:
    for i2 in subimages:
      # do not check the same image
      if (i1 == i2):
        continue

      # do not check if one is not placed yet
      if (i1.get('posHor') is None) or (i2.get('posHor') is None):
        continue

      if _checkUnitOverlapping(i1, i2):
        return True, 'Subimages ' + i1['filename'] + ' and ' + i2['filename'] + ' overlap'
  return False, ''



def _spriteSize(subimages):
  sprite_width = 0
  sprite_height = 0
  for subimage in subimages:
    if subimage.get('posHor') is None:
      break
    pos_w = int(subimage['posHor'])
    pos_h = int(subimage['posVer'])
    w = subimage['pil'].width
    h = subimage['pil'].height
    if sprite_width < pos_w + w:
      sprite_width = pos_w + w
    if sprite_height < pos_h + h:
      sprite_height = pos_h + h
  
  # if (sprite_width % 8 != 0):
  #   sprite_width = math.floor((sprite_width / 8) * 8) + 8
  # if (sprite_height % 8 != 0):
  #   sprite_height = math.floor((sprite_height / 8) * 8) + 8

  return sprite_width, sprite_height

def _placeScore(subimages, subimage, strategy):
  error, _ = _checkOverlapping(subimages)
  if error:
    return -1
  
  w,h = _spriteSize(subimages)

  if strategy == 'hor':
    return h*10000 + h*1000 + subimage['posHor'] + subimage['posVer']
  elif strategy == 'ver':
    return w*10000 + h*1000 + subimage['posHor'] + subimage['posVer']
  elif strategy == 'square':
    return max(w,h)*10000 + subimage['posHor'] + subimage['posVer']
  else:
    return _error('Unknown strategy ' + strategy)


def _placeSubimage(subimages, subimage, strategy):
  posHor = 0
  posVer = 0
  bestScore = -1

  for s in subimages:
    if s.get('posVer') is None:
      break

    # place it at right
    subimage['posHor'] = s['posHor'] + s['pil'].width
    subimage['posVer'] = s['posVer']
    score = _placeScore(subimages, subimage, strategy)
    if (score != -1) and ((score < bestScore) or (bestScore == -1)):
      posHor = subimage['posHor']
      posVer = subimage['posVer']
      bestScore = score

    # place it below
    subimage['posHor'] = s['posHor']
    subimage['posVer'] = s['posVer'] + s['pil'].height
    score = _placeScore(subimages, subimage, strategy)
    if (score != -1) and ((score < bestScore) or (bestScore == -1)):
      posHor = subimage['posHor']
      posVer = subimage['posVer']
      bestScore = score

  subimage['posHor'] = posHor
  subimage['posVer'] = posVer

def _setCssSelector(json_db):
  prefix = json_db.get('cssSelectorPrefix', '.')

  for subimage in json_db['subimages']:
    if subimage.get('cssSelector') is None:
      # https://stackoverflow.com/questions/678236/how-do-i-get-the-filename-without-the-extension-from-a-path-in-python
      subimage['cssSelector'] = prefix + Path(subimage['filename']).stem

def create_from_memory(json_db, rootDir='.'):
  _checkJson(json_db)
  _openSubimages(json_db, rootDir)

  error, msg = _checkOverlapping(json_db['subimages'])
  if error:
    _error(msg)

  sortSubimages(json_db)
  _setCssSelector(json_db)

  for subimage in json_db['subimages']:
    if subimage.get('posHor') is None:
      _placeSubimage(json_db['subimages'], subimage, json_db['strategy'])
  
  sprite_width, sprite_height = _spriteSize(json_db['subimages'])

  sprite = Image.new(
    mode='RGBA',
    size=(sprite_width, sprite_height),
    color=(0,0,0,0))  # fully transparent

  cssString = '/* Generated using python package spriteforhtml */\n\n'
  cssAllClasses = ''
  for subimage in json_db['subimages']:
    i = subimage['pil']
    pos_w = int(subimage['posHor'])
    pos_h = int(subimage['posVer'])

    sprite.paste(i, (pos_w, pos_h))
    pseudo = subimage.get('cssPseudo', '')

    cssString += subimage['cssSelector'] + pseudo + ' {'                                                \
      + ' background-position: -' + str(subimage['posHor']) + 'px -' + str(subimage['posVer']) + 'px;'  \
      + ' width: ' + str(i.width) + 'px;'                                                               \
      + ' height: ' + str(i.height) + 'px;'                                                             \
      + ' }\n'
    
    if cssAllClasses != '':
      cssAllClasses += ',\n'
    cssAllClasses += subimage['cssSelector'] + pseudo
  
  cssCommon = json_db.get('cssCommon')
  if cssCommon is not None:
    cssAllClasses += '{\n'
    for s in cssCommon:
      cssAllClasses += '  ' + s + ';\n'
    cssAllClasses += '}\n'
    cssString += '\n' + cssAllClasses

  spriteFilename = _getFullFilename(json_db['spriteFilename'], rootDir)
  png_result = spriteFilename + '.png'
  print('Save ' +  png_result)
  sprite.save(png_result, optimize=True)
  if (shutil.which('optipng') is not None):
    error = os.system('optipng ' + png_result)
    if error != 0:
      _error('Error in spriteforhtml.create.create_sprites related to optipng')
  else:
    print('Install optipng to get benefits of an even better optimization of .png file')


  # save as webp
  # https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html#webp
  # method=6 provides a better size, but is slow
  webp_result = spriteFilename + '.webp'
  print('Save ' +  webp_result)
  sprite.save(webp_result, method=6, quality=100, lossless=True)

  # save css file, or print on the console
  cssFilename = json_db.get('cssFilename')
  if cssFilename is None:
    print('\n=======================  copy/paste the sprite position in your favorite css file')
    print(cssString)
    print('=======================')
  else:
    cssFilename = _getFullFilename(cssFilename, rootDir)
    with open(cssFilename, 'w') as file:
      file.write(cssString)
      file.close()
    print('Save ' +  cssFilename)

def create_sprites(spriteJsonFilename):
  try:
    with open(spriteJsonFilename, encoding='utf-8') as file:
      json_db = json.load(file)
  except Exception as err:
    print(err)
    _error('Error in spriteforhtml.create.create_sprites when opening ' + spriteJsonFilename)

  rootDir = os.path.dirname(spriteJsonFilename)
  create_from_memory(json_db, rootDir)

# pylint           --indent-string='  '           --disable C0103,C0303,C0301,C0116,C0114,C0325,R1705 src/spriteforhtml/create.py
