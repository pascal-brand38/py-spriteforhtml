# MIT License
#
# Copyright (c) 2023 Pascal Brand

from PIL import Image

import os
import json
import shutil
#import math


# TODO: check the sprite does not overlap in some icons

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
  iconsKeys = json_db['icons'].keys()

  sprite_width = 0
  sprite_height = 0
  images = []

  for iconKey in iconsKeys:
    desc = json_db['icons'][iconKey]
    name = getFullFilename(desc['filename'], rootDirIcons)

    pos_w = int(desc['posHor'])
    pos_h = int(desc['posVer'])
    i = Image.open(name)
    if sprite_width < pos_w + i.width:
      sprite_width = pos_w + i.width
    if sprite_height < pos_h + i.height:
      sprite_height = pos_h + i.height
    images.append(i)

  # if sprite_width % 8 != 0:
  #   sprite_width = math.floor(sprite_width / 8) * 8 + 8
  # if sprite_height % 8 != 0:
  #   sprite_height = math.floor(sprite_height / 8) * 8 + 8
    
  sprite = Image.new(
    mode='RGBA',
    size=(sprite_width, sprite_height),
    color=(0,0,0,0))  # fully transparent

  index = 0
  for iconKey in iconsKeys:
    i = images[index]

    desc = json_db['icons'][iconKey]
    name = desc['filename']
    pos_w = int(desc['posHor'])
    pos_h = int(desc['posVer'])

    sprite.paste(i, (pos_w, pos_h))
    pseudo = desc.get('pseudo', '')

    cssString += iconKey + pseudo + ' {'                                                \
      + ' background-position: -' + str(desc['posHor']) + 'px -' + str(desc['posVer']) + 'px;'       \
      + ' width: ' + str(i.width) + 'px;'                                                            \
      + ' height: ' + str(i.height) + 'px;'                                                          \
      + ' }\n'
    
    if cssAllClasses != '':
      cssAllClasses += ',\n'
    cssAllClasses += iconKey + pseudo

    index = index + 1
  
  cssAdds = json_db.get('cssAdds')
  if cssAdds is not None:
    cssAllClasses += '{\n'
    for s in cssAdds:
      cssAllClasses += '  ' + s + ';\n'
    cssAllClasses += '}\n'
    cssString += '\n' + cssAllClasses

  spriteOutputBaseName = getFullFilename(json_db['spriteOutputBaseName'], rootDirIcons)
  png_result = spriteOutputBaseName + '.png'
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
  webp_result = spriteOutputBaseName + '.webp'
  print('Save ' +  webp_result)
  sprite.save(webp_result, method=6, quality=100, lossless=True)

  # save css file, or print on the console
  cssFilename = json_db.get('cssOutputFilename')
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
# root directory of the sprite json description file
def getFullFilename(filename, root):
  if (os.path.isabs(filename)):
    return filename
  else:
    return root + '/' + filename
