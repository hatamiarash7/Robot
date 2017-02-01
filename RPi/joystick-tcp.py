import pygame
import time
from socket import *
import numpy as np
import ctypes
import RPi.GPIO as GPIO

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (255, 0, 255)
CYAN = (0, 255, 255)

HOST = '192.168.1.8'
PORT = 80
Address = (HOST, PORT)
UDPSocket = socket(AF_INET, SOCK_DGRAM)

GPIO.setmode(GPIO.BCM)
GPIO.setup(4, GPIO.OUT)
pwm = GPIO.PWM(4, 100) #ch12 freq50Hz
pwm.start(0)
low = 0
high = 0
stop = True

class TextPrint:
    def __init__(self):
        self.reset()
        self.font = pygame.font.Font('/usr/share/fonts/truetype/droid/DroidSans.ttf', 20, bold=True)

    def print_info(self, screen, textString, color, flag):
        textBitmap = self.font.render(textString, True, color)
        if flag==0:
            screen.blit(textBitmap, [self.x, self.y])
            self.y += self.line_height + 5
        else:
            screen.blit(textBitmap, [400, 200])
            self.y += self.line_height + 5
			
    def reset(self):
        self.x = 10
        self.y = 10
        self.line_height = 15
		
    def nextline(self):
        self.y +=self.line_height + 5

def lines():
    #Borders
    pygame.draw.lines(screen, WHITE, True, [(0, 0), (1364, 0)], 10)
    pygame.draw.lines(screen, WHITE, True, [(1364, 0), (1364, 768)], 10)
    pygame.draw.lines(screen, WHITE, True, [(1364, 766), (0, 766)], 10)
    pygame.draw.lines(screen, WHITE, True, [(0, 763), (0, 0)], 10)
    	
    #Columns
    pygame.draw.lines(screen, WHITE, True, [(1316, 0), (1316, 768)], 1)

pygame.init()
size = [1366, 768]

screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
pygame.display.set_caption("UDP Sender")
#Loop until the user clicks the close button.
done = False
#how fast the screen updates
clock = pygame.time.Clock()
# Initialize the joysticks
pygame.joystick.init()
textPrint = TextPrint()
# -------- Main Program Loop -----------
while done==False:
    # EVENT PROCESSING STEP
    for event in pygame.event.get(): # User did something
        if event.type == pygame.QUIT: # If user clicked close
            done=True # Flag that we are done so we exit this loop
        # Possible joystick actions: JOYAXISMOTION JOYBALLMOTION JOYBUTTONDOWN JOYBUTTONUP JOYHATMOTION
        if event.type == pygame.JOYBUTTONDOWN:
            print("Joystick button pressed.")
        if event.type == pygame.JOYBUTTONUP:
            print("Joystick button released.")
        if event.type is pygame.KEYDOWN and event.key == pygame.K_f:
            if screen.get_flags() & pygame.FULLSCREEN:
                pygame.display.set_mode(size)
            else:
                pygame.display.set_mode(size, pygame.FULLSCREEN)
        if event.type is pygame.KEYDOWN and event.key == pygame.K_c:
            pygame.quit()
    # clear the screen to white
    screen.fill(BLACK)
    textPrint.reset()
    lines()
    # For each joystick:
    joystick_count = pygame.joystick.get_count()
    for i in range(joystick_count):
        joystick = pygame.joystick.Joystick(i)
        joystick.init() 		
		# get joystick key information
        name = joystick.get_name()
        axes = joystick.get_numaxes()
        buttons = joystick.get_numbuttons()
        hats = joystick.get_numhats()
        textPrint.print_info(screen, "               Robot Controller - UDP Sender - Device : {}    -    Malayer University".format(name), RED, 0)
        textPrint.nextline()
        textPrint.nextline()
        for i in range(axes):
            axis = joystick.get_axis(i)
            textPrint.print_info(screen, "  Axis {} : {:>6.3f}".format(i, axis), CYAN, 0)
        textPrint.nextline()
        for i in range(buttons):
            button = joystick.get_button(i)
            textPrint.print_info(screen, "  Button {:>2} : {}".format(i,button), PURPLE, 0)
        textPrint.nextline()
        for i in range(hats):
            hat = joystick.get_hat(i)
            textPrint.print_info(screen, "  Hat {} : {}".format(i, str(hat)), GREEN, 0)
        list = range(-1000, 1000)
        list2 = list[::-1]
        target = int(joystick.get_axis(3) * 1000)
        if target in list2:
            target = list2.index(target)
            target /= 2
        startpoint = (1338, 755)
        OldRange = (999 - 0)  
        NewRange = (50 - 755)  
        target = (((target - 0) * NewRange) / OldRange) + 755
        endpoint = (1338, target)
        screen.blit(pygame.font.Font('/usr/share/fonts/truetype/droid/DroidSans.ttf', 24, bold=True).render("3", True, WHITE), [1332,14])
        pygame.draw.lines(screen, YELLOW, True, [startpoint, endpoint], 28)
        pygame.display.update()
        textPrint.print_info(screen, str(int(joystick.get_axis(1) * 1000)) + "                                                                                  " + str(target) + " " + str(low) + " " + str(low), WHITE, 1)
        if int(target) < 191 and int(target) >= 50:
            low = 9
            high = 19
        elif int(target) < 332 and int(target) >= 191:
            low = 10
            high = 18
        elif int(target) < 473 and int(target) >= 332:
            low = 11
            high = 17
        elif int(target) < 614 and int(target) >= 473:
            low = 12
            high = 16
        elif int(target) <= 755 and int(target) >= 614:
            low = 13
            high = 15
        else:
            low = 100
        # Gripper
        if joystick.get_button(0)==1:
            textPrint.print_info(screen, "Situation : Gripper Close", WHITE, 1)
            Message = "Key1"
            UDPSocket.sendto(Message, Address)
        if joystick.get_button(1)==1:
            textPrint.print_info(screen, "Situation : Gripper Open", WHITE, 1)
            Message = "Key2"
            UDPSocket.sendto(Message, Address)
            
        #Elbow
        if joystick.get_button(2)==1:
            textPrint.print_info(screen, "Situation : Elbow Up", WHITE, 1)
            Message = "Key3"
            UDPSocket.sendto(Message, Address)
        if joystick.get_button(3)==1:
            textPrint.print_info(screen, "Situation : Elbow Down", WHITE, 1)			
            Message = "Key4"
            UDPSocket.sendto(Message, Address)
			
        #Cutter
        if joystick.get_button(4)==1:
            textPrint.print_info(screen, "Situation : Cutter Open", WHITE, 1)
            Message = "Key5"
            UDPSocket.sendto(Message, Address)
        if joystick.get_button(5)==1:
            textPrint.print_info(screen, "Situation : Cutter Close", WHITE, 1)
            Message = "Key6"
            UDPSocket.sendto(Message, Address)
			
        if joystick.get_button(6)==1:
            textPrint.print_info(screen, "Situation : Work 1", WHITE, 1)
            Message = "Key7"
            UDPSocket.sendto(Message, Address)
			
        if joystick.get_button(7)==1:
            textPrint.print_info(screen, "Situation : Work 2", WHITE, 1)
            Message = "Key8"
            UDPSocket.sendto(Message, Address)
			
        #Alert
        if joystick.get_button(8)==1:
            textPrint.print_info(screen, "Situation : Alert Off", WHITE, 1)			
            Message = "Key9"
            UDPSocket.sendto(Message, Address)
        if joystick.get_button(9)==1:
            textPrint.print_info(screen, "Situation : Alert On", WHITE, 1)			
            Message = "Key10"
            UDPSocket.sendto(Message, Address)
			
        if joystick.get_button(10)==1:
            textPrint.print_info(screen, "Situation : Stop", WHITE, 1)			
            Message = "Key11"
            UDPSocket.sendto(Message, Address)
            GPIO.output(4, 0)
			
        if joystick.get_button(11)==1:
            textPrint.print_info(screen, "Situation : Start", WHITE, 1)
            Message = "Key12"
            UDPSocket.sendto(Message, Address)
            
        
        
        
        if joystick.get_axis(1) * 1000 < -700:
            pwm.ChangeDutyCycle(high)
            time.sleep(0.1)
            stop = True
        if joystick.get_axis(1) * 1000 > 700:
            pwm.ChangeDutyCycle(low)
            time.sleep(0.1)
            stop = True
        if joystick.get_axis(1) * 1000 < 600 and joystick.get_axis(1) * 1000 > -600 and stop:
            pwm.ChangeDutyCycle(14)
            time.sleep(0.1)
            pwm.ChangeDutyCycle(0)
            stop = False
            
    pygame.display.flip()
    # Limit to 20 frames per second
    clock.tick(20)
UDPSocket.close()
pygame.quit ()
