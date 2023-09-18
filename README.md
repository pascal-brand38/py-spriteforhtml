<p>
  <a
    href="https://github.com/pascal-brand38/py-spriteforhtml/actions/workflows/pylint.yml">
    <img 
      alt="GitHub Actions build status (Lint)"
      src="https://github.com/pascal-brand38/py-spriteforhtml/actions/workflows/pylint.yml/badge.svg"
    >
  </a>
  <a
    href="https://github.com/pascal-brand38/py-spriteforhtml/actions/workflows/python-app.yml">
    <img 
      alt="GitHub Actions build status (Pytest)"
      src="https://github.com/pascal-brand38/py-spriteforhtml/actions/workflows/python-app.yml/badge.svg"
    >
  </a>

  <a
    href="https://pypi.org/project/spriteforhtml/">
    <img
      alt="Newest PyPI version"
      src="https://img.shields.io/pypi/v/spriteforhtml.svg">
  </a>
  <a href="https://pypi.org/project/spriteforhtml/">
  <img
      alt="Number of PyPI downloads"
      src="https://img.shields.io/pypi/dm/spriteforhtml.svg"></a>
</p>


# Introduction

**spriteforhtml** is a python package aimed at building a sprite from small images.
The sprite is created as a png and a webp image.

Typically, from single small images
![](https://raw.githubusercontent.com/pascal-brand38/py-spriteforhtml/main/src/spriteforhtml/data/english.png) and
![](https://raw.githubusercontent.com/pascal-brand38/py-spriteforhtml/main/src/spriteforhtml/data/france.png) and
![](https://raw.githubusercontent.com/pascal-brand38/py-spriteforhtml/main/src/spriteforhtml/data/facebook.png) and
![](https://raw.githubusercontent.com/pascal-brand38/py-spriteforhtml/main/src/spriteforhtml/data/youtube.png) and
![](https://raw.githubusercontent.com/pascal-brand38/py-spriteforhtml/main/src/spriteforhtml/data/play_20x20.png),
spriteforhtml will create the following bigger image (the sprite), that contains all small image (in 2 versions: the png one, and the webp one):

<p align="center">
  <img src="https://raw.githubusercontent.com/pascal-brand38/py-spriteforhtml/main/src/spriteforhtml/data/sprite.png" />
</p>


as well as a .css file, that used by the html to display a small image from the sprite. Typically, it includes:

```
  #english-id {
    background-position: -0px -32px;
    width: 32px;
    height: 32px;
  }
  #english-id {
    content: "";
    display: inline-block;
    vertical-align: middle;
    background-image:url(sprite.png);
  }
```

It is then rather easy to display the english flag in html, using for example:
```
  <p>
    <span id="english-id">  </span>
    English flag, as a css id
  </p>

```

For more information about sprites and their benefits, here is a link selection:

* [mdn web docs](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_images/Implementing_image_sprites_in_CSS)
* [w3schools](https://www.w3schools.com/css/css_image_sprites.asp)
* [GTMetrix](https://gtmetrix.com/combine-images-using-css-sprites.html)


# Usage

## Installation

Run ```python -m pip install spriteforhtlm``` to install the python package.

Also, please install the optional binary ```optipng``` 
(using apt-get, pacman, or directly from
[sourceforge](https://optipng.sourceforge.net/))
to further optimize the png version of the sprite.

## Demo

Running ```python -m spriteforhtml``` runs a demo based on the file at https://github.com/pascal-brand38/py-spriteforhtml/tree/main/src/spriteforhtml/data:

* [sprite.json](https://github.com/pascal-brand38/py-spriteforhtml/tree/main/src/spriteforhtml/data/sprite.json):
describe the small images to use in the sprite, their
position, and what the .css file will contain (css
classes, pseudo,...). This json file is the default
argument of ```python -m spriteforhtml```, but you
will use your own json file.

* the small images, as png file

and it will result

* [sprite.png](https://github.com/pascal-brand38/py-spriteforhtml/tree/main/src/spriteforhtml/data/sprite.png) and 
[sprite.webp](https://github.com/pascal-brand38/py-spriteforhtml/tree/main/src/spriteforhtml/data/sprite.webp),
the resulting sprite images

* [sprite.css](https://github.com/pascal-brand38/py-spriteforhtml/tree/main/src/spriteforhtml/data/sprite.css),
the css to be used in your html file. As an example,
[page.html](https://github.com/pascal-brand38/py-spriteforhtml/tree/main/src/spriteforhtml/data/page.html) uses it.

In this demo, the outputs are created in the tmp rootdir (as specified in sprite.json). But a copy of them is in  https://github.com/pascal-brand38/py-spriteforhtml/tree/main/src/spriteforhtml/data




## Generating my sprite

### Command and API
There are different ways to generate a sprite and css file:
* Using the command line with subimages as arguments, such as
```
  python -m spriteforhtml \
    --subimages english.png facebook.png france.png play_20x20.png youtube.png \
    --spriteFilename=tmp/sprite
```
* Using the command line providing a json file
```
  python -m spriteforhtml -json <mysprite.json>
```
* Using the API, as a json object as aurgument
```
  from spriteforhtml.create import create_from_memory
  create_from_memory('<jsonObject>')
```
* Using the API, as a json object as aurgument:
```
  from spriteforhtml.create import create_sprites
  create_sprites('<mysprite.json>')
```

### Json file structure
The json object providing the description of the sprite to create
contain all kind of information:
sub images name, position in sprite (optional),
css class to generate (optional), filenames of the resulting
sprite, filename of the runsulting css file (optional),...

Do not hesitate to check 
[the one of the demo](https://github.com/pascal-brand38/py-spriteforhtml/tree/main/src/spriteforhtml/data/sprite.json).

<br />
Note that in the following, when a path or a filename is considered, there are 2 different cases to take care:

* an absolute path
* a relative path: it is then relative to the
  location of json file ```<mysprite.json>``` when provided

<br />
The properties of the json are:

#### ```"subimages"``` (mandatory)
A list of objects describing all the sub images to be used in the sprite.
Each sub image is made of a json object containing the following properties:
* ```"filename"``` (mandatory):
  the name of the subimage, is mandatory
* ```"posHor"``` (optional): its horizontal position in the sprite.
  When missing, the best position, according to the
  chosen strategy (see below), is found.
* ```"posVer"```  (optional): its vertical position in the sprite.
  Note that either both posHor and posVer are provided,
  or they are both missing
* ```"cssSelector"```  (optional):
  the css selector to use it in html. 
  It can be a class (starting with a .),
  an id (starting with a #),...
  If not present, the css selector name will be the global
  ```cssSelectorPrefix``` (see below), being '.' by default
* ```"cssPseudo"```  (optional):
  If present, this is the
  [pseudo-class](https://developer.mozilla.org/fr/docs/Web/CSS/Pseudo-classes)
  added at the end of the ```cssSelector```

#### ```"spriteFilename"```  (mandatory)
A string of the name of the resulting sprite, without the image extension.
2 versions is be created: a ```.png```, and a ```.webp```.

#### ```"strategy"```  (optional)
This is the algorithm strategy to place subimages in the sprite,
when posHor and posVer are not provided.

The strategy can have the following values:
* ```hor```: the generated sprite will be a rectangle with the minimum
  height
* ```ver```: the generated sprite will be a rectangle with
  the minimum width
* ```square```: the generated sprite will be as squared as possible
* ```auto``` (default value): either ```hor``` (when
  the max height of the subimages is greater than the max width 
  of the subimages) or ```ver``` is chosen

#### ```"cssCommon"```  (optional)
A list of 
[css rules](https://developer.mozilla.org/fr/docs/Learn/Getting_started_with_the_web/CSS_basics) ```"property: value;"``` 
common to
all the designated selectors of the sprite.
Typically, we could have ```"display": inline-block;```.

Here, this is **important** to add the background-image
property, with the correct path of the sprite image. As an example, it could be
```
  "background-image:url(sprite.png)"
```

#### ```"cssFilename"```  (optional)
If present, a css file containing the selectors
is created. This css file can then be used by your html.

If not present, the generated css content is displayed on
the console.

#### ```"cssSelectorPrefix"``` (optional)
In case the ```cssSelector``` property is not set for a subimage,
its cssSelector is generated using the image filename, prefixed
with ```cssSelectorPrefix``` (its default value is ```'.'```)

### Command line
The above json file can be provided to the command line
```python -m spriteforhtml -json <sprite.json>```, or using
the API functions ```create_from_memory``` and
```create_sprites```

But this is also possible to call the command-line without
a json file providing the following options. From these options,
a json object is created in memory, and then
```create_from_memory``` is called.

* ```--spriteFilename <spritename>``` (mandatory):
  Name of the sprite images to be created, without the image
  extension.
  In the json object, it populates `spriteFilename` property
* ```--spriteFilename img1.png, img2.png...``` (mandatory):
  all the subimage names to be used to create the sprite.
  In the json object, it populates `"subimages" "filename"`
* ```--strategy <value>``` (optional):
  The placement strategy to be used.
  Default is `auto`.
  In the json object, it populates ```strategy```
* ```--cssSelectorPrefix <value>``` (optional):
  In the json object, it populates ```cssSelectorPrefix```
* ```--cssPseudo <value>``` (optional):
  In the json object, it populates ```cssPseudo```
  of all subimages
* ```--cssFilename <filename>``` (optional):
  Css file to create
  In the json object, it populates ```cssFilename```
* ```--cssCommon <value>``` (optional):
  A string of all css rules to be added  to
  all the designated selectors of the sprite
  In the json object, it populates ```cssCommon```

### Use the result
To basically use the generated files, you must add in the
head section of the html a link to the created .css file,
for example
```
  <link href="sprite.css" rel="stylesheet" media="all">
```

and use the icons in the body. This usage depends on the
way the selectors are defined in your sprite.json, 
but it can be typically
```
  <span class="icon-facebook">  </span>
```

You may refer to the 
[example page](https://github.com/pascal-brand38/py-spriteforhtml/tree/main/src/spriteforhtml/data/page.html).


# Releases

## 1.1

* Automatic placement, with multiple strategies
* command-line without json file
* Automatic css selector naming
* API using json object

### 1.1.1
* Fix python v3.8 and v3.9 (match instruction)
* Pylint and pytest

## 1.0

Initial version
* Use json file
* Subimage description include their placement
