import filecmp
import tempfile
import platform
from spriteforhtml import create

def cmp_lines(path_1, path_2):
  l1 = l2 = True
  with open(path_1, 'r') as f1, open(path_2, 'r') as f2:
    while l1 and l2:
      l1 = f1.readline()
      l2 = f2.readline()
      if l1 != l2:
        return False
  return True

def test_fromjson():
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
    assert cmp_lines(refdir+file, resdir+file), f"{file}"


  # compare binary files
  if platform.system() == "Windows":
    listSprites = [ 'sprite.webp', ]    # on windows, png are not the same
  else:
    listSprites = [ 'sprite.webp', 'sprite.png', ]
  for file in listSprites:
    assert filecmp.cmp(refdir+file, resdir+file, shallow=True), f"{file}"
