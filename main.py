import pygame as pg
import pymunk as pm
import pymunk.pygame_util

RES = WIDTH, HEIGHT = 900, 600
FPS = 60

SIDE_LENGTH_OF_SMALL_SQUARE, MASS_OF_SMALL_SQUARE = 50, 1
SIDE_LENGTH_OF_BIG_SQUARE, MASS_OF_BIG_SQUARE = 100, 1
VELOCITY_OF_SMALL_SQUARE = (0, 0)
VELOCITY_OF_BIG_SQUARE = (-100 * MASS_OF_BIG_SQUARE, 0)

THICKNESS_OF_STATIC_SEGMENTS = 2

FRICTION = 0

def game():
    # little_square = Square(SIDE_LENGTH_OF_SMALL_SQUARE, 100 + THICKNESS_OF_STATIC_SEGMENTS, SIDE_LENGTH_OF_SMALL_SQUARE/2 + THICKNESS_OF_STATIC_SEGMENTS, 1, VELOCITY_OF_SMALL_SQUARE, MASS_OF_SMALL_SQUARE)
    # big_square = Square(SIDE_LENGTH_OF_BIG_SQUARE, SIDE_LENGTH_OF_BIG_SQUARE/2 + WIDTH - SIDE_LENGTH_OF_BIG_SQUARE, SIDE_LENGTH_OF_BIG_SQUARE/2 + THICKNESS_OF_STATIC_SEGMENTS, 2, VELOCITY_OF_BIG_SQUARE, MASS_OF_BIG_SQUARE)

    little_square = Square(SIDE_LENGTH_OF_SMALL_SQUARE, 100, SIDE_LENGTH_OF_SMALL_SQUARE/2, 1, VELOCITY_OF_SMALL_SQUARE, MASS_OF_SMALL_SQUARE)
    big_square = Square(SIDE_LENGTH_OF_BIG_SQUARE, 500, SIDE_LENGTH_OF_BIG_SQUARE/2, 2, VELOCITY_OF_BIG_SQUARE, MASS_OF_BIG_SQUARE)
    left_wall = VerticalStaticSegment((0, 0), (0, HEIGHT), THICKNESS_OF_STATIC_SEGMENTS, 3)
    floor = HorizontalStaticSegment((0, 0), (WIDTH, 0), THICKNESS_OF_STATIC_SEGMENTS, 4)
    big_square.move()


    handler = space.add_collision_handler(1, 2)
    handler2 = space.add_collision_handler(3, 1)
    handler.begin = collide
    handler2.begin = collide


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

def collide(arbiter, space, data):
    global number_of_collisions
    number_of_collisions += 1
    print(number_of_collisions)

    return True

class Square():
    def __init__(self, side_length, coordinate_x, coordinate_y, collision_type, velocity, mass):
        moment = pm.moment_for_box(mass, (side_length, side_length))
        self.body = pm.Body(mass, moment)
        self.body.position = convert_coordinates((coordinate_x, coordinate_y))
        self.body.velocity = velocity

        self.shape = pm.Poly.create_box(self.body, size=(side_length, side_length))
        self.shape.elasticity = 1
        self.shape.friction = FRICTION
        self.shape.density = 1
        self.shape.collision_type = collision_type

        space.add(self.body, self.shape)

    @staticmethod
    def draw():
        space.debug_draw(draw_options)

    def move(self):
        self.body.apply_impulse_at_world_point(self.body.velocity, self.body.position)

class HorizontalStaticSegment():
    def __init__(self, start, end, thickness, collision_type):
        self.body = pm.Body(body_type=pm.Body.STATIC)
        self.shape = pm.Segment(self.body, convert_coordinates(start), convert_coordinates(end), thickness)
        self.shape.elasticity = 0
        self.shape.friction = 0
        self.shape.collision_type = collision_type

        space.add(self.body, self.shape)

class VerticalStaticSegment():
    def __init__(self, start, end, thickness, collision_type):
        self.body = pm.Body(body_type=pm.Body.STATIC)
        self.shape = pm.Segment(self.body, convert_coordinates(start), convert_coordinates(end), thickness)
        self.shape.elasticity = 1
        self.shape.friction = 0
        self.shape.collision_type = collision_type

        space.add(self.body, self.shape)


pg.init()
display = pg.display.set_mode(RES)
clock = pg.time.Clock()
space = pm.Space()
space.gravity = (0, 30000)
draw_options = pm.pygame_util.DrawOptions(display)

number_of_collisions = 0
game()
