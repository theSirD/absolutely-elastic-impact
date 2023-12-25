import pygame as pg
import pymunk as pm
import pymunk.pygame_util

RES = WIDTH, HEIGHT = 900, 600
FPS = 60

SIDE_LENGTH_OF_SMALL_SQUARE, MASS_OF_SMALL_SQUARE = 50, 1
SIDE_LENGTH_OF_BIG_SQUARE, MASS_OF_BIG_SQUARE = 100, 10
VELOCITY_OF_SMALL_SQUARE = (0, 0)
VELOCITY_OF_BIG_SQUARE = (-100 * MASS_OF_BIG_SQUARE, 0)


THICKNESS_OF_STATIC_SEGMENTS = 100

FRICTION = 0


def convert_coordinates(point):
    return int(point[0]), HEIGHT-int(point[1])


def collide(arbiter, space, data):
    global number_of_collisions
    number_of_collisions += 1
    print(number_of_collisions)

    return True


# setting of scene
pg.init()
display = pg.display.set_mode(RES)
clock = pg.time.Clock()
space = pm.Space()
space.gravity = (0, 30000)
draw_options = pm.pygame_util.DrawOptions(display)


floor_body = pm.Body(body_type=pm.Body.STATIC)
floor_shape = pymunk.Segment(floor_body, convert_coordinates((0, 0)), convert_coordinates((WIDTH, 0)), THICKNESS_OF_STATIC_SEGMENTS)
floor_shape.elasticity = 0
floor_shape.friction = FRICTION
floor_shape.collision_type = 4

space.add(floor_body, floor_shape)

wall_body = pm.Body(body_type=pm.Body.STATIC)
wall_shape = pymunk.Segment(wall_body, convert_coordinates((0, 0)), convert_coordinates((0, HEIGHT)), THICKNESS_OF_STATIC_SEGMENTS)
wall_shape.elasticity = 1
wall_shape.friction = 0
wall_shape.collision_type = 3
space.add(wall_body, wall_shape)


# small square
small_sqaure_moment = pymunk.moment_for_box(MASS_OF_SMALL_SQUARE, (SIDE_LENGTH_OF_SMALL_SQUARE, SIDE_LENGTH_OF_SMALL_SQUARE))
small_sqaure_body = pymunk.Body(MASS_OF_SMALL_SQUARE, small_sqaure_moment)

small_sqaure_body.position = convert_coordinates((300, THICKNESS_OF_STATIC_SEGMENTS + small_sqaure_moment))
small_sqaure_shape = pymunk.Poly.create_box(small_sqaure_body, (SIDE_LENGTH_OF_SMALL_SQUARE, SIDE_LENGTH_OF_SMALL_SQUARE))
small_sqaure_shape.collision_type = 1
small_sqaure_shape.elasticity = 1
small_sqaure_shape.friction = 0

small_sqaure_body.apply_impulse_at_world_point(VELOCITY_OF_SMALL_SQUARE, small_sqaure_body.position)

space.add(small_sqaure_body, small_sqaure_shape)


#big square
big_square_moment = pymunk.moment_for_box(MASS_OF_BIG_SQUARE, (SIDE_LENGTH_OF_BIG_SQUARE, SIDE_LENGTH_OF_BIG_SQUARE))
big_square_body = pymunk.Body(MASS_OF_BIG_SQUARE, big_square_moment)

big_square_body.position = convert_coordinates((500, 10))
big_square_shape = pymunk.Poly.create_box(big_square_body, (SIDE_LENGTH_OF_BIG_SQUARE, SIDE_LENGTH_OF_BIG_SQUARE))
big_square_shape.collision_type = 2
big_square_shape.elasticity = 1
big_square_shape.friction = 0

big_square_body.apply_impulse_at_world_point(VELOCITY_OF_BIG_SQUARE, big_square_body.position)

space.add(big_square_body, big_square_shape)

# start action
number_of_collisions = 0
handler = space.add_collision_handler(1, 2)
handler2 = space.add_collision_handler(3, 1)
handler.begin = collide
handler2.begin = collide


while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            exit()

    display.fill((255, 255, 255))
    space.debug_draw(draw_options)
    pg.display.update()
    clock.tick(FPS)
    space.step(1/FPS)
