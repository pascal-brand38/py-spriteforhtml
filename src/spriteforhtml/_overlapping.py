"""
MIT License
Copyright (c) 2023 Pascal Brand

Check subimages placement are overlapping or not, using the API checkOverlapping(subimages),
where subimages is an array of object having the properties
- 'posHor': horizontal position of the top-left corner of the image
  Can be None if not placed yet. In such case, this subimage is not considered
- 'posVer': vertical position
- 'pil': the opened image, by pil. Properties 'width' and 'height' are used
- 'filename': the filename of the sub-image
"""

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

def checkOverlapping(subimages):
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
