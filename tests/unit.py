"""
MIT License
Copyright (c) 2023 Pascal Brand

Unit testing
"""

import filecmp
import tempfile
import platform
from spriteforhtml import create

def _cmp_lines(path_1, path_2):
  l1 = l2 = True
  with open(path_1, 'r', encoding='utf-8') as f1, open(path_2, 'r', encoding='utf-8') as f2:
    while l1 and l2:
      l1 = f1.readline()
      l2 = f2.readline()
      if l1 != l2:
        return False
  return True

def test_fromjson():
  """
  Test using a json file
  """
  refdir = 'src/spriteforhtml/data/'
  if platform.system() == "Windows":
    resdir = tempfile.gettempdir() + '/'
  else:
    resdir = '/tmp/'
  create.create_sprites('src/spriteforhtml/data/sprite.json')

  # compare text files, not bothering about endofline which is different on
  # linux and windows
  for file in [ 'sprite.css' ]:
    # fname = refdir+file
    # with open(fname, 'r') as fin:
    #   print(fin.read())

    # fname = resdir+file
    # with open(fname, 'r') as fin:
    #   print(fin.read())
    assert _cmp_lines(refdir+file, resdir+file), f"{file}"


  # compare binary files
  if platform.system() == "Windows":
    listSprites = [ 'sprite.webp', ]    # on windows, png are not the same
  else:
    listSprites = [ 'sprite.webp', 'sprite.png', ]
  for file in listSprites:
    assert (filecmp.cmp(refdir+file, resdir+file, shallow=True) or filecmp.cmp(refdir+'2-'+file, resdir+file, shallow=True)), f"{file}"
