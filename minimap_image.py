#!/usr/bin/env python3

from PIL import Image, ImageFont, ImageDraw
import json
import sys

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
CAPZONE_FONT_TRANSPARENT = 255
MAPINFO_PATH = 'maps/manifest.json'


class minimap_image:
    def __init__(self, replayfile):
        self.mapinfo = json.loads(open('maps/manifest.json', 'r').read())
        self.replaydata = json.loads(open(replayfile, 'r').read())
        self.mapname = self.replaydata['hidden']['map']
        self.mapsize = self.mapinfo[self.mapname][1]
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

    def render(self, size, filename):
        base = Image.new('RGB', size, color=(255,255,255))
        base = self.draw_minimap_image(base, size)
        base = self.draw_grid(base, size, GRID_COLOR, 2)
        fontface = ImageFont.truetype(GRID_FONTFACE, GRID_FONTSIZE)
        base = self.draw_grid_name(base, size, GRID_FONTCOLOR, fontface, (10, 10))
        fontface = ImageFont.truetype(CAPZONE_FONTFACE, CAPZONE_FONTSIZE)
        base = self.draw_capture_zones(
            base, size,
            CAPZONE_NEUTRAL_COLOR,
            CAPZONE_ALLY_COLOR,
            CAPZONE_ENEMY_COLOR,
            CAPZONE_TRANSPARENT,
            CAPZONE_FONT_TRANSPARENT,
            fontface)
        base.save(filename)

    def draw_minimap_image(self, base, size):
        base.paste(self.background.resize(size, Image.NEAREST))
        islands = self.islands.resize(size, Image.NEAREST)
        base.paste(islands, mask=islands)
        return base

    def draw_grid(self, base, size, color, width):
        draw = ImageDraw.Draw(base, 'RGBA')
        x, y = size
        gx, gy = x/10, y/10
        for i in range(10):
            draw.line((0,gy*i,x,gy*i), fill=color, width=width)
            draw.line((gx*i,0,gx*i,y), fill=color, width=width)
        return base

    def draw_grid_name(self, base, size, color, fontface, centeroffset):
        draw = ImageDraw.Draw(base, 'RGBA')
        x, y = size
        gx, gy = x/10, y/10
        vcenter, hcenter = centeroffset
        for i, c in enumerate('ABCDEFGHIJ'):
            left, top, right, bottom = fontface.getbbox(c)
            width, height = right - left, bottom - top
            pos = vcenter-width/2, gy*i + gy/2 - height/2
            draw.text(pos, c, font=fontface, fill=color)
        for i in range(0,10):
            left, top, right, bottom = fontface.getbbox(str(i+1))
            width, height = right - left, bottom - top
            pos = gx*i + gx/2 - width/2, hcenter-bottom+height
            draw.text(pos, str(i+1), font=fontface, fill=color)
        return base

    def draw_capture_zones(self, base, size, neutral, ally, enemy, trans, fonttrans, fontface):
        draw = ImageDraw.Draw(base, 'RGBA')
        ix, iy = size
        xscale, yscale = ix/self.mapsize, iy/self.mapsize
        for index, cap in self.caps.items():
            radius = cap['radius']
            position = cap['position']
            name = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'[index]
            upperleft = (position['x']-radius)*xscale + ix/2, -(position['z']+radius)*yscale + iy/2
            lowerright = (position['x']+radius)*xscale + ix/2, -(position['z']-radius)*yscale + iy/2
            if cap['teamId'] == -1:
                color = neutral
            elif cap['teamId'] == 0:
                color = ally
            elif cap['teamId'] == 1:
                color = enemy
            draw.ellipse((upperleft, lowerright), fill=color+(trans,))
            if cap['type'] == 1:
                left, top, right, bottom = fontface.getbbox(name)
                width, height = right - left, bottom - top
                pos = position['x']*xscale + ix/2 - width/2, -position['z']*yscale + iy/2 - bottom + height/2
                draw.text(pos, name, font=fontface, fill=color+(fonttrans,))
        return base
    
def main():
    renderer = minimap_image(sys.argv[1])
    renderer.render((1080, 1080), 'test.png')

if __name__ == '__main__':
    main()
