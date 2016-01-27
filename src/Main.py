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

    def __init__(self, path):
        with open(path, 'r') as tilemap:
            content = tilemap.read()
            self.tiles = parse_tilemap(content)

        self.size = width, height = 1280, 800
        vmin = min(width, height)
        self.screen = pygame.display.set_mode(self.size)
        # Assume Width > Height
        self.tile_height = int(self.screen.get_height() / 28)
        self.tile_width = int((self.screen.get_height() * 0.903225806) / 28)

        self.start_x = (self.screen.get_width() - (28 * self.tile_width)) / 2

        #print("Tile width = %s, tile height = %s, start x = %s" %(self.tile_width, self.tile_height, self.start_x))

        for curr_x in range(0, 28):
            for curr_y in range(0, 29):
                self.blit_tile(self.tiles[curr_x][curr_y], curr_x, curr_y)

    def blit_tile(self, sprite, x, y):
        tile_surface = pygame.transform.scale(sprite, (self.tile_width, self.tile_height))
        self.screen.blit(tile_surface, (x * self.tile_width + self.start_x , self.tile_height * y))

    def blit(self, sprite):
        tile_pos = sprite.get_curr_tile(self)
        print("Sprite is in position %s" % (tile_pos, ))
        x = tile_pos[0]
        y = tile_pos[1]
        self.blit_tile(self.tiles[x][y], x, y)
        self.blit_tile(self.tiles[x - 1][y], x - 1, y)
        self.blit_tile(self.tiles[x + 1][y], x + 1, y)
        self.blit_tile(self.tiles[x][y - 1], x, y - 1)
        self.blit_tile(self.tiles[x][y + 1], x, y + 1)
        self.blit_tile(self.tiles[x - 1][y - 1], x - 1, y - 1)
        self.blit_tile(self.tiles[x + 1][y - 1], x + 1, y - 1)
        self.blit_tile(self.tiles[x - 1][y + 1], x - 1, y + 1)
        self.blit_tile(self.tiles[x + 1][y + 1], x + 1, y + 1)
        sprite_surface = pygame.transform.scale(sprite.current_sprite(), (self.tile_width, self.tile_height))
        self.screen.blit(sprite_surface, (sprite.x, sprite.y))

    def is_wall(self, x, y):
        tile = self.tilemap[x][y]
        return tile != Terrain_tiles[0] and tile != Terrain_tiles[1] and tile != Terrain_tiles[2]

class PlayableSprite:
    speed = 4
    direction = Direction.NONE
    base_image = None
    none_sprite = None
    up_sprite = None
    right_sprite = None
    down_sprite = None
    left_sprite = None
    rect = pygame.Rect((15, 15), (15, 15))
    x = 0
    y = 0

    def current_sprite(self):
        if(self.direction == Direction.NONE):
            return self.none_sprite
        elif(self.direction == Direction.UP):
            return self.up_sprite
        elif(self.direction == Direction.DOWN):
            return self.down_sprite
        elif(self.direction == Direction.LEFT):
            return self.left_sprite
        elif(self.direction == Direction.RIGHT):
            return self.right_sprite

    def spawn(self, board, x, y):
        board.blit_tile(self.none_sprite, x, y)
        self.x = board.start_x + x * board.tile_width
        self.y = y * board.tile_height
        self.board = board

    def get_curr_tile(self, board):
        x_tile = (self.x - board.start_x) / board.tile_width
        y_tile = self.y / board.tile_height
        return (x_tile, y_tile)

    def update(self, i):
        if(i == UP):
            self.direction = Direction.UP
            self.y -= self.speed
        elif(i == RIGHT):
            self.direction = Direction.RIGHT
            self.x += self.speed
        elif(i == DOWN):
            self.direction = Direction.DOWN
            self.y += self.speed
        elif(i == LEFT):
            self.direction = Direction.LEFT
            self.x -= self.speed

class Ghost(PlayableSprite):
    """Ghost base class"""
    vulnerable_sprite = pygame.image.load("assets/vulnerable_ghost.png")

    def __init__(self, path):
        self.base_image = pygame.image.load(path)
        sprite_surface = (self.base_image.get_width() // 2, self.base_image.get_height() // 2)

        sprite_base = pygame.Rect((0, 0), sprite_surface)
        self.up_sprite = self.base_image.subsurface(sprite_base)

        sprite_base = pygame.Rect((self.base_image.get_width() // 2, 0), sprite_surface)
        self.right_sprite = self.base_image.subsurface(sprite_base)

        sprite_base = pygame.Rect((0, self.base_image.get_height() // 2), sprite_surface)
        self.down_sprite = self.base_image.subsurface(sprite_base)

        sprite_base = pygame.Rect((self.base_image.get_width() // 2, self.base_image.get_height() // 2), sprite_surface)
        self.left_sprite = self.base_image.subsurface(sprite_base)

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
                #print("Terrain tile (%s,%s) = %s" %(x, len(tilemap[x]), Terrain_tiles[tlidx]))
                tilemap[x].append(Terrain_tiles[tlidx])
                x += 1
    return tilemap

def main():
    pygame.init();
    pygame.mixer.init();

    akabe = Ghost("assets/akabe.png")
    pinky = Ghost("assets/pinky.png")
    aosuke = Ghost("assets/aosuke.png")
    guzuta = Ghost("assets/guzuta.png")
    #pacman = Pacman("assets/pacman.png")
    board = Board("tilemap.pacman");

    player_entities = [akabe, pinky, aosuke, guzuta]
    player_mappings = [
            [pygame.K_UP, pygame.K_RIGHT, pygame.K_DOWN, pygame.K_LEFT],
            [pygame.K_w, pygame.K_d, pygame.K_s, pygame.K_a],
            [pygame.K_t, pygame.K_h, pygame.K_g, pygame.K_f],
            [pygame.K_i, pygame.K_l, pygame.K_k, pygame.K_j]
            ]

    akabe.spawn(board, 13, 10)
    pinky.spawn(board, 11, 13)
    aosuke.spawn(board, 13, 13)
    guzuta.spawn(board, 15, 13)

    pygame.display.flip()

    aka_pos = akabe.get_curr_tile(board)
    pink_pos = pinky.get_curr_tile(board)
    ao_pos = aosuke.get_curr_tile(board)
    guz_pos = guzuta.get_curr_tile(board)

    while True:
        for event in pygame.event.get():
            if event.type != pygame.KEYDOWN:
                continue
            if event.key == pygame.K_q:
                return
            for i in range(0, 4):
                for j in range(0, 4):
                    if event.key == player_mappings[i][j]:
                        player_entities[i].update(j)
        for i in range(0, 4):
            board.blit(player_entities[i])
        pygame.display.flip()

UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3

main()
