"""A very basic pinball game.
"""
__version__ = "$Id:$"
__docformat__ = "reStructuredText"

import random,datetime,time,os,sys
import pygame,pymunk,pyautogui
import pymunk.pygame_util
from pygame import mixer
from pymunk import Vec2d
mixer.init()
global score
score = 0
script_name = os.path.basename(__file__) #sys.argv[0].split('/')[-1]

pygame.init()
screen = pygame.display.set_mode((600, 600))

#pygame.font.init()
#my_font = pygame.font.SysFont('Comic Sans MS', 30)
#text_surface = my_font.render('Some Text', True, (0, 255, 0))
#screen.blit(text_surface, (100,100))

# Clear screen
#screen.fill(pygame.Color("white"))

clock = pygame.time.Clock()
running = True

### Physics stuff
space = pymunk.Space()
space.gravity = (0.0, 900.0)
draw_options = pymunk.pygame_util.DrawOptions(screen)

## Balls
balls = []

### walls
static_lines = [
    pymunk.Segment(space.static_body, (120, 480), (50, 50), 2.0),
    pymunk.Segment(space.static_body, (480, 480), (545, 110), 2.0),
    pymunk.Segment(space.static_body, (50, 50), (300, 0), 2.0),
    pymunk.Segment(space.static_body, (300, 0), (550, 50), 2.0),
    pymunk.Segment(space.static_body, (510,480), (580,90), 2.0),
    pymunk.Segment(space.static_body, (580,90), (550,50), 2.0),
    pymunk.Segment(space.static_body, (480,480), (510,480), 2.0),
    pymunk.Segment(space.static_body, (120,480), (140,500), 4.0),
    pymunk.Segment(space.static_body, (480,480), (462,495), 2.0)
    #pymunk.Segment(space.static_body, (550,50), (545,115), 2.0)

]
for line in static_lines:
    line.elasticity = 0.7
    line.group = 1
space.add(*static_lines)

fp = [(20, -20),(-132, 0),(20, 20)]
mass = 100
moment = pymunk.moment_for_poly(mass, fp)

# right flipper
r_flipper_body = pymunk.Body(mass, moment)
r_flipper_body.position = 450, 500
#r_flipper_shape = pymunk.Poly(r_flipper_body, fp)
r_flipper_shape = pymunk.Segment(r_flipper_body, (0, 0), (-116, 0), 14)
space.add(r_flipper_body, r_flipper_shape)

r_flipper_joint_body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
r_flipper_joint_body.position = r_flipper_body.position
j = pymunk.PinJoint(r_flipper_body, r_flipper_joint_body, (0, 0), (0, 0))

s = pymunk.DampedRotarySpring(r_flipper_body, r_flipper_joint_body, 0.0, 20000000, 900000)
space.add(j, s)

# left flipper
l_flipper_body = pymunk.Body(mass, moment)
l_flipper_body.position = 150, 500
#l_flipper_shape = pymunk.Poly(l_flipper_body, [(-x, y) for x, y in fp])
l_flipper_shape = pymunk.Segment(l_flipper_body, (0, 0), (116, 0), 14)
space.add(l_flipper_body, l_flipper_shape)

l_flipper_joint_body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
l_flipper_joint_body.position = l_flipper_body.position
j = pymunk.PinJoint(l_flipper_body, l_flipper_joint_body, (0, 0), (0, 0))
s = pymunk.DampedRotarySpring(l_flipper_body, l_flipper_joint_body, -0.0, 20000000, 900000)
space.add(j, s)

r_flipper_shape.group = l_flipper_shape.group = 1
r_flipper_shape.elasticity = l_flipper_shape.elasticity = 0.4

# bumpers (round)
plist = [(230, 100), (370, 100),(300,140)]

body1 = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
body1.position = plist[0]
shape21 = pymunk.Circle(body1, 20)
shape21.elasticity = 1.5
shape21.collision_type = 3
shape21.color = (31, 163, 5, 255)
space.add(body1, shape21)

body2 = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
body2.position = plist[1]
shape22 = pymunk.Circle(body2, 20)
shape22.elasticity = 1.5
shape22.collision_type = 4
shape22.color = (31, 163, 5, 255)
space.add(body2, shape22)

body3 = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
body3.position = plist[2]
shape23 = pymunk.Circle(body3, 20)
shape23.elasticity = 1.5
shape23.collision_type = 5
shape23.color = (31, 163, 5, 255)
space.add(body3, shape23)



# bumper (triangle)
vertices = [(10, -20), (90, 120), (0, 90)]
body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
body.position = (100,240)
shape3 = pymunk.Poly(body, vertices)
shape3.elasticity = 1.3
shape3.collision_type = 6
shape3.color = (191, 48, 48, 255)
space.add(body, shape3)

vertices = [(-10, -20), (-90, 120), (0, 90)]
body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
body.position = (500,240)
shape4 = pymunk.Poly(body, vertices)
shape4.elasticity = 1.3
shape4.collision_type = 7
shape4.color = (191, 48, 48, 255)
space.add(body, shape4)

# Add text


# Spawning balls
def addBall():
    global ballbody,shape1
    mass = 1
    radius = 14
    inertia = pymunk.moment_for_circle(mass, 0, radius, (0, 0))
    ballbody = pymunk.Body(mass, inertia)
    ballbody.position = 500,460
    shape1 = pymunk.Circle(ballbody, radius, (0, 0))
    shape1.elasticity = 0.90
    shape1.collision_type = 0
    space.add(ballbody, shape1)
    balls.append(shape1)


# Define collision callback function, will be called when ball touches bumpers
def bounceOnBump1(space, arbiter,dummy):
    global score
    score += 10
    os.system('cls')
    print("SCORE : ",score)
    mixer.music.load(r'C:\Users\Dimuth De Zoysa\Downloads\PyMunk-Physics-Simulation-main\PyMunk-Physics-Simulation-main\bumperSound01.WAV')
    mixer.music.play()
    shape21.color = (0,255,0,255)
    time.sleep(0.06)
    return True
def bounceOnBump2(space, arbiter,dummy):
    global score
    score += 10
    os.system('cls')
    print("SCORE : ",score)
    mixer.music.load(r'C:\Users\Dimuth De Zoysa\Downloads\PyMunk-Physics-Simulation-main\PyMunk-Physics-Simulation-main\bumperSound01.WAV')
    mixer.music.play()
    shape22.color = (0,255,0,255)
    time.sleep(0.06)
    return True
def bounceOnBump3(space, arbiter,dummy):
    global score
    score += 10
    os.system('cls')
    print("SCORE : ",score)
    mixer.music.load(r'C:\Users\Dimuth De Zoysa\Downloads\PyMunk-Physics-Simulation-main\PyMunk-Physics-Simulation-main\bumperSound01.WAV')
    mixer.music.play()
    shape23.color = (0,255,0,255)
    time.sleep(0.06)
    return True
def bounceOnBump4(space, arbiter,dummy):
    global score
    score += 10
    os.system('cls')
    print("SCORE : ",score)
    mixer.music.load(r'C:\Users\Dimuth De Zoysa\Downloads\PyMunk-Physics-Simulation-main\PyMunk-Physics-Simulation-main\bumperSound01.WAV')
    mixer.music.play()
    shape3.color = (255,0,0,255)
    time.sleep(0.06)
    return True
def bounceOnBump5(space, arbiter,dummy):
    global score
    score += 10
    os.system('cls')
    print("SCORE : ",score)
    mixer.music.load(r'C:\Users\Dimuth De Zoysa\Downloads\PyMunk-Physics-Simulation-main\PyMunk-Physics-Simulation-main\bumperSound01.WAV')
    mixer.music.play()
    shape4.color = (255,0,0,255)
    time.sleep(0.06)
    return True
def SepCol1(space,arbiter,dummy):
    shape21.color = (31, 163, 5, 255)
def SepCol2(space,arbiter,dummy):
    shape22.color = (31, 163, 5, 255)
def SepCol3(space,arbiter,dummy):
    shape23.color = (31, 163, 5, 255)
def SepCol4(space,arbiter,dummy):
    shape3.color = (191, 48, 48, 255)
def SepCol5(space,arbiter,dummy):
    shape4.color = (191, 48, 48, 255)

# Setup the collision callback function
h1 = space.add_collision_handler(0, 3)
h1.begin = bounceOnBump1
h1.separate = SepCol1
h2 = space.add_collision_handler(0, 4)
h2.begin = bounceOnBump2
h2.separate = SepCol2
h3 = space.add_collision_handler(0, 5)
h3.begin = bounceOnBump3
h3.separate = SepCol3
h4 = space.add_collision_handler(0, 6)
h4.begin = bounceOnBump4
h4.separate = SepCol4
h5 = space.add_collision_handler(0, 7)
h5.begin = bounceOnBump5
h5.separate = SepCol5
#h.separate = changeColor# Listening for key press events
addBall()
rounds = 3
pygame.font.init()

while running:
    screen.fill(pygame.Color("white")) # Fill screen white
    pygame.draw.rect(screen,(11, 156, 136),(0,550,610,100))
    my_font = pygame.font.SysFont('Comic Sans MS', 30)
    text_surface = my_font.render(('Score : '+str(score)), True, (0, 255, 0))
    screen.blit(text_surface, (20,550))
    text_surface2 = my_font.render(('Balls Remaining : '+str(rounds)), True, (0, 255, 0))
    screen.blit(text_surface2, (325,550))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_p:
            timestamp = str(datetime.datetime.now()).replace(' ','_').replace(':','')
            pygame.image.save(screen, f"flipper{timestamp}.png")

        elif event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
            r_flipper_body.apply_impulse_at_local_point(Vec2d.unit() * -40000, (-100, 0))
            mixer.music.load(r'C:\Users\Dimuth De Zoysa\Downloads\PyMunk-Physics-Simulation-main\PyMunk-Physics-Simulation-main\flipperSound02.mp3')
            mixer.music.play()

        elif event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
            l_flipper_body.apply_impulse_at_local_point(Vec2d.unit() * 40000, (-100, 0))
            mixer.music.load(r'C:\Users\Dimuth De Zoysa\Downloads\PyMunk-Physics-Simulation-main\PyMunk-Physics-Simulation-main\flipperSound02.mp3')
            mixer.music.play()

        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            #print(ballbody.position)
            # Check if balls on the spring
            if ballbody.position.x > 494 and ballbody.position.y < 465:
                ballbody.apply_impulse_at_local_point(Vec2d.unit() * -1150, (0, 0))
                mixer.music.load(r'C:\Users\Dimuth De Zoysa\Downloads\PyMunk-Physics-Simulation-main\PyMunk-Physics-Simulation-main\launchersound01.WAV')
                mixer.music.play()

    ### Draw stuff
    space.debug_draw(draw_options)

    r_flipper_body.position = 450, 500
    l_flipper_body.position = 150, 500
    r_flipper_body.velocity = l_flipper_body.velocity = 0, 0

    ### Remove any balls outside

    to_remove = []
    for ball in balls:
        if ball.body.position.get_distance((300, 300)) > 1000:
            to_remove.append(ball)
            #GameOver after 3 rounds of playing
            rounds -= 1
            if rounds <= 0 :
                print('GAME OVER')
                rounds = 0
                res = pyautogui.confirm(text='Restart Game ?', title='Game Over', buttons=['Yes', 'No'])
                if res == "Yes" :
                    exec(f'import {script_name}') # Re-run the script
            else:
                addBall()
                print('Rounds remaining : ',rounds)

    for ball in to_remove:
        space.remove(ball.body, ball)
        balls.remove(ball)

    ### Update physics
    dt = 1.0 / 60.0 / 5.0
    for x in range(5):
        space.step(dt)

    ### Flip screen
    pygame.display.flip()
    clock.tick(50)
    pygame.display.set_caption("PINBALL GAME  |  FPS: " + str(clock.get_fps())[0:4])
    
