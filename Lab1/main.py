import os
import sys
import pygame
import numpy as np
from figures import *

t = 0
Width = 640
Height = 640

b = -np.pi / 240
g = np.pi / 120
a = np.pi / 240

selected = 'x'
hold = True

pygame.init()
screen = pygame.display.set_mode((Width, Height))

pygame.font.init()
font = pygame.font.SysFont('Verdana', 20)

Star = Object(obj_to_coords('star.obj')).rotateX(3 * np.pi / 2)
projected_object = Star.translate([0, 4, 150], copy=True).project(1, 10, 10, 1)

clock = pygame.time.Clock()
axis = dict(zip('xyz', [b, g, a]))

while True:
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                hold = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_x: selected = 'x'
            if event.key == pygame.K_y: selected = 'y'
            if event.key == pygame.K_z: selected = 'z'
            if event.key == pygame.K_r:
                axis['x'] = 0
                axis['y'] = 0
                axis['z'] = 0

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:
                axis[selected] += np.pi / 100 * t / 60
                axis[selected] = axis[selected] if axis[selected] < 2 * np.pi else 2 * np.pi
            if event.button == 5:
                axis[selected] -= np.pi / 100 * t / 60
                axis[selected] = axis[selected] if axis[selected] > -2 * np.pi else -2 * np.pi
            if event.button == 1:
                hold = True

    if hold:
        Star = Star.rotateX(axis['x']).rotateY(axis['y']).rotateZ(axis['z'])
        projected_object = Star.translate([0, 4, 150], copy=True).project(1, 10, 10, 1)

    screen.fill((0, 0, 0))
    projected_object.prepare(screen, copy=True).translate([0, Height // 4, 0]).draw(screen)

    data = [
        f'x: β = {axis["x"] / np.pi * 60: .2f} pi/s',
        f'y: γ = {axis["y"] / np.pi * 60: .2f} pi/s',
        f'z: α = {axis["z"] / np.pi * 60: .2f} pi/s'
    ]
    for i, s in enumerate(data):
        color = (255, 255, 255)
        text_surface = font.render(s, False, color)
        screen.blit(text_surface, (240, 20 + i * 25))

    pygame.display.update()
    t = clock.tick(60)