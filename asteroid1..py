#attempt at asteroid-like
from tkinter import *
import random
import math
import time

root = Tk()

WIDTH = 800
HEIGHT = 450
CANVAS_CENTER = (WIDTH / 2, HEIGHT / 2)
INITIAL_VEL = (0, 0)
running = True

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
debris_image = PhotoImage(file = "C:/Users/Michael Cole/Documents/Games/debris2_blue.gif")

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = PhotoImage(file = "C:/Users/Michael Cole/Documents/Games/nebula_blue.gif")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = PhotoImage(file = "C:/Users/Michael Cole/Documents/Games/splash.gif")

# ship image
#ship_thrust_info = ImageInfo([45, 45], [90, 90], 35)
#ship_thrust_image = PhotoImage(file = "C;/Users/Michael Cole/Documents/Games/ship_thrust_image.gif")
#ship_info = ImageInfo([45, 45], [90, 90], 35)
#ship_image = PhotoImage(file = "C:/Users/Michael Cole/Documents/Games/double_ship.gif")
ship_info = ImageInfo([45, 45], [45, 45], 35)
ship_image = PhotoImage(file = "C:/Users/Michael Cole/Documents/Games/ship_image.gif")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, 50)
missile_image = PhotoImage(file = "C:/Users/Michael Cole/Documents/Games/shot2.gif")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = PhotoImage(file = "C:/Users/Michael Cole/Documents/Games/asteroid_blue.gif")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = PhotoImage(file = "C:/Users/Michael Cole/Documents/Games/explosion_alpha.gif")

# sound assets purchased from sounddogs.com, please do not redistribute
#soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = "http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3"
#missile_sound.set_volume(.5)
ship_thrust_sound = "http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3"
explosion_sound = "http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3"

#helper functions
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p,q):
    return math.sqrt((p[0]-q[0])**2+(p[1]-q[1])**2)

# Ship class
class Ship:
    
    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.time = 0
        
    def increment_angle_vel(self):
        self.angle_vel += 0.05
        
    def decrement_angle_vel(self):
        self.angle_vel -= 0.05
        
    def set_thrust(self, on):
        self.thrust = on
    #    if self.thrust:
    #        ship_thrust_sound.rewind()
    #        ship_thrust_sound.play()
    #    else:
    #        ship_thrust_sound.pause()
            
    #def shoot_missile(self):
    #    global a_missile
        
    #    forward = angle_to_vector(self.angle)
    #    missile_pos = [ self.pos[0] + self.radius * forward[0], self.pos[1] + self.radius * forward[1]]
    #    missile_vel = [self.vel[0] + 6 * forward[0], self.vel[1] + 6 * forward[1]]
    #    if not dead:
    #        missile_group.add(Sprite(missile_pos, missile_vel, self.angle, 0, missile_image, missile_info, missile_sound))
        
    #def destroyed(self):
    #    self.time = 0
    #    while self.time < 10:
    #        self.time += 1
    #    self.myship = Ship([width / 2, height / 2], [0, 0], 0, ship_image, ship_info)
        
    def draw(self,canvas):
        self.canvas = canvas
        #canvas.create_oval(self.pos, (self.pos[0] + self.radius, self.pos[1] + self.radius),
        #                  fill = 'white')
        #if self.thrust:
        #    canvas.create_image([self.image_center[0] + self.image_size[0],
        #                                   self.image_center[1]], image = self.image, anchor = CENTER)
        #else:
        self.canvas.create_image((self.pos[0], self.pos[1]), image = self.image, tag = 'ship')
        
    def update(self):        
        #update angle
        self.angle += self.angle_vel
        
        #update pos
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT
        
        #update velocity
        acc = angle_to_vector(self.angle)
        if self.thrust:
            self.vel[0] += acc[0] * 0.1
            self.vel[1] += acc[1] * 0.1
        else: #decelerate
            self.vel[0] *= 0.99
            self.vel[1] *= 0.99

def keypress(event):
    if event.keysym == 'Up':
        ship.set_thrust(True)
    if event.keysym == 'Left':
        ship.decrement_angle_vel()
    if event.keysym == 'Right':
        ship.increment_angle_vel()
    if event.keysym == 'Space':
        pass
    
def keyrelease(event):
    if event.keysym == 'Up':
        ship.set_thrust(False)
    if event.keysym == 'Left':
        ship.increment_angle_vel()
    if event.keysym == 'Right':
        ship.decrement_angle_vel()
    if event.keysym == 'Space':
        pass
    
def draw(canvas):
    while running:
        time.sleep(0.01)
        ship.update()
        canvas.move(ship.canvas.gettags('ship'), 5, 5)
        canvas.update()
    else:
        quit()
        
frame = Frame(root)
frame.grid()
canvas = Canvas(frame, width = WIDTH, height = HEIGHT)
canvas.grid()

root.bind("<KeyPress>", keypress)
root.bind("<KeyRelease>", keyrelease)

ship = Ship(CANVAS_CENTER, INITIAL_VEL, 0, ship_image, ship_info)
ship.draw(canvas)

draw(canvas)

root.mainloop()
