#!/usr/bin/env python
import sys
import pygame
import random
from math import *
from pygame import *


class OctoberChallenge(pygame.sprite.Sprite):
    def __init__(self):
        # # Basic setup
        pygame.init()
        fps_limiter = pygame.time.Clock()

        # # Will be used later
        self.player_health = 20

        # # Setting up the frame
        icon = pygame.image.load('sprites/other/ldOctober.png')
        self.font = pygame.font.Font('fonts/gameFont.ttf', 20)
        self.ambient_music = pygame.mixer.Sound('audio/groove.wav')

        pygame.display.set_icon(icon)
        self.background = pygame.image.load('sprites/terrain/mapOne.png')
        self.screen_x = 560
        self.screen_y = 560
        self.surface = pygame.display.set_mode((self.screen_x, self.screen_y), pygame.DOUBLEBUF)
        self.bliter = pygame.surface.Surface((self.screen_x, self.screen_y))

        # # Mouse stuff
        self.mouse_x, self.mouse_y = pygame.mouse.get_pos()
        self.mouse_pointer = pygame.image.load('sprites/other/mouse_pointer.png').convert_alpha()

        # # Player stuff
        self.player_front = pygame.image.load('sprites/player/pf.png')
        self.player_back = pygame.image.load('sprites/player/pb.png')
        self.player_left = pygame.image.load('sprites/player/pl.png')
        self.player_right = pygame.transform.flip(self.player_left, True, False)

        self.player_front_rect = self.player_front.get_rect()
        self.player_back_rect = self.player_back.get_rect()
        self.player_left_rect = self.player_left.get_rect()
        self.player_right_rect = self.player_right.get_rect()

        self.player_sprite = self.player_front
        self.player_sprite_rect = self.player_sprite.get_rect()

        # Mob stuff

        # # Terrain types
        self.stone_floor_internal = pygame.image.load('sprites/terrain/internal_floor.png')
        self.stone_floor_rect = self.stone_floor_internal.get_rect()
        self.grass_floor_external = pygame.image.load('sprites/terrain/external_floor.png')
        self.grass_floor_rect = self.grass_floor_external.get_rect()

        # # Colour variables
        self.red = pygame.Color(255, 0, 0)
        self.green = pygame.Color(0, 255, 0)
        self.blue = pygame.Color(0, 0, 255)
        self.white = pygame.Color(255, 255, 255)
        self.black = pygame.Color(0, 0, 0)
        self.pink = pygame.Color(255, 0, 255)
        self.yellow = pygame.Color(255, 255, 0)

        # # Mapping stuff
        self.tile_size = 16
        self.x_step = self.screen_x / self.tile_size
        self.y_step = self.screen_y / self.tile_size
        self.tile_type = 0
        self.tiles = 0
        self.tile_map = []
        while self.tiles < 16:
            self.y_pos = random.randint(1, self.screen_y) / 16
            self.x_pos = random.randint(1, self.screen_x)
            self.tile_map.append((self.x_pos / self.tile_size, self.y_pos / self.tile_size))
            self.tiles += 1

        # # Direction stuff
        self.north = False
        self.south = False
        self.east = False
        self.west = False

        # # General
        self.player_x = self.screen_x / 2
        self.player_y = self.screen_y / 2
        self.player_move_speed = 1

        # # Audio variables
        self.music_playing = False
        self.min_volume = 0.000
        self.max_volume = 0.200
        self.play_music = False
        self.vol_up = False
        self.vol_down = False
        self.current_volume = 0.2

        # # Other stuff
        self.time_played = 0
        self.frame_rate = 30
        
        self.move_speed = 1

        surface_array = []
        for x in range(0, self.screen_x / self.x_step):
            for y in range(0, self.screen_y / self.y_step):
                surface_array.append((x, y))

        while True:

            self.tile_type = random.randint(0, 2)

            fps_limiter.tick(60)
            #===================================================================
            # for x in range(len(surface_array)):
            #     for y in range(len(surface_array)):
            #         self.surface.blit(grass_floor_external, (x * 32, y * 32))
            # self.draw()
            # self.surface.blit(self.mouse_pointer, (self.mouse_x, self.mouse_y))
            #===================================================================
            self.surface.fill(self.white)
            self.controls()
            self.player_move_control()
            self.audio_control()

            for i in self.tile_map:
                self.surface.blit(self.stone_floor_internal, i, self.stone_floor_rect)
            # # All terrain blitting must be done before this
            if self.play_music:
                self.draw_message("Volume: " + str(self.current_volume), 10, 10, self.blue)
            self.surface.blit(self.player_sprite_control(), (self.player_x, self.player_y))
            pygame.display.update()
            pygame.display.set_caption("FPS: %s" % round(fps_limiter.get_fps()) + " | October LD")

    def gen_terrain(self):
        v = random.randint(0, self.screen_x)
        a = sin(v)
        b = cos(v)
        d = sqrt(self.screen_x ** 2 + self.screen_y ** 2)
        c = random.random() * d - d / 2
        e = random.randint(15)
        for x in range(self.screen_x):
            for y in range(self.screen_y):
                self.terrain_array[x][y] += e * atan(a * x + b * y - c)

    def draw(self):
        for y in range(0, self.screen_y):
            for x in range(0, self.screen_x):
                if self.terrain_array[y][x] + 150 < 0:
                    color = self.black
                else:
                    if self.terrain_array[y][x] + 150 > 255:
                        color = self.white
                    else:
                        color = [self.terrain_array[y][x] + 150, self.terrain_array[y][x] + 150, self.terrain_array[y][x] + 150]
                self.bliter.fill(color)
        self.surface.blit(self.bliter, (x * self.tile_size, y * self.tile_size))
        pygame.display.flip()

    def controls(self):

        keys = pygame.key.get_pressed()
        if keys[K_w] or keys[K_UP]:
            self.north = True
            self.south = False
        if keys[K_s] or keys[K_DOWN]:
            self.north = False
            self.south = True
        if keys[K_a] or keys[K_LEFT]:
            self.west = True
            self.east = False
        if keys[K_d] or keys[K_RIGHT]:
            self.west = False
            self.east = True
        if keys[K_MINUS]:
            self.vol_down = True
            self.vol_up = False
        if keys[K_EQUALS]:
            self.vol_down = False
            self.vol_up = True

        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                print("Mouse x: %s | Mouse y: %s" % (self.mouse_x, self.mouse_y))
            elif event.type == MOUSEMOTION:
                self.mouse_x, self.mouse_y = event.pos
            elif event.type == KEYDOWN:
                if event.key == K_p:
                    if self.play_music:
                        self.play_music = False
                    elif not self.play_music:
                        self.play_music = True
            elif event.type == KEYUP:
                if event.key == (K_w or K_UP):
                    self.north = False
                    self.south = False
                if event.key == (K_s or K_DOWN):
                    self.north = False
                    self.south = False
                if event.key == (K_a or K_LEFT):
                    self.east = False
                    self.west = False
                if event.key == (K_d or K_RIGHT):
                    self.east = False
                    self.west = False
                if event.key == K_MINUS:
                    self.vol_down = False
                if event.key == K_EQUALS:
                    self.vol_up = False
                    
    def player_move_control(self):
        if self.north:
            self.player_y -= self.move_speed
        if self.east:
            self.player_x += self.move_speed
        if self.south:
            self.player_y += self.move_speed
        if self.west:
            self.player_x -= self.move_speed
        if self.player_x == 0:
            self.west = False
            print self.east
            print self.west
        if self.player_x == self.screen_x:
            self.player_move_speed = 0
            self.east = False
            print self.east
            print self.west
        if self.player_y == 0:
            self.player_move_speed = 0
            self.north = False
            print self.north
            print self.south
        if self.player_y == self.screen_y:
            self.player_move_speed = 0
            self.south = False
            print self.north
            print self.south

    def player_sprite_control(self):
        if self.north:
            self.player_sprite = self.player_back
        if self.south:
            self.player_sprite = self.player_front
        if self.east:
            self.player_sprite = self.player_right
        if self.west:
            self.player_sprite = self.player_left

        return self.player_sprite

    def draw_message(self, msg, loc_x, loc_y, colour):
        message_surface = self.font.render(msg, True, colour)
        message_rect = message_surface.get_rect()
        message_rect.topleft = (loc_x, loc_y)
        self.surface.blit(message_surface, message_rect)

    def audio_control(self):

        if self.vol_up:
            self.current_volume += 0.005
        elif self.vol_down:
            self.current_volume -= 0.005

        if self.play_music:
            self.ambient_music.play()
            self.ambient_music.set_volume(self.current_volume)
        else:
            self.ambient_music.stop()
            
    def collision_detection(self, group_name):
        if pygame.sprite.spritecollide(self, group_name, False):
            self.move_speed = -self.move_speed           

if __name__ == '__main__':
    Game = OctoberChallenge()
