#!/usr/bin/env python
"""A simple pygame module demonstrating population growth"""

import pygame
from pygame.locals import *

B = (0, 0, 0)
W = (255, 255, 255)
x_direction = 0
y_direction = 0

# A 2d array of black and white pixels poorly resembling a person
dude_map = [[W, W, B, B, B, B, B, B, B, B, W, W],
            [W, B, B, W, W, W, W, W, W, B, B, W],
            [B, B, W, W, B, W, W, B, W, W, B, B],
            [B, W, W, W, W, W, W, W, W, W, W, B],
            [B, W, W, W, B, B, B, B, W, W, W, B],
            [B, B, W, W, W, W, W, W, W, W, B, B],
            [W, B, B, B, B, B, B, B, B, B, B, W],
            [W, W, W, B, W, W, W, W, B, W, W, W],
            [W, B, B, B, W, W, W, W, B, B, B, W],
            [B, B, W, W, W, W, W, W, W, W, B, B],
            [B, W, W, B, W, W, W, W, B, W, W, B],
            [B, B, B, B, W, W, W, W, B, B, B, B],
            [W, W, B, B, W, W, W, W, B, B, W, W],
            [W, B, B, W, W, W, W, W, W, B, B, W],
            [W, B, W, W, W, B, B, W, W, W, B, W],
            [W, B, B, B, B, B, B, B, B, B, B, W]]

dude = pygame.Surface((12, 16))

for x in xrange(12):
    for y in xrange(16):
        dude.set_at((x, y), dude_map[y][x])

dude = pygame.transform.scale(dude, (24, 32))    # Scale to an appropriate surface
group = pygame.sprite.Group()

class Dude(pygame.sprite.Sprite):
    def __init__(self, location, add_group):
        pygame.sprite.Sprite.__init__(self, add_group)
        
        self.image = dude.convert()
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location
    
    def update(self):
        global group
        self.rect.move_ip(x_direction * self.rect.width, y_direction * self.rect.height)
        neighbors = pygame.sprite.Group()
        self.l = Dude((self.rect.left - self.rect.width, self.rect.top), neighbors)
        self.r = Dude((self.rect.left + self.rect.width, self.rect.top), neighbors)
        self.u = Dude((self.rect.left, self.rect.top - self.rect.height), neighbors)
        self.d = Dude((self.rect.left, self.rect.top + self.rect.height), neighbors)
        pygame.sprite.groupcollide(neighbors, group, False, True)   # Remove pre-existing object from group
        group.add(neighbors)

def main():
    global x_direction, y_direction
    pygame.init()
    running = True
    pygame.key.set_repeat(500, 100)
    screen = pygame.display.set_mode((640, 640))
    
    background = pygame.Surface((640, 640))
    background.fill((255, 255, 255))
    dude_1 = Dude((308, 304), group)    # Start in the center
    
    screen.blit(background, (0, 0))
    screen.blit(dude_1.image, dude_1.rect)
    pygame.display.update()
    
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == KEYDOWN:
                if event.key == K_UP:
                    y_direction += -1
                elif event.key == K_DOWN:
                    y_direction += 1
                elif event.key == K_LEFT:
                    x_direction += -1
                elif event.key == K_RIGHT:
                    x_direction += 1
                group.update()
#                screen.blit(background, (0, 0))    # Not necessary for now
                group.draw(screen)
                x_direction = 0
                y_direction = 0
                pygame.display.update()
    
    pygame.quit()

if __name__ == "__main__": main()

