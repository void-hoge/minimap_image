# MINIMAP_IMAGE

Generate minimap images for tactics planning. Set the images as the background of google slide or MS powerpoint and use it by placing the ship icons.

![generated image](pics/greece4caps.png)

![example of using on google slide](pics/slide.png)

## Usage
```
$ ./minimap_image.py --json <json unpacked replay> --out <dst filename> --size <width>x<height>
```
- `--size` is optional. The default size is 1920x1080.

## Configuring
- You can configure capzone, background and grid rendering by modifing the global variables of `minimap_image.py`.
```python
BACKGROUND_COLOR = 32,32,32 # color of background
GRID_FONTFACE = 'Roboto-Medium.ttf' # font name of grid numbers and alphabets
GRID_FONTSIZE = 25 # font size of grid numbers and alphabets
GRID_COLOR = 255,255,255,40 # color of grid line
GRID_FONTCOLOR = 255,255,255,255 # color of grid numbers and alphabets
CAPZONE_FONTFACE = 'Roboto-Medium.ttf' # font name of capzone identifier alphabet
CAPZONE_FONTSIZE = 30 # font size of capzone identidier
CAPZONE_NEUTRAL_COLOR = 255,255,255 # color of capturezones initialized as neutral
CAPZONE_ALLY_COLOR = 50,255,50 # color of capturezones initialized as ally 
CAPZONE_ENEMY_COLOR = 255,0,0 # color of capturezones initialize as enemy
CAPZONE_TRANSPARENT = 30 # transparancy of capturezones
CAPZONE_OUTLINE_TRANSPARENT = 128 # transparancy of outline of capturezones
CAPZONE_FONT_TRANSPARENT = 255 # transparency of identifier alphabet of capturezones
MAPINFO_PATH = 'maps/manifest.json' # path of manifest.json
```


## Depends
- replay unpack
  - https://github.com/void-hoge/replays_unpack
  - original: https://github.com/Monstrofil/replays_unpack

## See Also
- shipicons
  - https://github.com/void-hoge/shipicons 
