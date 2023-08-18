# Introduction

**spriteforhtml** is a python package aimed at building a sprite from small image.
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




## Making your sprite

You have to write a json file with the same structure than [the one of the demo](https://github.com/pascal-brand38/py-spriteforhtml/tree/main/src/spriteforhtml/data/sprite.json). 