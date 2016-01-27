import pygame
from enum import Enum
import math

"""
Tilemap:
BIG_DOT = 0
BLANK = 1
DOT = 2
DOWN_DOWBLE_WALL = 3
DL_ANGLED_CORNER = 4
DL_SMOOTH_CORNER = 5
DR_ANGLED_CORNER = 6
DR_SMOOTH_CORNER = 7
DOWN_SIMPLE_WALL = 8
GHOST_BARRIER = 9
LEFT_DOUBLE_WALL = 10
LEFT_SIMPLE_WALL = 11
RIGHT_DOUBLE_WALL = 12
RIGHT_SIMPLE_WALL = 13
UP_DOUBLE_WALL = 14
UL_ANGLED_CORNER = 15
UL_SMOOTH_CORNER = 16
UR_ANGLED_CORNER = 17
UR_SMOOTH_CORNER = 18
UP_SIMPLE_WALL = 19
FULL_WALL = 20
"""
Terrain_tiles = [pygame.image.load("assets/terrain/big_dot_sprite.png"), pygame.image.load("assets/terrain/blank_tile.png"), pygame.image.load("assets/terrain/dot_sprite.png"), pygame.image.load("assets/terrain/down_double_wall.png"), pygame.image.load("assets/terrain/down_left_angled_corner.png"), pygame.image.load("assets/terrain/down_left_smooth_corner.png"), pygame.image.load("assets/terrain/down_right_angled_corner.png"), pygame.image.load("assets/terrain/down_right_smooth_corner.png"), pygame.image.load("assets/terrain/down_simple_wall.png"), pygame.image.load("assets/terrain/ghost_spawn_barrier.png"), pygame.image.load("assets/terrain/left_double_wall.png"), pygame.image.load("assets/terrain/left_simple_wall.png"), pygame.image.load("assets/terrain/right_double_wall.png"), pygame.image.load("assets/terrain/right_simple_wall.png"), pygame.image.load("assets/terrain/up_double_wall.png"), pygame.image.load("assets/terrain/up_left_angled_corner.png"), pygame.image.load("assets/terrain/up_left_smooth_corner.png"), pygame.image.load("assets/terrain/up_right_angled_corner.png"), pygame.image.load("assets/terrain/up_right_smooth_corner.png"), pygame.image.load("assets/terrain/up_simple_wall.png"), pygame.image.load("assets/terrain/full_wall.png")]

class Direction(Enum):
    NONE = 0
    UP = 1
    RIGHT = 2
    DOWN = 3
    LEFT = 4

class Board:
    """Simple Pacman board"""
    width, height = 28, 31
    def __init__(self, path):
        with open(path, 'r') as tilemap:
            content = tilemap.read()
            self.tiles = parse_tilemap(content)

class PlayableSprite:
    speed = 0
    direction = Direction.NONE
    base_image = None
    none_sprite = None
    up_sprite = None
    right_sprite = None
    down_sprite = None
    left_sprite = None
    rect = pygame.Rect((15, 15), (15, 15))

class Ghost(PlayableSprite):
    """Ghost base class"""
    vulnerable_sprite = pygame.image.load("assets/vulnerable_ghost.png")
    def __init__(self, path):
        self.base_image = pygame.image.load(path)
        self.up_sprite = pygame.Rect((0, 0), (self.base_image.get_width() / 2, self.base_image.get_height() / 2))
        self.right_sprite = pygame.Rect((self.base_image.get_width() / 2, 0), (self.base_image.get_width() / 2, self.base_image.get_height() / 2))
        self.down_sprite = pygame.Rect((0, self.base_image.get_height() / 2), (self.base_image.get_width() / 2, self.base_image.get_height() / 2))
        self.left_sprite = pygame.Rect((self.base_image.get_width() / 2, self.base_image.get_height() / 2), (self.base_image.get_width() / 2, self.base_image.get_height() / 2))
        self.none_sprite = self.up_sprite

class Pacman(PlayableSprite):
    """Pacman object"""
    lives = 3

def parse_tilemap(content):
    tilemap = []
    for i in range(0, 28):
        tilemap.append([])
    lines = str.split(content, '\n')
    for ln in lines:
        x = 0
        if len(ln.strip()) != 0:
            els = str.split(ln, ',')
            for tl in els:
                tlidx = int(tl.strip())
                print("Terrain tile (%s,%s) = %s" %(x, len(tilemap[x]), Terrain_tiles[tlidx]))
                tilemap[x].append(Terrain_tiles[tlidx])
                x += 1
    return tilemap

def blit_tile(screen, tilemap, x, y, w, h, start_width):
    print("Get tile at position (%s, %s)" %(x, y))
    tile_surface = pygame.transform.scale(tilemap[x][y], (w, h))
    print("Blitting surface at position %s, %s" %(x * w + start_width, y * h))
    screen.blit(tile_surface, (x * w + start_width, y * h))

pygame.init();

akabe = Ghost("assets/akabe.png")
pinky = Ghost("assets/pinky.png")
aosuke = Ghost("assets/aosuke.png")
guzuta = Ghost("assets/guzuta.png")
board = Board("tilemap.pacman");

size = width, height = 1280, 800
vmin = min(width, height)
screen = pygame.display.set_mode(size)
# Assume Width > Height
tile_height = int(screen.get_height() / 31)
tile_width = int((screen.get_height() * 0.903225806) / 28)

start_x = (screen.get_width() - (28 * tile_width)) / 2

print("Tile width = %s, tile height = %s, start x = %s" %(tile_width, tile_height, start_x))

for curr_x in range(0, 28):
    for curr_y in range(0, 29):
        blit_tile(screen, board.tiles, curr_x, curr_y, tile_width, tile_height, start_x)

pygame.display.flip()

raw_input()
