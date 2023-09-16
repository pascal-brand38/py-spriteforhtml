# MIT License
# Copyright (c) 2023 Pascal Brand

'''
To be called with
  python -m spriteforhtml ...


if no arguments, same as
  python -m spriteforhtml <dirofmain>/data/sprite.json
'''

import sys
import os
import argparse
from spriteforhtml import create


def createParser():
  parser = argparse.ArgumentParser(
     prog='spriteforhtml',
     description='Creation of png and webp sprite to be used in html ',
     formatter_class=argparse.RawTextHelpFormatter
     )
  parser.add_argument('--json', 
                      help='json file describing the sprite to create.\nIf provided, the other options are not considered', 
                      required=False)
  parser.add_argument('--spriteFilename', 
                      help='Required when no json is provided.\nPopulate spriteFilename property', 
                      required=False)
  parser.add_argument('--subimages', nargs='*', 
                      help='Required when no json is provided.\nPopulate all subimages filename', 
                      required=False)
  parser.add_argument('--cssSelectorPrefix', 
                      help='Populate cssSelectorPrefix property', 
                      required=False)
  parser.add_argument('--strategy', 
                      help='Populate strategy property', 
                      required=False)
  parser.add_argument('--cssFilename', 
                      help='Populate cssFilename property', 
                      required=False)
  parser.add_argument('--cssCommon', 
                      help='Populate cssCommon property', 
                      required=False)
  parser.add_argument('--cssPseudo', 
                      help='Populate cssPseudo property of all subimages', 
                      required=False)
  
  return parser

def main():
  parser = createParser()
  args = parser.parse_args()

  print('parser = ', args)
  
  argv = sys.argv
  if len(argv) == 1:
    create.create_sprites(os.path.dirname(__file__) + '/data/sprite.json')
  elif args.json is not None:
    create.create_sprites(args.json)
  else:
    json_db = {}
    mylist = [  
      [ 'cssSelectorPrefix', args.cssSelectorPrefix ],
      [ 'spriteFilename', args.spriteFilename ],
      [ 'strategy', args.strategy ],
      [ 'cssFilename', args.cssFilename ],
    ]
    for item in mylist:
      if item[1] is not None:
        json_db[item[0]] = item[1]
    json_db['subimages'] = []
    for sub in args.subimages:
      if args.cssPseudo is not None:
        json_db['subimages'].append( { "filename": sub, "cssPseudo": args.cssPseudo })
      else:
        json_db['subimages'].append( { "filename": sub })

    if args.cssCommon is not None:
      json_db['cssCommon'] = [ args.cssCommon ]

    print(json_db)
    create.create_from_memory(json_db)

if __name__ == "__main__":
  main()
