# MIT License
#
# Copyright (c) 2023 Pascal Brand

from PIL import Image

import os
import json


# TODO: check the sprite does not overlap in some icons
# TODO: save .css file instead of prints in the console

def create_sprites(spriteJsonFilename):
  try:
    with open(spriteJsonFilename, encoding='utf-8') as file:
      json_db = json.load(file)
  except Exception as err:
    print(err)
    raise Exception('Error in sprite-generator.create.create_sprites')

  rootDirIcons = os.path.dirname(spriteJsonFilename)
  iconsKeys = json_db['icons'].keys()

  sprite_width = 0
  sprite_height = 0
  images = []

  for iconKey in iconsKeys:
    desc = json_db['icons'][iconKey]
    name = desc['filename']
    if (not os.path.isabs(name)):
      name = rootDirIcons + '/' + name

    pos_w = int(desc['posHor'])
    pos_h = int(desc['posVer'])
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
  for iconKey in iconsKeys:
    i = images[index]

    desc = json_db['icons'][iconKey]
    name = desc['filename']
    pos_w = int(desc['posHor'])
    pos_h = int(desc['posVer'])

    sprite.paste(i, (pos_w, pos_h))
    spanPosition = desc.get('spanPosition', 'before')
    print(iconKey + '::' + spanPosition + ' {'
      + ' background-position: -' + str(desc['posHor']) + 'px -' + str(desc['posVer']) + 'px;'
      + ' width: ' + str(i.width) + 'px;'
      + ' height: ' + str(i.height) + 'px;'
      + ' }')
    index = index + 1
  
  spriteOutputBaseName = json_db['spriteOutputBaseName']
  if (not os.path.isabs(spriteOutputBaseName)):
    spriteOutputBaseName = rootDirIcons + '/' + spriteOutputBaseName

  png_result = spriteOutputBaseName + '.png'
  print('Save ' +  png_result)
  sprite.save(png_result, optimize=True)
  error = os.system('optipng ' + png_result)
  if error != 0:
    exit(1)

  # save as webp
  # https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html#webp
  # method=6 provides a better size, but is slow
  webp_result = spriteOutputBaseName + '.webp'
  print('Save ' +  webp_result)
  sprite.save(webp_result, method=6, quality=100, lossless=True)

  return 0    # no error
