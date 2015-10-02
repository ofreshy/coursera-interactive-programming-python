# codeskulptor link : http://www.codeskulptor.org/#user40_l1Lu6kXBscQC188.py
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

# globals for contorls
TURN_LEFT = simplegui.KEY_MAP["left"]
TURN_RIGHT = simplegui.KEY_MAP["right"]
THRUST = simplegui.KEY_MAP["up"]
FRICTION = 0.99
ACCELERATION = 0.25

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
missile_info = ImageInfo([5,5], [10, 10], 3, 50)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")

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
        self.image_center = self.thrust_image_center
        self.thrust_sound.play()

    def thrust_off(self):
        self.thrust = False
        self.image_center = self.no_thrust_image_center
        self.thrust_sound.rewind()

    def shoot(self):
        global a_missile
        x = math.cos(self.angle) * self.radius
        y = math.sin(self.angle) * self.radius
        missile_vel = self.vel[0] + ACCELERATION * 10 * math.cos(self.angle), self.vel[1] + ACCELERATION * 10 * math.sin(self.angle)
        missle_pos = self.pos[0] + x, self.pos[1] + y
        a_missile = build_missile(missle_pos, missile_vel)

    def update(self):
        self.pos = (self.pos[0] + self.vel[0]) % WIDTH, (self.pos[1] + self.vel[1]    ) % HEIGHT

        self.angle += self.angle_vel

        self.vel = self.vel[0] * FRICTION, self.vel[1] * FRICTION
        if self.thrust:
            self.vel = self.vel[0] + ACCELERATION * math.cos(self.angle), self.vel[1] + ACCELERATION * math.sin(self.angle)




# Sprite class
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
        self.pos = pos[0], pos[1]
        self.vel = vel[0],vel[1]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        if sound:
            sound.rewind()
            sound.play()

    def draw(self, canvas):
        canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)

    def update(self):
        self.pos = (self.pos[0] + self.vel[0]) % WIDTH, (self.pos[1] + self.vel[1]    ) % HEIGHT
        self.angle += self.angle_vel


def draw(canvas):
    global time

    # animiate background
    time += 1
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))

    # draw ship and sprites
    my_ship.draw(canvas)
    a_rock.draw(canvas)
    a_missile.draw(canvas)

    # update ship and sprites
    my_ship.update()
    a_rock.update()
    a_missile.update()

    #update the score and lives
    canvas.draw_text("lives : %s" % lives, (25, 25), 24, "White", "serif")
    canvas.draw_text("score : %s" % score, (WIDTH-100, 25), 24, "White", "serif")

# timer handler that spawns a rock
def rock_spawner():
    global a_rock

    pos = [WIDTH / random.random() * WIDTH, HEIGHT / random.random() * HEIGHT]
    # between 0.02 to 0.21
    ang_vel = (random.random() + 0.1 ) / 5.0
    # velocity should correspond to the angular velocity
    values = random.randrange(3)
    x_vel = ang_vel * (random.random() * 3 + 10) * (1 if random.randrange(2) == 1 else -1) * (0 if random.random() < 0.05 else 1)
    y_vel = ang_vel * (random.random() * 3 + 10) * (1 if random.randrange(2) == 1 else -1) * (0 if random.random() < 0.05 else 1)

    a_rock = build_rock(pos, ang_vel, (x_vel, y_vel))

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


def keydown(key):
    if key == TURN_LEFT:
        my_ship.turn_left()
    elif key == TURN_RIGHT:
        my_ship.turn_right()
    elif key == THRUST:
        my_ship.thrust_on()
    elif key == simplegui.KEY_MAP["space"]:
        my_ship.shoot()


def keyup(key):
    if key in (TURN_LEFT, TURN_RIGHT):
        my_ship.stop_turn()
    elif key == THRUST:
        my_ship.thrust_off()



# initialize frame
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)


# initialize ship and two sprites
my_ship = Ship((WIDTH / 2, HEIGHT / 2), (0, 0), 0, ship_image, ship_info, ship_thrust_sound)
a_rock = build_rock((WIDTH / 3, HEIGHT / 3), 0.1, (1, -1))
my_ship.shoot()

# register handlers
frame.set_draw_handler(draw)

timer = simplegui.create_timer(1000.0, rock_spawner)

# get things rolling
timer.start()
frame.start()
