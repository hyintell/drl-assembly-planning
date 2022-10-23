# IMPORT PYGAME AND OPENGL
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
# IMPORT GUI
import sys
import time

"""
Draw site utils
"""

def draw_site(site):
    # Get Center Point Of The Map
    # For good view position
    center_x = len(site.site_3D[0][0]) / 2
    center_y = len(site.site_3D[0]) / 2
    # print("Center X: {}\nCenter Y: {}\nCenter Z:{}".format(center_x,center_y,center_z))

    # Set Cube Size
    Cube_Size = 100
    all_space = False

    # Draw site
    for k in range(len(site.site_3D)):
        # draw ground
        if k == 0:
            for i in range(len(site.site_3D[0])):
                for j in range(len(site.site_3D[0][0])):
                    if site.site_3D[0][i][j] != 50 and site.site_3D[0][i][j] != 'foundation':
                        draw_cube((j - center_x) * Cube_Size, -Cube_Size, (i - center_y) * -Cube_Size, Cube_Size, 10)
                        draw_plane((j - center_x) * Cube_Size, -Cube_Size, (i - center_y) * -Cube_Size, Cube_Size, 10)
                    elif site.site_3D[0][i][j] == 50:
                        draw_cube((j - center_x) * Cube_Size, -Cube_Size, (i - center_y) * -Cube_Size, Cube_Size, 50)
                        draw_plane((j - center_x) * Cube_Size, -Cube_Size, (i - center_y) * -Cube_Size, Cube_Size, 10)
                    elif site.site_3D[0][i][j] == 'foundation':
                        draw_cube((j - center_x) * Cube_Size, -Cube_Size, (i - center_y) * -Cube_Size, Cube_Size, 'foundation')
                        draw_plane((j - center_x) * Cube_Size, -Cube_Size, (i - center_y) * -Cube_Size, Cube_Size, 10)
        # draw component and other
        if k != 0:
            #draw target
            for sco in site.scos:
                draw_plane((sco.y_tar_1 - center_x) * Cube_Size, (sco.z_tar_1 - 1) * Cube_Size,
                           (sco.x_tar_1 - center_y) * -Cube_Size,
                           Cube_Size, 5)
                draw_plane((sco.y_tar_2 - center_x) * Cube_Size, (sco.z_tar_2 - 1) * Cube_Size,
                           (sco.x_tar_2 - center_y) * -Cube_Size,
                           Cube_Size, 5)
                if sco.length > 2:
                    if sco.x_tar_1 > sco.x_tar_2:
                        for x_len in range(abs(sco.x_tar_1 - sco.x_tar_2) - 1):
                            draw_plane((sco.y_tar_2 - center_x) * Cube_Size, (sco.z_tar_2 - 1) * Cube_Size,
                                       (sco.x_tar_2 + x_len + 1 - center_y) * -Cube_Size,
                                       Cube_Size, 5)
                    elif sco.x_tar_2 > sco.x_tar_1:
                        for x_len in range(abs(sco.x_tar_2 - sco.x_tar_1) - 1):
                            draw_plane((sco.y_tar_1 - center_x) * Cube_Size, (sco.z_tar_1 - 1) * Cube_Size,
                                       (sco.x_tar_1 + x_len + 1 - center_y) * -Cube_Size,
                                       Cube_Size, 5)
                    elif sco.y_tar_1 > sco.y_tar_2:
                        for x_len in range(abs(sco.y_tar_1 - sco.y_tar_2) - 1):
                            draw_plane((sco.y_tar_2 + x_len + 1 - center_x) * Cube_Size, (sco.z_tar_2 - 1) * Cube_Size,
                                       (sco.x_tar_2 - center_y) * -Cube_Size,
                                       Cube_Size, 5)
                    elif sco.y_tar_2 > sco.y_tar_1:
                        for x_len in range(abs(sco.y_tar_2 - sco.y_tar_1) - 1):
                            draw_plane((sco.y_tar_1 + x_len + 1 - center_x) * Cube_Size, (sco.z_tar_1 - 1) * Cube_Size,
                                       (sco.x_tar_1 - center_y) * -Cube_Size,
                                       Cube_Size, 5)
                    elif sco.z_tar_1 > sco.z_tar_2:
                        for z_len in range(sco.length - 2):
                            draw_plane((sco.y_tar_1 - center_x) * Cube_Size, (sco.z_tar_2 + z_len) * Cube_Size,
                                       (sco.x_tar_1 - center_y) * -Cube_Size,
                                       Cube_Size, 5)
                    elif sco.z_tar_2 > sco.z_tar_1:
                        for z_len in range(sco.length - 2):
                            draw_plane((sco.y_tar_1 - center_x) * Cube_Size, (sco.z_tar_1 + z_len) * Cube_Size,
                                       (sco.x_tar_1 - center_y) * -Cube_Size,
                                       Cube_Size, 5)

            # draw component
            for i in range(len(site.site_3D[0])):
                for j in range(len(site.site_3D[0][0])):
                    if site.site_3D[k][i][j] == 0:
                        if all_space is True:
                            draw_plane((j - center_x) * Cube_Size, (k-1) * Cube_Size, (i - center_y) * -Cube_Size, Cube_Size, 1)
                    if site.site_3D[k][i][j] == 1:
                        draw_cube((j - center_x) * Cube_Size,  (k-1)*Cube_Size, (i - center_y) * -Cube_Size,
                                   Cube_Size, 1)
                        draw_plane((j - center_x) * Cube_Size, (k - 1) * Cube_Size, (i - center_y) * -Cube_Size,
                                   Cube_Size, 1)
                    if site.site_3D[k][i][j] == 2:
                        draw_cube((j - center_x) * Cube_Size,  (k-1)*Cube_Size, (i - center_y) * -Cube_Size,
                                   Cube_Size, 2)
                        draw_plane((j - center_x) * Cube_Size, (k - 1) * Cube_Size, (i - center_y) * -Cube_Size,
                                   Cube_Size, 2)
                    if site.site_3D[k][i][j] == 100:
                        draw_cube((j - center_x) * Cube_Size,  (k-1)*Cube_Size, (i - center_y) * -Cube_Size,
                                   Cube_Size, 100)
                        draw_plane((j - center_x) * Cube_Size, (k - 1) * Cube_Size, (i - center_y) * -Cube_Size,
                                   Cube_Size, 1)
                    if site.site_3D[k][i][j] == 200:
                        draw_cube((j - center_x) * Cube_Size,  (k-1)*Cube_Size, (i - center_y) * -Cube_Size,
                                   Cube_Size, 200)
                        draw_plane((j - center_x) * Cube_Size, (k - 1) * Cube_Size, (i - center_y) * -Cube_Size,
                                   Cube_Size, 1)

                    # draw fid
                    if site.site_3D[k][i][j] == 'fid':
                        draw_cube((j - center_x) * Cube_Size,  (k-1)*Cube_Size, (i - center_y) * -Cube_Size,
                                   Cube_Size, 'fid')

                    # draw init place
                    if site.site_3D[k][i][j] == 3:
                        draw_plane((j - center_x) * Cube_Size, (k - 1) * Cube_Size, (i - center_y) * -Cube_Size,
                                   Cube_Size, 3)




def draw_cube(centerPosX, centerPosY, centerPosZ, edgeLength,type):
    halfSideLength = edgeLength * 0.5
    vertices = (
        # front face
        centerPosX - halfSideLength, centerPosY + halfSideLength, centerPosZ + halfSideLength,  # top left
        centerPosX + halfSideLength, centerPosY + halfSideLength, centerPosZ + halfSideLength,  # top right
        centerPosX + halfSideLength, centerPosY - halfSideLength, centerPosZ + halfSideLength,  # bottom right
        centerPosX - halfSideLength, centerPosY - halfSideLength, centerPosZ + halfSideLength,  # bottom left

        # back face
        centerPosX - halfSideLength, centerPosY + halfSideLength, centerPosZ - halfSideLength,  # top left
        centerPosX + halfSideLength, centerPosY + halfSideLength, centerPosZ - halfSideLength,  # top right
        centerPosX + halfSideLength, centerPosY - halfSideLength, centerPosZ - halfSideLength,  # bottom right
        centerPosX - halfSideLength, centerPosY - halfSideLength, centerPosZ - halfSideLength,  # bottom left

        # left face
        centerPosX - halfSideLength, centerPosY + halfSideLength, centerPosZ + halfSideLength,  # top left
        centerPosX - halfSideLength, centerPosY + halfSideLength, centerPosZ - halfSideLength,  # top right
        centerPosX - halfSideLength, centerPosY - halfSideLength, centerPosZ - halfSideLength,  # bottom right
        centerPosX - halfSideLength, centerPosY - halfSideLength, centerPosZ + halfSideLength,  # bottom left

        # right face
        centerPosX + halfSideLength, centerPosY + halfSideLength, centerPosZ + halfSideLength,  # top left
        centerPosX + halfSideLength, centerPosY + halfSideLength, centerPosZ - halfSideLength,  # top right
        centerPosX + halfSideLength, centerPosY - halfSideLength, centerPosZ - halfSideLength,  # bottom right
        centerPosX + halfSideLength, centerPosY - halfSideLength, centerPosZ + halfSideLength,  # bottom left

        # top face
        centerPosX - halfSideLength, centerPosY + halfSideLength, centerPosZ + halfSideLength,  # top left
        centerPosX - halfSideLength, centerPosY + halfSideLength, centerPosZ - halfSideLength,  # top right
        centerPosX + halfSideLength, centerPosY + halfSideLength, centerPosZ - halfSideLength,  # bottom right
        centerPosX + halfSideLength, centerPosY + halfSideLength, centerPosZ + halfSideLength,  # bottom left

        # top face
        centerPosX - halfSideLength, centerPosY - halfSideLength, centerPosZ + halfSideLength,  # top left
        centerPosX - halfSideLength, centerPosY - halfSideLength, centerPosZ - halfSideLength,  # top right
        centerPosX + halfSideLength, centerPosY - halfSideLength, centerPosZ - halfSideLength,  # bottom right
        centerPosX + halfSideLength, centerPosY - halfSideLength, centerPosZ + halfSideLength  # bottom left
    )

    # OLD RENDER (POLYGONS)
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

    # NEW RENDER (GL_QUADS)
    glBegin(GL_QUADS)

    if type == 10:
        glColor3f(0.75, 0.75, 0.75)
    elif type == 50:
        glColor3f(0, 0.7, 0.7)
    elif type == 1:
        glColor3f(1, 0.65, 0)
    elif type == 100:
        glColor3f(0, 1, 0)
    elif type == 200:
        glColor3f(1, 0.1, 1)
    elif type == 2:
        glColor3f(0, 0, 1)
    elif type == 'foundation':
        glColor3f(1, 0.5, 1)
    elif type == 'fid':
        glColor3f(0, 0, 0)


    # FOR EVERY VERTICES
    for x in range(24):
        glVertex3f(vertices[x * 3], vertices[x * 3 + 1], vertices[x * 3 + 2])
    glColor3f(0.5, 0.5, 0.5)
    glEnd()



def draw_plane(centerPosX, centerPosY, centerPosZ, edgeLength, type):
    halfSideLength = edgeLength * 0.5
    vertices = (
        # front face
        centerPosX - halfSideLength, centerPosY + halfSideLength, centerPosZ + halfSideLength,  # top left
        centerPosX + halfSideLength, centerPosY + halfSideLength, centerPosZ + halfSideLength,  # top right
        centerPosX + halfSideLength, centerPosY - halfSideLength, centerPosZ + halfSideLength,  # bottom right
        centerPosX - halfSideLength, centerPosY - halfSideLength, centerPosZ + halfSideLength,  # bottom left

        # back face
        centerPosX - halfSideLength, centerPosY + halfSideLength, centerPosZ - halfSideLength,  # top left
        centerPosX + halfSideLength, centerPosY + halfSideLength, centerPosZ - halfSideLength,  # top right
        centerPosX + halfSideLength, centerPosY - halfSideLength, centerPosZ - halfSideLength,  # bottom right
        centerPosX - halfSideLength, centerPosY - halfSideLength, centerPosZ - halfSideLength,  # bottom left

        # left face
        centerPosX - halfSideLength, centerPosY + halfSideLength, centerPosZ + halfSideLength,  # top left
        centerPosX - halfSideLength, centerPosY + halfSideLength, centerPosZ - halfSideLength,  # top right
        centerPosX - halfSideLength, centerPosY - halfSideLength, centerPosZ - halfSideLength,  # bottom right
        centerPosX - halfSideLength, centerPosY - halfSideLength, centerPosZ + halfSideLength,  # bottom left

        # right face
        centerPosX + halfSideLength, centerPosY + halfSideLength, centerPosZ + halfSideLength,  # top left
        centerPosX + halfSideLength, centerPosY + halfSideLength, centerPosZ - halfSideLength,  # top right
        centerPosX + halfSideLength, centerPosY - halfSideLength, centerPosZ - halfSideLength,  # bottom right
        centerPosX + halfSideLength, centerPosY - halfSideLength, centerPosZ + halfSideLength,  # bottom left

        # top face
        centerPosX - halfSideLength, centerPosY + halfSideLength, centerPosZ + halfSideLength,  # top left
        centerPosX - halfSideLength, centerPosY + halfSideLength, centerPosZ - halfSideLength,  # top right
        centerPosX + halfSideLength, centerPosY + halfSideLength, centerPosZ - halfSideLength,  # bottom right
        centerPosX + halfSideLength, centerPosY + halfSideLength, centerPosZ + halfSideLength,  # bottom left

        # top face
        centerPosX - halfSideLength, centerPosY - halfSideLength, centerPosZ + halfSideLength,  # top left
        centerPosX - halfSideLength, centerPosY - halfSideLength, centerPosZ - halfSideLength,  # top right
        centerPosX + halfSideLength, centerPosY - halfSideLength, centerPosZ - halfSideLength,  # bottom right
        centerPosX + halfSideLength, centerPosY - halfSideLength, centerPosZ + halfSideLength  # bottom left
    )

    # OLD RENDER (POLYGONS)
    glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

    if type == 10:
        glLineWidth(2)
        glColor3f(0, 0, 0)
    elif type == 1:
        glLineWidth(0.1)
        glColor3f(0.9, 0.9, 0.9)
        # glLineStipple(10, 0x5555)
    elif type == 3:
        glColor3f(1, 0.65, 0)
    elif type == 5:
        glLineWidth(2)
        glColor3f(1, 0.1, 1)
    elif type == 100:
        glColor3f(0, 1, 0)


    glEnableClientState(GL_VERTEX_ARRAY)
    # glEnable(GL_LINE_STIPPLE)
    glVertexPointer(3, GL_FLOAT, 0, vertices)
    glDrawArrays(GL_QUADS, 0, 24)
    glDisableClientState(GL_VERTEX_ARRAY)