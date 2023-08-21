# MIT License
#
# Copyright (c) 2023 Pascal Brand

from PIL import Image

import os
import json
import shutil


# TODO: check the sprite does not overlap in some icons
# TODO: auto-position the sprite

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

  requiredKeys = [ 'filename', 'posHor', 'posVer', 'cssSelector']
  for subimage in subimages:
    for key in requiredKeys:
      if subimage.get(key) is None:
        _error('Error in spriteforhtml.create.create_sprites: in "subimages", property ' + key + ' is required')

  if json_db.get('spriteFilename') is None:
    _error('Error in spriteforhtml.create.create_sprites: property "spriteFilename" is missing')


def _openSubimages(json_db, rootDir):
  for subimage in json_db['subimages']:
    name = _getFullFilename(subimage['filename'], rootDir)
    i = Image.open(name)
    subimage['pil'] = i

def create_sprites(spriteJsonFilename):
  try:
    with open(spriteJsonFilename, encoding='utf-8') as file:
      json_db = json.load(file)
  except Exception as err:
    print(err)
    _error('Error in spriteforhtml.create.create_sprites when opening ' + spriteJsonFilename)

  rootDir = os.path.dirname(spriteJsonFilename)
  _checkJson(json_db)
  _openSubimages(json_db, rootDir)

  cssString = '/* Generated using python package spriteforhtml */\n\n'
  cssAllClasses = ''

  sprite_width = 0
  sprite_height = 0

  for subimage in json_db['subimages']:
    pos_w = int(subimage['posHor'])
    pos_h = int(subimage['posVer'])
    w = subimage['pil'].width
    h = subimage['pil'].height
    if sprite_width < pos_w + w:
      sprite_width = pos_w + w
    if sprite_height < pos_h + h:
      sprite_height = pos_h + h

  sprite = Image.new(
    mode='RGBA',
    size=(sprite_width, sprite_height),
    color=(0,0,0,0))  # fully transparent

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

