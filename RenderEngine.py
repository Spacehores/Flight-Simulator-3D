import math

import numpy as np
from numpy import array
import pygame
import Noise
import MyMath
import time

far_plane = 20
near_plane = 0.1
width = 1800
height = 950
display = pygame.display.set_mode(size=(width, height))

delta = 1
last_frame_time = time.time()
last_second_time = time.time()
frames_current_second = 0
frames_last_second = 0


class Polygon_2D:
    def __init__(self, vertices, color, depth):
        self.vertices = vertices
        self.color = color
        self.depth = depth


class Camera:
    def __init__(self):
        self.position = array([0.0, 0.0, 0.0])
        self.rotation_matrix = np.identity(4)

    def rotate(self, rotation):
        rotation = np.append(rotation, 1.0)
        rotation = rotation @ self.rotation_matrix
        self.rotation_matrix = self.rotation_matrix @ MyMath.createRotationMatrix(rotation)


camera = Camera()

view_matrix = MyMath.createViewMatrix(camera)
projection_matrix = MyMath.createProjectionMatrix(near_plane, far_plane, display.get_width(), display.get_height())


def update():
    global view_matrix
    view_matrix = MyMath.createViewMatrix(camera)
    calcDelta()


def render(models, player):
    polygons = []
    day_color = array([178, 255, 255])
    night_color = array([11, 16, 38])
    time_factor = ((math.sin(time.time())+1)*0.5)
    sky_color = MyMath.lerp(time_factor, day_color, night_color)

    viewport = pygame.Rect(0, 0, display.get_width(), display.get_height())

    display.fill(sky_color, rect=viewport)

    for model in models:
        for i in range(int(len(model.transformed_vertices) / 3)):
            v1 = fromWorldToScreen(model.transformed_vertices[i * 3 + 0])
            v2 = fromWorldToScreen(model.transformed_vertices[i * 3 + 1])
            v3 = fromWorldToScreen(model.transformed_vertices[i * 3 + 2])
            depth = (v1[2] + v2[2] + v3[2]) / 3
            if v1[2] < near_plane or v2[2] < near_plane or v3[2] < near_plane:
                continue
            else:
                vertices = array([v1[0:2], v2[0:2], v3[0:2]])
                polygons.append(Polygon_2D(vertices, model.last_calculated_colors[i], depth))

    polygons.sort(key=lambda x: x.depth, reverse= True)

    for polygon in polygons:
        #inverterat y-axeln
        polygon.vertices[0][1] = height - polygon.vertices[0][1]
        polygon.vertices[1][1] = height - polygon.vertices[1][1]
        polygon.vertices[2][1] = height - polygon.vertices[2][1]

        fog = (far_plane-polygon.depth)/(far_plane-far_plane*0.5)
        fog = pygame.math.clamp(fog, 0, 1)
        color = MyMath.lerp(1-fog, polygon.color, sky_color)
        color[0] =pygame.math.clamp(color[0], 0, 255)
        color[1] =pygame.math.clamp(color[1], 0, 255)
        color[2] =pygame.math.clamp(color[2], 0, 255)

        pygame.draw.polygon(display, color, polygon.vertices)
        # pygame.gfxdraw.filled_polygon(display, polygon.vertices, polygon.color,)


    #drawMap(array([int(width / 2), int(height)]), player)

    pygame.display.update()


def calcDelta():
    global last_frame_time
    global last_second_time
    global frames_current_second
    global delta
    current_frame_time = time.time()
    delta = current_frame_time - last_frame_time
    if time.time() - last_second_time >= 1:
        global frames_last_second
        frames_last_second = frames_current_second
        last_second_time = current_frame_time
        frames_current_second = 0
        pygame.display.set_caption("Flight-Simulator-3D " + frames_last_second.__str__() + "fps")
    frames_current_second += 1
    last_frame_time = current_frame_time

map_resolution = 50
surface = pygame.Surface((map_resolution, map_resolution))
i = 0
def drawMap(position_screen, player):
    r = int(map_resolution / 2)
    global surface
    zoom_out = 0.35

    forward = np.append(player.model.position+array([0, 0, 1]), 1.0)@player.model.rotation_matrix
    dx = forward[0]-player.model.position[0]
    dz = forward[2]-player.model.position[2]
    angle_y = np.arctan2(dx, dz)

    for x in range(-r, r, 1):
        for y in range(-r, r, 1):
            noise_x = (x * zoom_out + player.model.position[0])
            noise_y = (y * zoom_out + player.model.position[2])
            rotated = array([noise_x, 0, noise_y, 1.0]) @ MyMath.createRotationMatrix([0, angle_y+math.pi/2, 0])
            height = Noise.noiseFunction(rotated[0], rotated[2])
            color = array([0, 255, 0])
            if height <= 0:
                color = array([0, 0, 255])
            if height >= 1.2:
                color = array([255, 255, 255])

            color = color * ((height / 10) + 0.5)
            color[0] = pygame.math.clamp(color[0], 0, 255)
            color[1] = pygame.math.clamp(color[1], 0, 255)
            color[2] = pygame.math.clamp(color[2], 0, 255)


            surface.set_at((r +x , r+y), color)


    display.blit(surface, (position_screen[0]-r, position_screen[1]-map_resolution))

def fromWorldToScreen(point_3D):
    clipspace_position = projection_matrix @ view_matrix @ point_3D
    if clipspace_position[3] == 0: clipspace_position[3] = 0.00001
    NDC_space = clipspace_position[0:2] / clipspace_position[3]
    x = ((NDC_space[0] + 1) / 2) * display.get_width()
    y = ((NDC_space[1] + 1) / 2) * display.get_height()
    screen_space = array([x, y, clipspace_position[2]])
    return screen_space
