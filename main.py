import pygame as pg
import pymunk as pm
import pymunk.pygame_util

RES = WIDTH, HEIGHT = 900, 600
FPS = 60
SIDE_LENGTH_OF_SMALL_SQUARE = 50
SIDE_LENGTH_OF_BIG_SQUARE = 100
VELOCITY_OF_SMALL_SQUARE = (0, 0)
VELOCITY_OF_BIG_SQUARE = (-500, 0)
MASS_OF_SMALL_SQUARE = 1
MASS_OF_BIG_SQUARE = 10000


THICKNESS_OF_STATIC_SEGMENTS = 5

def game():
    little_square = Square(SIDE_LENGTH_OF_SMALL_SQUARE, SIDE_LENGTH_OF_SMALL_SQUARE/2 + THICKNESS_OF_STATIC_SEGMENTS, SIDE_LENGTH_OF_SMALL_SQUARE/2 + THICKNESS_OF_STATIC_SEGMENTS, 1, VELOCITY_OF_SMALL_SQUARE, MASS_OF_SMALL_SQUARE)
    big_square = Square(SIDE_LENGTH_OF_BIG_SQUARE, SIDE_LENGTH_OF_BIG_SQUARE/2 + WIDTH - SIDE_LENGTH_OF_BIG_SQUARE, SIDE_LENGTH_OF_BIG_SQUARE/2 + THICKNESS_OF_STATIC_SEGMENTS, 1, VELOCITY_OF_BIG_SQUARE, MASS_OF_BIG_SQUARE)
    left_wall = StaticSegment((0, 0), (0, HEIGHT), THICKNESS_OF_STATIC_SEGMENTS)
    floor = StaticSegment((0, 0), (WIDTH, 0), THICKNESS_OF_STATIC_SEGMENTS)

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return
        display.fill((255, 255, 255))
        little_square.draw()
        big_square.draw()

        pg.display.update()
        clock.tick(FPS)
        space.step(1/FPS)


def convert_coordinates(point):
    return int(point[0]), HEIGHT-int(point[1])


class Square():
    def __init__(self, side_length, coordinate_x, coordinate_y, collision_type, velocity, mass):
        self.body = pm.Body()
        self.body.position = convert_coordinates((coordinate_x, coordinate_y))
        self.body.velocity = velocity

        self.shape = pm.Poly.create_box(self.body, (side_length, side_length))
        self.shape.elasticity = 1
        # what is density?
        self.shape.density = 1
        self.shape.collision_type = collision_type

        space.add(self.body, self.shape)

    @staticmethod
    def draw():
        space.debug_draw(draw_options)


class StaticSegment():
    def __init__(self, start, end, thickness):
        self.body = pm.Body(body_type=pm.Body.STATIC)
        self.shape = pm.Segment(self.body, convert_coordinates(start), convert_coordinates(end), thickness)

        space.add(self.body, self.shape)


pg.init()
display = pg.display.set_mode(RES)
clock = pg.time.Clock()
space = pm.Space()
draw_options = pm.pygame_util.DrawOptions(display)
game()
