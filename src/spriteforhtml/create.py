# MIT License
#
# Copyright (c) 2023 Pascal Brand

from PIL import Image

import os
import json
import shutil
#import math


# TODO: check the sprite does not overlap in some icons
# TODO: auto-position the sprite

def create_sprites(spriteJsonFilename):
  try:
    with open(spriteJsonFilename, encoding='utf-8') as file:
      json_db = json.load(file)
  except Exception as err:
    print(err)
    raise Exception('Error in spriteforhtml.create.create_sprites when opening ', spriteJsonFilename)
  
  cssString = '/* Generated using python package spriteforhtml */\n\n'
  cssAllClasses = ''

  rootDirIcons = os.path.dirname(spriteJsonFilename)
  subimages = json_db['subimages']

  sprite_width = 0
  sprite_height = 0
  images = []

  for subimage in subimages:
    name = getFullFilename(subimage['filename'], rootDirIcons)

    pos_w = int(subimage['posHor'])
    pos_h = int(subimage['posVer'])
    i = Image.open(name)
    if sprite_width < pos_w + i.width:
      sprite_width = pos_w + i.width
    if sprite_height < pos_h + i.height:
      sprite_height = pos_h + i.height
    images.append(i)

  sprite = Image.new(
    mode='RGBA',
    size=(sprite_width, sprite_height),
    color=(0,0,0,0))  # fully transparent

  index = 0
  for subimage in subimages:
    i = images[index]
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

    index = index + 1
  
  cssCommon = json_db.get('cssCommon')
  if cssCommon is not None:
    cssAllClasses += '{\n'
    for s in cssCommon:
      cssAllClasses += '  ' + s + ';\n'
    cssAllClasses += '}\n'
    cssString += '\n' + cssAllClasses

  spriteFilename = getFullFilename(json_db['spriteFilename'], rootDirIcons)
  png_result = spriteFilename + '.png'
  print('Save ' +  png_result)
  sprite.save(png_result, optimize=True)
  if (shutil.which('optipng') is not None):
    error = os.system('optipng ' + png_result)
    if error != 0:
      raise Exception('Error in spriteforhtml.create.create_sprites related to optipng')
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
    cssFilename = getFullFilename(cssFilename, rootDirIcons)
    with open(cssFilename, 'w') as file:
      file.write(cssString)
      file.close()
    print('Save ' +  cssFilename)



# utility function to get the full filename given a filename (absolute or relative) and the
# root directory of the sprite json desription file
def getFullFilename(filename, root):
  if (os.path.isabs(filename)):
    return filename
  else:
    return root + '/' + filename
