#!/usr/bin/env python
import pygame
import sys
import random
import numpy
from pygame.locals import *

## Basic setup
pygame.init()
fpsLimit = pygame.time.Clock()

global playerSprite, mobSprite

## Will be used later
mouseX, mouseY = 0, 0
playerHealth = 20

## Setting up the frame
icon = pygame.image.load('sprites/other/ldOctober.png')
font = pygame.font.Font('fonts/gameFont.ttf', 20)
backgroundMusic = pygame.mixer.Sound('audio/groove.wav')

pygame.display.set_icon(icon)
pygame.display.set_caption('LD October Challenge')
background = pygame.image.load('sprites/terrain/mapOne.png')
screenX = 560
screenY = 560
surface = pygame.display.set_mode((screenY, screenX), pygame.DOUBLEBUF|pygame.NOFRAME)
#pygame.mouse.set_cursor(*pygame.cursors.diamond)

## Player stuff
playerBack = pygame.image.load('sprites/player/pb.png').convert_alpha()
playerFront = pygame.image.load('sprites/player/pf.png').convert_alpha()
playerLeft = pygame.image.load('sprites/player/ps.png').convert_alpha()
playerRight = pygame.transform.flip(playerLeft, True, False)

## Mob stuff
mobFront = pygame.image.load('sprites/mobs/ffm.png').convert_alpha()
mobBack = pygame.image.load('sprites/mobs/fbm.png').convert_alpha()
mobLeft = pygame.image.load('sprites/mobs/flm.png').convert_alpha()
mobRight = pygame.transform.flip(mobLeft, True, False)

## Terrain stuff
internalFloorTile = pygame.image.load('sprites/terrain/internalFloor.png')
externalFloorTile = pygame.image.load('sprites/terrain/externalFloor.png')

## Colour variables
RED = pygame.Color(255, 0, 0)
GREEN = pygame.Color(0, 255, 0)
BLUE = pygame.Color(0, 0, 255)
WHITE = pygame.Color(255, 255, 255)
BLACK = pygame.Color(0, 0, 0)
PINK = pygame.Color(255, 0, 255)
YELLOW = pygame.Color(255, 255, 0)

## Incrementing GRAY
LIGHTEST_GRAY = pygame.Color(120, 120, 120)
GRAY = pygame.Color(128, 128, 128)


## Mapping stuff
tileSize = 16
xStep = screenX / tileSize
yStep = screenY / tileSize

## General
playerX, playerY = screenX / 2, screenY / 2
speed = 0
playerDirection = 1
mobDirection = 1


mobX, mobY = random.randint(0, screenX), random.randint(0, screenY)

msg = ""

musicPlaying = False
minVolume = 0.000
maxVolume = 0.200
currentVolume = maxVolume
playMusic = True
repeatRate = 5
pygame.key.set_repeat(repeatRate)

while True:

    fpsLimit.tick(60)
    surface.fill(GRAY)

    if playMusic == False:
        backgroundMusic.stop()
    else:
        backgroundMusic.play()
        backgroundMusic.set_volume(currentVolume)

    msgSurface = font.render(msg, True, WHITE)
    msgRect = msgSurface.get_rect()
    msgRect.topleft = (10, 10)
    surface.blit(msgSurface, msgRect)

    if playerX == 0 and playerDirection == 2:
        speed = 0
    elif playerX == (screenX - 30) and playerDirection == 3:
        speed = 0
    elif playerY == 0 and playerDirection == 0:
        speed = 0
    elif playerY == (screenY - 30) and playerDirection == 1:
        speed = 0
    else:
        speed = 1

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN:
            if event.key == pygame.K_w:
                playerY -= speed
                playerDirection = 0
            elif event.key == pygame.K_s:
                playerY += speed
                playerDirection = 1
            elif event.key == pygame.K_a:
                playerX -= speed
                playerDirection = 2
            elif event.key == pygame.K_d:
                playerX += speed
                playerDirection = 3
            elif event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit(0)
            elif event.key == pygame.K_F1:
                if playMusic:
                    backgroundMusic.fadeout(1500)
                    msg = "Music: STOPPED"
                    playMusic = False
                else:
                    playMusic = True
                    msg = "Music: PLAYING"
            elif event.key == pygame.K_MINUS:
                pygame.key.set_repeat(repeatRate)
                if currentVolume > minVolume:
                    currentVolume -= 0.005
                    msg = " Volume: " + str((currentVolume * 10) / 2)
            elif event.key == pygame.K_EQUALS:
                pygame.key.set_repeat(repeatRate)
                if currentVolume < maxVolume:
                    currentVolume += 0.005
                    msg = " Volume: " + str((currentVolume * 10) / 2)

    if playerDirection == 0:
        playerSprite = playerBack
    elif playerDirection == 1:
        playerSprite = playerFront
    elif playerDirection == 2:
        playerSprite = playerLeft
    elif playerDirection == 3:
        playerSprite = playerRight

    if mobDirection == 0:
        mobSprite = mobBack
    elif mobDirection == 1:
        mobSprite = mobFront
    elif mobDirection == 2:
        mobSprite = mobLeft
    elif mobDirection == 3:
        mobSprite = mobRight

    surface.blit(playerSprite, (playerX, playerY))
    pygame.display.flip()
