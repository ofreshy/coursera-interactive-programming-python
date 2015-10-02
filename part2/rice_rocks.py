# CodeSkulptor http://www.codeskulptor.org/#user40_l1Lu6kXBscQC188.py

# program template for Spaceship
import simplegui
import math
import random

# globals for user interface
WIDTH = 800
HEIGHT = 600
score = 0
lives = 3
time = 0
game_on = False

# globals for contorls
TURN_LEFT = simplegui.KEY_MAP["left"]
TURN_RIGHT = simplegui.KEY_MAP["right"]
THRUST = simplegui.KEY_MAP["up"]
BREAKS = simplegui.KEY_MAP["down"]
FRICTION = 0.99
ACCELERATION = 0.25

# Rocks and Missles
MAX_ROCKS = 10
rock_group = set()

MAX_MISSILES = 100
MISSILE_LIFESPAN = 75
missile_group = set()

# Enhacemnet, a bigger missile that
# travels faster, live longer and does not dissipiate when
# hit a rock. Press 's' to launch
SUPER_MISSILE_LIFESPAN = 100
SUPER_MISSILE_REBIRTH = 200
super_missile = True
super_missile_group = set()


explosion_group = set()


class ImageInfo:
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated


# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim

# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.f2014.png")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, MISSILE_LIFESPAN)
super_missile_info = ImageInfo([10,10], [15, 15], 3, MISSILE_LIFESPAN * 2)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")
super_missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot3.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

# sound assets purchased from sounddogs.com, please do not redistribute
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")

# helper functions to handle transformations
def dist(p,q):
    return math.sqrt((p[0] - q[0]) ** 2+(p[1] - q[1]) ** 2)

# returns true if the two objects collide,
# false otherwise
# objects must have pos attribute and a radius attribute
def collide(obj1, obj2, radius=0):
    # distance between centres
    centre_dist = dist(obj1.pos, obj2.pos)
    # collison happens when distance between the centres
    # is smaller or equal to sum of radiuses
    return centre_dist - (obj1.radius + obj2.radius + radius) <= 0

# Returns the sets of colliders in group1 and group2
def get_colliders(obj_group1, obj_group2, r=0):
    colliders_group1 , colliders_group2 = set(), set()
    for o1 in obj_group1:
        for o2 in obj_group2:
            if collide(o1, o2, r):
                colliders_group1.add(o1)
                colliders_group2.add(o2)
    return colliders_group1, colliders_group2

# process sprite group
def process_sprite_group(sprite_group, canvas):
    diers = [s for s in sprite_group if s.update()]
    sprite_group.difference_update(diers)
    [s.draw(canvas) for s in sprite_group]

def add_explosions(explosions, rock_colliders):
    for r in rock_colliders:
        explosions.add(build_explosion(r.pos))

# A step function to control the speed of the rocks
# bases on the game score
def ang_vel_from_time():
    if score < 25:
        return (random.random() + 0.1 ) / 50.0
    if time < 45:
        return (random.random() + 0.1 ) / 25.0
    if time < 60:
        return (random.random() + 0.1 ) / 15.0
    if time < 70:
        return (random.random() + 0.1 ) / 10.0
    if time < 80:
        return (random.random() + 0.1 ) / 7.0
    return (random.random() + 0.1 ) / 5.0


# Ship class
class Ship:
    def __init__(self, pos, vel, angle, image, info, sound):
        self.pos = pos[0], pos[1]
        self.vel = vel[0], vel[1]
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.image_center = info.get_center()
        self.no_thrust_image_center = info.get_center()
        self.thrust_image_center = info.get_center()[0] + info.get_size()[0], info.get_center()[1]
        self.thrust = False
        self.breaks = False
        self.thrust_sound = sound
        self.thrust_sound.rewind()


    def draw(self,canvas):
        canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)

    def turn_left(self, radian=0.1):
        self.angle_vel -= radian

    def turn_right(self, radian=0.1):
        self.angle_vel += radian

    def stop_turn(self):
        self.angle_vel = 0

    def thrust_on(self):
        self.thrust = True
        self.breaks = False
        self.image_center = self.thrust_image_center
        self.thrust_sound.play()

    def thrust_off(self):
        self.thrust = False
        self.image_center = self.no_thrust_image_center
        self.thrust_sound.rewind()

    def breaks_on(self):
        self.breaks = True
        self.thrust = False

    def breaks_off(self):
        self.breaks = False

    def shoot(self):
        if len(missile_group) >= MAX_MISSILES:
            return

        x = math.cos(self.angle) * self.radius
        y = math.sin(self.angle) * self.radius
        missile_vel = self.vel[0] + ACCELERATION * 20 * math.cos(self.angle), self.vel[1] + ACCELERATION * 20 * math.sin(self.angle)
        missle_pos = self.pos[0] + x, self.pos[1] + y
        missile_group.add(build_missile(missle_pos, missile_vel) )

    def shoot_super_missile(self):
        if len(super_missile_group) >= 1:
            return

        x = math.cos(self.angle) * self.radius
        y = math.sin(self.angle) * self.radius
        missile_vel = self.vel[0] + ACCELERATION * 50 * math.cos(self.angle), self.vel[1] + ACCELERATION * 50 * math.sin(self.angle)
        missle_pos = self.pos[0] + x, self.pos[1] + y
        super_missile_group.add(build_super_missile(missle_pos, missile_vel, self.angle) )



    def update(self):
        self.pos = (self.pos[0] + self.vel[0]) % WIDTH, (self.pos[1] + self.vel[1]    ) % HEIGHT

        self.angle += self.angle_vel

        self.vel = self.vel[0] * FRICTION, self.vel[1] * FRICTION
        if self.thrust:
            self.vel = self.vel[0] + ACCELERATION * math.cos(self.angle), self.vel[1] + ACCELERATION * math.sin(self.angle)
        if self.vel > 0 and self.breaks:
            self.vel = self.vel[0] * 0.95, self.vel[1] * 0.95



# Sprite class
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
        self.pos = pos[0], pos[1]
        self.vel = vel[0], vel[1]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.age = 0
        self.animated = info.get_animated()
        self.age = 0
        if sound:
            sound.rewind()
            sound.play()

    def draw(self, canvas):
        if self.animated:
            image_center = self.image_center[0] + self.image_size[0] * self.age, self.image_center[1]
        else:
            image_center = self.image_center
        canvas.draw_image(self.image, image_center, self.image_size, self.pos, self.image_size, self.angle)

    def update(self):
        self.pos = (self.pos[0] + self.vel[0]) % WIDTH, (self.pos[1] + self.vel[1]    ) % HEIGHT
        self.angle += self.angle_vel
        self.age += 1
        return self.age > self.lifespan


def draw(canvas):
    global game_on, time, lives, score, super_missile, rock_group, missile_group
    if not game_on:
        canvas.draw_image(splash_image, splash_info.get_center(), splash_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
        return

    # animiate background
    time += 1
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))

    if time % SUPER_MISSILE_REBIRTH == 0:
        super_missile = True

    # update ship
    my_ship.update()
    # update and draw rocks
    process_sprite_group(rock_group, canvas)
    # update and draw missiles
    process_sprite_group(missile_group, canvas)
    # update and draw super missiles
    process_sprite_group(super_missile_group, canvas)
    # update and draw explosions
    process_sprite_group(explosion_group, canvas)

    # draw ship
    my_ship.draw(canvas)

    # COLLISIONS
    #missiles with rocks
    collided_rocks_a, collided_missiles = get_colliders(rock_group, missile_group)
    collided_rocks_b, super_missiles = get_colliders(rock_group, super_missile_group, 20)
    collided_rocks = collided_rocks_a.union(collided_rocks_b)
    if collided_rocks:
        add_explosions(explosion_group, collided_rocks)
        score += len(collided_rocks)
        rock_group.difference_update(collided_rocks)
        missile_group.difference_update(collided_missiles)
        if score % 50 == 0:
            lives += 1
    # ship with rock
    collided_rocks, _ = get_colliders(rock_group, [my_ship])
    if collided_rocks:
        add_explosions(explosion_group, collided_rocks)
        lives -= 1
        if lives == 0:
            game_on = False
            return
        reset()

    #update the score and lives
    canvas.draw_text("lives : %s" % lives, (25, 25), 24, "White", "serif")
    canvas.draw_text("score : %s" % score, (WIDTH-100, 25), 24, "White", "serif")
    canvas.draw_text("superM : %s" % int(super_missile), (WIDTH-450, 25), 24, "White", "serif")



# timer handler that spawns a rock
def rock_spawner():
    global rock_group
    if len(rock_group) >= MAX_ROCKS:
        return

    pos = [WIDTH / random.random() * WIDTH, HEIGHT / random.random() * HEIGHT]
    # between 0.02 to 0.11
    ang_vel = ang_vel_from_time()
    # velocity should correspond to the angular velocity
    values = random.randrange(3)
    x_vel = ang_vel * (random.random() * 3 + 10) * (1 if random.randrange(2) == 1 else -1) * (0 if random.random() < 0.05 else 1)
    y_vel = ang_vel * (random.random() * 3 + 10) * (1 if random.randrange(2) == 1 else -1) * (0 if random.random() < 0.05 else 1)

    a_rock = build_rock(pos, ang_vel, (x_vel, y_vel))
    collided = collide(a_rock, my_ship, my_ship.radius * 5)
    if not collided:
        rock_group.add(a_rock)



def build_rock(pos, ang_vel, vel):
    return Sprite(
        pos=pos,
        vel=vel,
        ang=0,
        ang_vel=ang_vel,
        image=asteroid_image,
        info=asteroid_info)

def build_missile(pos, vel):
    return Sprite(pos=pos,
                  vel=vel,
                  ang=0,
                  ang_vel=0,
                  image=missile_image,
                  info=missile_info,
                  sound=missile_sound)


def build_super_missile(pos, vel, ang):
    return Sprite(pos=pos,
                  vel=vel,
                  ang=ang,
                  ang_vel=0,
                  image=super_missile_image,
                  info=super_missile_info,
                  sound=missile_sound)


def build_explosion(pos):
    return Sprite(pos=pos,
                  vel=(0,0),
                  ang=0,
                  ang_vel=0,
                  image=explosion_image,
                  info=explosion_info,
                  sound=explosion_sound)



def keydown(key):
    if not game_on:
        return

    global super_missile

    if key == TURN_LEFT:
        my_ship.turn_left()
    elif key == TURN_RIGHT:
        my_ship.turn_right()
    elif key == THRUST:
        my_ship.thrust_on()
    elif key == BREAKS:
        my_ship.breaks_on()
    elif key == simplegui.KEY_MAP["space"]:
        my_ship.shoot()
    elif key == simplegui.KEY_MAP["s"] and super_missile:
        super_missile = False
        my_ship.shoot_super_missile()



def keyup(key):
    if not game_on:
        return
    if key in (TURN_LEFT, TURN_RIGHT):
        my_ship.stop_turn()
    elif key == THRUST:
        my_ship.thrust_off()
    elif key == BREAKS:
        my_ship.breaks_off()

def mouseclick(pos):
    global game_on
    if not game_on:
        game_on = True
        new_game()

# resets ship to centre, and clears all rocks and misslies
def reset():
    global rock_group, missile_group, explosion_group, my_ship, super_missle
    rock_group, missile_group, super_missile_group, explosion_group = set(), set(), set(), set()
    my_ship = Ship((WIDTH / 2, HEIGHT / 2), (0, 0), 0, ship_image, ship_info, ship_thrust_sound)
    super_missile = True

def new_game():
    global score, lives, time
    soundtrack.rewind()
    soundtrack.play()
    score, time, lives = 0, 0, 3
    reset()




# initialize frame
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.set_mouseclick_handler(mouseclick)

# initialize game
my_ship = Ship((WIDTH / 2, HEIGHT / 2), (0, 0), 0, ship_image, ship_info, ship_thrust_sound)


# register handlers
frame.set_draw_handler(draw)

timer = simplegui.create_timer(1000.0, rock_spawner)

# get things rolling
timer.start()
frame.start()
