import pygame
import time
from socket import *
import numpy as np
import ctypes

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (255, 0, 255)
CYAN = (0, 255, 255)

#config tcp connection
HOST = '169.254.243.180' #set ip address
PORT = 80 #set port number ( default 80)
Address = (HOST, PORT)
UDPSocket = socket(AF_INET, SOCK_DGRAM)

speed = 0

class TextPrint:
    def __init__(self):
        self.reset()
        #set screen font
        self.font = pygame.font.Font('/usr/share/fonts/truetype/droid/DroidSans.ttf', 20, bold = True)

    def print_info(self, screen, textString, color, flag):
        textBitmap = self.font.render(textString, True, color)
        if flag == 0:
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

pygame.init() #init pygame module
size = [1366, 768] #screen size ( default for laptop )
screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
pygame.display.set_caption("Network Command Sender") #set software title
done = False #Loop until the user clicks the close button.
clock = pygame.time.Clock() #how fast the screen updates
pygame.joystick.init() #initialize the joysticks
textPrint = TextPrint() #print situation info
# -------- Main Program Loop -----------
while done == False:
    # EVENT PROCESSING STEP
    for event in pygame.event.get(): #user did something
        if event.type == pygame.QUIT: #if user clicked close
            done = True #flag that we are done so we exit this loop
        #possible joystick actions: JOYAXISMOTION JOYBALLMOTION JOYBUTTONDOWN JOYBUTTONUP JOYHATMOTION
        if event.type == pygame.JOYBUTTONDOWN:
            print("Joystick button pressed !")
        if event.type == pygame.JOYBUTTONUP:
            print("Joystick button released !")
        if event.type is pygame.KEYDOWN and event.key == pygame.K_f:
            if screen.get_flags() & pygame.FULLSCREEN:
                pygame.display.set_mode(size)
            else:
                pygame.display.set_mode(size, pygame.FULLSCREEN)
        if event.type is pygame.KEYDOWN and event.key == pygame.K_c:
            pygame.quit()
    screen.fill(BLACK) #clear the screen to black
    textPrint.reset() #reset text printing settings & positions
    lines() #draw table lines
    joystick_count = pygame.joystick.get_count() #get count of available joysticks
    for i in range(joystick_count): #for each joystick
        joystick = pygame.joystick.Joystick(i) #select joystick[i]
        joystick.init() #init selected joystick
        name = joystick.get_name() #get joystick name
        axes = joystick.get_numaxes() #get joystick axes
        buttons = joystick.get_numbuttons() #get joystick buttons
        hats = joystick.get_numhats() #get joystick hats
        textPrint.print_info(screen, "               Robot Controller - UDP Sender - Device : {}    -    Malayer University".format(name), RED, 0)
        textPrint.nextline()
        textPrint.nextline()
        for i in range(axes): #print axe's info
            axis = joystick.get_axis(i)
            textPrint.print_info(screen, "  Axis {} : {:>6.3f}".format(i, axis), CYAN, 0)
        textPrint.nextline()
        for i in range(buttons): #print button's info
            button = joystick.get_button(i)
            textPrint.print_info(screen, "  Button {:>2} : {}".format(i,button), PURPLE, 0)
        textPrint.nextline()
        for i in range(hats): #print hat's info
            hat = joystick.get_hat(i)
            textPrint.print_info(screen, "  Hat {} : {}".format(i, str(hat)), GREEN, 0)
        #convert geted range from axes for sending usable data to receiver
        list = range(-1000, 1000)
        list2 = list[::-1] #reverse list
        target = int(joystick.get_axis(3) * 1000)
        if target in list2:
            target = list2.index(target) #get true value for current axes target by select index number from list
            target /= 2 #devide by 2 for set a final target and also possitive
        startpoint = (1338, 755)
        OldRange = (999 - 0)  
        NewRange = (50 - 755)  
        target = (((target - 0) * NewRange) / OldRange) + 755 #change range from (0,999) to (50,755)
        endpoint = (1338, target)
        pygame.draw.lines(screen, YELLOW, True, [startpoint, endpoint], 28) #draw speed bar
        pygame.display.update() #update screen
        #textPrint.print_info(screen, str(target), WHITE, 1)
        target = int(target)
        '''
        set final speed value before sending, we can define many speeds but i define 8 differente speed by other side ( motor drivers )
        we have differente speed value in the other side ( motor drivers ), so we should define some numbers first and then send final
        value by these numbers
        '''
        if target <= 138:
            speed = 8
        elif target <= 226:
            speed = 7
        elif target <= 314:
            speed = 6
        elif target <= 402:
            speed = 5
        elif target <= 490:
            speed = 4
        elif target <= 578:
            speed = 3
        elif target <= 666:
            speed = 2
        elif target <= 750:
            speed = 1
        screen.blit(pygame.font.Font('/usr/share/fonts/truetype/droid/DroidSans.ttf', 25, bold = True).render(str(speed), True, WHITE), [1332, 14])
        '''
        command's configuration as like as follow :
            --- Robot-Part : Speed
        speed is for wheels only !!! other parts get a zero speed value 
        '''
        arm = False
        if joystick.get_button(0) == 1:
            textPrint.print_info(screen, "Situation : Arm Down", WHITE, 1)
            Message = "ArmUP:0"
            UDPSocket.sendto(Message, Address)
            arm = True
        if joystick.get_button(1) == 1:
            textPrint.print_info(screen, "Situation : Arm UP", WHITE, 1)
            Message = "ArmDown:0"
            UDPSocket.sendto(Message, Address)
            arm = True
        if joystick.get_button(2) == 1:
            textPrint.print_info(screen, "Situation : Elbow Up", WHITE, 1)
            Message = "ArmLeft:0"
            UDPSocket.sendto(Message, Address)
        if joystick.get_button(3) == 1:
            textPrint.print_info(screen, "Situation : Elbow Down", WHITE, 1)			
            Message = "ArmRight:0"
            UDPSocket.sendto(Message, Address)
        if joystick.get_button(4) == 1:
            textPrint.print_info(screen, "Situation : Cutter Open", WHITE, 1)
            Message = "ArenjDown:0"
            UDPSocket.sendto(Message, Address)
        if joystick.get_button(5) == 1:
            textPrint.print_info(screen, "Situation : Cutter Close", WHITE, 1)
            Message = "ArenjUP:0"
            UDPSocket.sendto(Message, Address)
        if joystick.get_button(6) == 1:
            textPrint.print_info(screen, "Situation : Work 1", WHITE, 1)
            Message = "GripperOpen:0"
            UDPSocket.sendto(Message, Address)			
        if joystick.get_button(7) == 1:
            textPrint.print_info(screen, "Situation : Work 2", WHITE, 1)
            Message = "GripperClose:0"
            UDPSocket.sendto(Message, Address)
        if joystick.get_button(8) == 1:
            textPrint.print_info(screen, "Situation : Alert Off", WHITE, 1)			
            Message = "LEDOn:0"
            UDPSocket.sendto(Message, Address)
        if joystick.get_button(9) == 1:
            textPrint.print_info(screen, "Situation : Alert On", WHITE, 1)			
            Message = "LEDOff:0"
            UDPSocket.sendto(Message, Address)
        if joystick.get_button(10) == 1:
            textPrint.print_info(screen, "Situation : Stop", WHITE, 1)			
            Message = "RelayOn:0"
            UDPSocket.sendto(Message, Address)
        if joystick.get_button(11) == 1:
            textPrint.print_info(screen, "Situation : Start", WHITE, 1)
            Message = "RelayOff:0"
            UDPSocket.sendto(Message, Address)
        if joystick.get_axis(1) * 1000 < -700:
            if speed==1: f=25
            if speed==2: f=24
            if speed==3: f=23
            if speed==4: f=22
            if speed==5: f=21
            if speed==6: f=20
            if speed==7: f=19
            if speed==8: f=18
            Message = "Forward:" + str(f)
            UDPSocket.sendto(Message, Address)
        elif joystick.get_axis(1) * 1000 > 700:
            if speed==1: b=31
            if speed==2: b=32
            if speed==3: b=33
            if speed==4: b=34
            if speed==5: b=35
            if speed==6: b=36
            if speed==7: b=37
            if speed==8: b=38
            Message = "Backward:" + str(b)
            UDPSocket.sendto(Message, Address)
        elif joystick.get_axis(0) * 1000 < -700:
            if speed==1: f=25
            if speed==2: f=24
            if speed==3: f=23
            if speed==4: f=22
            if speed==5: f=21
            if speed==6: f=20
            if speed==7: f=19
            if speed==8: f=18
            Message = "Left:" + str(f)
            UDPSocket.sendto(Message, Address)
        elif joystick.get_axis(0) * 1000 > 700:
            if speed==1: b=31
            if speed==2: b=32
            if speed==3: b=33
            if speed==4: b=34       
            if speed==5: b=35
            if speed==6: b=36
            if speed==7: b=37
            if speed==8: b=38
            Message = "Right:" + str(b)
            UDPSocket.sendto(Message, Address)
        elif joystick.get_axis(1) * 1000 < 300 and joystick.get_axis(1) * 1000 > -300:
            Message = "Stop:0"
            UDPSocket.sendto(Message, Address)
        time.sleep(0.1)
    pygame.display.flip()
    # Limit to 20 frames per second
    clock.tick(15)
UDPSocket.close()
pygame.quit ()