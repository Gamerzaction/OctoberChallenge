#!/usr/bin/env python
import pygame
import sys
import time
from pygame.locals import *


class Container():
    def __init__(self):
        pass


class OctoberChallenge():
    global data
    data = Container()
    def __init__(self):
        ## Basic setup
        pygame.init()
        fps_limiter = pygame.time.Clock()

        ## Will be used later
        data.player_health = 20

        ## Setting up the frame
        icon = pygame.image.load('sprites/other/ldOctober.png')
        data.font = pygame.font.Font('fonts/gameFont.ttf', 20)
        data.ambient_music = pygame.mixer.Sound('audio/groove.wav')

        pygame.display.set_icon(icon)
        background = pygame.image.load('sprites/terrain/mapOne.png')
        data.screen_x = 560
        data.screen_y = 560
        data.surface = pygame.display.set_mode((data.screen_x, data.screen_y), pygame.DOUBLEBUF)

        ## Mouse stuff
        data.mouse_x, data.mouse_y = pygame.mouse.get_pos()
        data.mouse_pointer = pygame.image.load('sprites/other/mouse_pointer.png').convert_alpha()

        ## Player stuff
        data.player_back = pygame.transform.scale2x(pygame.image.load('sprites/player/pb.png').convert_alpha())
        data.player_front = pygame.transform.scale2x(pygame.image.load('sprites/player/pf.png').convert_alpha())
        data.player_left = pygame.transform.scale2x(pygame.image.load('sprites/player/ps.png').convert_alpha())
        data.player_right = pygame.transform.flip(data.player_left, True, False)
        data.player_sprite = data.player_front

        ## Mob stuff
        data.mob_front = pygame.image.load('sprites/mobs/ffm.png').convert_alpha()
        data.mob_back = pygame.image.load('sprites/mobs/fbm.png').convert_alpha()
        data.mob_left = pygame.image.load('sprites/mobs/flm.png').convert_alpha()
        data.mob_right = pygame.transform.flip(data.mob_left, True, False)

        ## Terrain types
        stone_floor_internal = pygame.transform.scale2x(pygame.image.load('sprites/terrain/internal_floor.png'))
        grass_floor_external = pygame.transform.scale2x(pygame.image.load('sprites/terrain/external_floor.png'))

        ## Colour variables
        data.red = pygame.Color(255, 0, 0)
        data.green = pygame.Color(0, 255, 0)
        data.blue = pygame.Color(0, 0, 255)
        data.white = pygame.Color(255, 255, 255)
        data.black = pygame.Color(0, 0, 0)
        data.pink = pygame.Color(255, 0, 255)
        data.yellow = pygame.Color(255, 255, 0)

        ## Mapping stuff
        data.tile_size = 16
        data.x_step = data.screen_x / data.tile_size
        data.y_step = data.screen_y / data.tile_size

        ## Direction stuff
        data.north = False
        data.south = False
        data.east = False
        data.west = False

        ## General
        data.player_x = data.screen_x / 2
        data.player_y = data.screen_y / 2
        data.player_move_speed = 1

        ## Audio variables
        data.music_playing = False
        data.min_volume = 0.000
        data.max_volume = 0.200
        data.play_music = True
        data.vol_up = False
        data.vol_down = False
        data.current_volume = 0.2

        ## Other stuff
        data.time_played = 0
        data.frame_rate = 30

        surface_array = []
        for x in range(0, data.screen_x / data.x_step):
            for y in range(0, data.screen_y / data.y_step):
                surface_array.append((x, y))

        while True:

            fps_limiter.tick(100)
            for x in range(len(surface_array)):
                for y in range(len(surface_array)):
                    data.surface.blit(grass_floor_external, (x * 32, y * 32))
            data.surface.blit(data.mouse_pointer, (data.mouse_x, data.mouse_y))

            self.controls()
            self.player_move_control()
            self.audio_control()

            ## All terrain blitting must be done before this
            if data.play_music:
                self.draw_message("Volume: " + str(data.current_volume), 10, 10, data.blue)
            data.surface.blit(self.player_sprite_control(), (data.player_x, data.player_y))
            pygame.display.update()
            pygame.display.set_caption("FPS: %s" % fps_limiter.get_fps())

    @staticmethod
    def controls():

        keys = pygame.key.get_pressed()
        if keys[K_w] or keys[K_UP]:
            data.north = True
            data.south = False
        if keys[K_s] or keys[K_DOWN]:
            data.north = False
            data.south = True
        if keys[K_a] or keys[K_LEFT]:
            data.west = True
            data.east = False
        if keys[K_d] or keys[K_RIGHT]:
            data.west = False
            data.east = True
        if keys[K_MINUS]:
            data.vol_down = True
            data.vol_up = False
        if keys[K_EQUALS]:
            data.vol_down = False
            data.vol_up = True

        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                print("Mouse x: %s | Mouse y: %s" % (data.mouse_x, data.mouse_y))
            elif event.type == MOUSEMOTION:
                data.mouse_x, data.mouse_y = event.pos
            elif event.type == KEYDOWN:
                if event.key == K_p:
                    if data.play_music:
                        data.play_music = False
                    elif not data.play_music:
                        data.play_music = True
            elif event.type == KEYUP:
                if event.key == (K_w or K_UP):
                    data.north = False
                    data.south = False
                if event.key == (K_s or K_DOWN):
                    data.north = False
                    data.south = False
                if event.key == (K_a or K_LEFT):
                    data.east = False
                    data.west = False
                if event.key == (K_d or K_RIGHT):
                    data.east = False
                    data.west = False
                if event.key == K_MINUS:
                    data.vol_down = False
                if event.key == K_EQUALS:
                    data.vol_up = False

    @staticmethod
    def player_move_control():

        if data.north:
            data.player_y -= data.player_move_speed
        if data.east:
            data.player_x += data.player_move_speed
        if data.south:
            data.player_y += data.player_move_speed
        if data.west:
            data.player_x -= data.player_move_speed

        if data.player_x == (0 or data.screen_x):
            data.player_move_speed = 0
        if data.player_y == (0 or data.screen_y):
            data.player_move_speed = 0

    @staticmethod
    def player_sprite_control():

        if data.north:
            data.player_sprite = data.player_back
        if data.south:
            data.player_sprite = data.player_front
        if data.east:
            data.player_sprite = data.player_right
        if data.west:
            data.player_sprite = data.player_left
        return data.player_sprite

    @staticmethod
    def draw_message(msg, loc_x, loc_y, colour):
        message_surface = data.font.render(msg, True, colour)
        message_rect = message_surface.get_rect()
        message_rect.topleft = (loc_x, loc_y)
        data.surface.blit(message_surface, message_rect)

    @staticmethod
    def audio_control():

        if data.vol_up:
            data.current_volume += 0.005
        elif data.vol_down:
            data.current_volume -= 0.005

        if data.play_music:
            data.ambient_music.play()
            data.ambient_music.set_volume(data.current_volume)
        else:
            data.ambient_music.stop()

if __name__ == '__main__':
    Game = OctoberChallenge()