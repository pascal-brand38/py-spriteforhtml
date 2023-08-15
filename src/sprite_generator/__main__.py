# __main__.py

import sys, os
from sprite_generator import create

def main():
  argv = sys.argv
  if len(argv) == 1:
    spriteJsonFilename = os.path.dirname(__file__) + '/data/sprite.json'
  else:
     spriteJsonFilename = argv[1]

  create.create_sprites(spriteJsonFilename)

if __name__ == "__main__":
    main()
