#!/usr/bin/env python3

from PIL import Image, ImageFont, ImageDraw
import json
import sys

BACKGROUND_COLOR = 32,32,32
GRID_FONTFACE = 'Roboto-Medium.ttf'
GRID_FONTSIZE = 25
GRID_COLOR = 255,255,255,40
GRID_FONTCOLOR = 255,255,255,255
CAPZONE_FONTFACE = 'Roboto-Medium.ttf'
CAPZONE_FONTSIZE = 30
CAPZONE_NEUTRAL_COLOR = 255,255,255
CAPZONE_ALLY_COLOR = 50,255,50
CAPZONE_ENEMY_COLOR = 255,0,0
CAPZONE_TRANSPARENT = 30
CAPZONE_OUTLINE_TRANSPARENT = 128
CAPZONE_FONT_TRANSPARENT = 255
MAPINFO_PATH = 'maps/manifest.json'


class minimap_image:
    def __init__(self, replayfile):
        self.mapinfo = json.loads(open(MAPINFO_PATH, 'r').read())
        self.replaydata = json.loads(open(replayfile, 'r').read())
        self.mapname = self.replaydata['hidden']['map']
        self.mapsize = self.mapinfo[self.mapname][1]
        print(f'{self.mapname}: {self.mapsize*30//1000}x{self.mapsize*30//1000}km')
        self.load_images()
        self.load_caps()

    def load_images(self):
        self.islands = Image.open(f'maps/{self.mapname}/minimap.png')
        self.background = Image.open(f'maps/{self.mapname}/minimap_water.png')

    def load_caps(self):
        self.caps = {}
        for cap in self.replaydata['hidden']['control_points']:
            self.caps[cap['componentsState']['controlPoint']['index']] = {
                'position':cap['position'],
                'radius':cap['radius'],
                'innerRadius':cap['innerRadius'],
                'teamId':cap['teamId'],
                'type':cap['componentsState']['controlPoint']['type'],
            }

    def render(self, backgroundsize, filename):
        width, height = backgroundsize
        if width < height:
            size = width, width
            offset = 0, (height-width)//2
        else:
            size = height, height
            offset = (width-height)//2, 0
        base = Image.new('RGB', backgroundsize, color=BACKGROUND_COLOR)
        base = self.draw_minimap_image(base, size, offset)
        base = self.draw_grid(base, size, offset, GRID_COLOR, 2)
        fontface = ImageFont.truetype(GRID_FONTFACE, GRID_FONTSIZE)
        base = self.draw_grid_name(base, size, offset, GRID_FONTCOLOR, fontface, (10,7))
        fontface = ImageFont.truetype(CAPZONE_FONTFACE, CAPZONE_FONTSIZE)
        base = self.draw_capture_zones(
            base, size, offset,
            CAPZONE_NEUTRAL_COLOR,
            CAPZONE_ALLY_COLOR,
            CAPZONE_ENEMY_COLOR,
            CAPZONE_TRANSPARENT,
            CAPZONE_FONT_TRANSPARENT,
            CAPZONE_OUTLINE_TRANSPARENT,
            fontface)
        base.save(filename)

    def draw_minimap_image(self, base, size, offset):
        base.paste(self.background.resize(size, Image.NEAREST), offset)
        islands = self.islands.resize(size, Image.NEAREST)
        base.paste(islands, offset, mask=islands)
        return base

    def draw_grid(self, base, size, offset, color, width):
        draw = ImageDraw.Draw(base, 'RGBA')
        x, y = offset
        sx, sy = size
        gx, gy = sx/10, sy/10
        for i in range(10):
            draw.line((x,gy*i+y,sx+x,gy*i+y), fill=color, width=width)
            draw.line((gx*i+x,y,gx*i+x,sy+y), fill=color, width=width)
        return base

    def draw_grid_name(self, base, size, offset, color, fontface, center):
        draw = ImageDraw.Draw(base, 'RGBA')
        x, y = offset
        sx, sy = size
        gx, gy = sx/10, sy/10
        vcenter, hcenter = center
        for i, c in enumerate('ABCDEFGHIJ'):
            left, top, right, bottom = fontface.getbbox(c)
            width, height = right - left, bottom - top
            pos = vcenter-width/2 + x, gy*i + gy/2 - height/2 + y
            draw.text(pos, c, font=fontface, fill=color)
        for i in range(0,10):
            left, top, right, bottom = fontface.getbbox(str(i+1))
            width, height = right - left, bottom - top
            pos = gx*i + gx/2 - width/2 + x, hcenter-bottom+height + y
            draw.text(pos, str(i+1), font=fontface, fill=color)
        return base

    def draw_capture_zones(self, base, size, offset, neutral, ally, enemy, trans, fonttrans, outlinetrans, fontface):
        draw = ImageDraw.Draw(base, 'RGBA')
        x, y = offset
        sx, sy = size
        xscale, yscale = sx/self.mapsize, sy/self.mapsize
        for index, cap in self.caps.items():
            radius = cap['radius']
            position = cap['position']
            name = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'[index]
            upperleft = (position['x']-radius)*xscale + sx/2 + x, -(position['z']+radius)*yscale + sy/2 + y
            lowerright = (position['x']+radius)*xscale + sx/2 + x, -(position['z']-radius)*yscale + sy/2 + y
            if cap['teamId'] == -1:
                color = neutral
            elif cap['teamId'] == 0:
                color = ally
            elif cap['teamId'] == 1:
                color = enemy
            draw.ellipse((upperleft, lowerright), fill=color+(trans,), outline=color+(outlinetrans,))
            if cap['type'] == 1:
                left, top, right, bottom = fontface.getbbox(name)
                width, height = right - left, bottom - top
                pos = position['x']*xscale + sx/2 - width/2 + x, -position['z']*yscale + sy/2 - bottom + height/2 + y
                draw.text(pos, name, font=fontface, fill=color+(fonttrans,))
        return base
    
def main():
    import argparse
    import re
    parser = argparse.ArgumentParser()
    parser.add_argument('--json', type=str, required=True)
    parser.add_argument('--out', type=str, required=True)
    parser.add_argument('--size', type=str, required=False)
    result = parser.parse_args()
    sizestr = result.size
    try:
        m = re.match(r'(\d+)x(\d+)',sizestr)
        size = int(m.group(1)), int(m.group(2))
    except TypeError:
        size = 1920, 1080

    renderer = minimap_image(result.json)
    renderer.render(size, result.out)

if __name__ == '__main__':
    main()
