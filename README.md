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
There are 2 ways to generate a sprite and css file:
* Using the command line:
  ```python -m spriteforhtml <mysprite.json>```
* Using the API in your favorite python source, with the following:
```
  from spriteforhtml.create import create_sprites
  create_sprites('<mysprite.json>')
```

### <mysprite.json>
This file is a json file format that includes all the information
used to create the sprite: small images name, position in sprite,
css class to generate, filenames of the resulting sprite, filename
of the runsulting css file,...

Do not hesitate to check 
[the one of the demo](https://github.com/pascal-brand38/py-spriteforhtml/tree/main/src/spriteforhtml/data/sprite.json).

<br />
Note that in the following, when a path or a filename is considered, there are 2 different cases to take care:

* an absolute path
* a relative path: it is then relative to the
  location of ```<mysprite.json>```

<br />
The properties of the json are:

#### ```"subimages"```
A list of objects describing all the sub images to be used in the sprite.
Each sub image is made of a json object containing the following properties:
* ```"filename"```: the name of the subimage
* ```"posHor"```: its horizontal position in the sprite
* ```"posVer"```: its vertical position in the sprite
* ```"cssSelector"```: the css selector to use it in html.  It can be a class
  (starting with a .), an id (starting with a #),...
* ```"cssPseudo"```: It is optional. If present, this is the
  [pseudo-class](https://developer.mozilla.org/fr/docs/Web/CSS/Pseudo-classes)
  added at the end of the ```cssSelector```


#### ```"spriteFilename"``` 
A string of the name of the resulting sprite, without the image extension.
2 versions is be created: a ```.png```, and a ```.webp```.

### ```"cssCommon"```
A list of 
[css rules](https://developer.mozilla.org/fr/docs/Learn/Getting_started_with_the_web/CSS_basics) ```"property: value;"``` 
common to
all the designated selectors for the sprite.
Typically, we could have ```"display: inline-block;```.

Here, this is **important** to add the background-image
property, with the correct path of the sprite image. As an example, it could be
```
  "background-image:url(sprite.png)"
```


#### ```cssFilename```
This is an optional property.
If present, a css file containing the selectors
is created. This css file can then be used by your html.

If not present, the generated css content is displayed on
the console.


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
