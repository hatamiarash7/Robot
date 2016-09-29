import pygame
import serial
import time

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (255, 0, 255)
CYAN = (0, 255, 255)

sp = serial.Serial(
	port='/dev/ttyUSB0',
	baudrate=9600,
	bytesize=serial.EIGHTBITS,
	parity=serial.PARITY_NONE,
	stopbits=serial.STOPBITS_ONE,
	xonxoff=serial.XOFF,
	rtscts=False,
	dsrdtr=False
	)
sp.close()
sp.open()

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
    	
pygame.init()
size = [1000, 600]
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Joystick Information")
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
    # clear the screen to white
    screen.fill(BLACK)
    textPrint.reset()
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
        textPrint.print_info(screen, "Joystick Information Controller", RED, 0)
        textPrint.nextline()
        textPrint.print_info(screen, "Controller : {}".format(name), YELLOW, 0)
        textPrint.nextline()
        for i in range(axes):
            axis = joystick.get_axis(i)
            textPrint.print_info(screen, "Axis {} : {:>6.3f}".format(i, axis), CYAN, 0)
        textPrint.nextline()
        for i in range(buttons):
            button = joystick.get_button(i)
            textPrint.print_info(screen, "Button {:>2} : {}".format(i,button), PURPLE, 0)
        textPrint.nextline()
        for i in range(hats):
            hat = joystick.get_hat(i)
            textPrint.print_info(screen, "Hat {} : {}".format(i, str(hat)), GREEN, 0)

        # Gripper
        if joystick.get_button(0)==1:
            textPrint.print_info(screen, "Situation : Gripper Close", WHITE, 1)
            sp.write("key1\n")
        if joystick.get_button(1)==1:
            textPrint.print_info(screen, "Situation : Gripper Open", WHITE, 1)
            sp.write("key2\n")
            
        #Elbow
        if joystick.get_button(2)==1:
            textPrint.print_info(screen, "Situation : Elbow Up", WHITE, 1)
            sp.write("key3\n")
        if joystick.get_button(3)==1:
            textPrint.print_info(screen, "Situation : Elbow Down", WHITE, 1)			
            sp.write("key4\n")
			
        #Cutter
        if joystick.get_button(4)==1:
            textPrint.print_info(screen, "Situation : Cutter Open", WHITE, 1)
            sp.write("key5\n")
        if joystick.get_button(5)==1:
            textPrint.print_info(screen, "Situation : Cutter Close", WHITE, 1)
            sp.write("key6\n")
			
        if joystick.get_button(6)==1:
            textPrint.print_info(screen, "Situation : Work 1", WHITE, 1)
            sp.write("key7\n")
			
        if joystick.get_button(7)==1:
            textPrint.print_info(screen, "Situation : Work 2", WHITE, 1)
            sp.write("key8\n")
			
        #Alert
        if joystick.get_button(8)==1:
            textPrint.print_info(screen, "Situation : Alert Off", WHITE, 1)			
            sp.write("key9\n")
        if joystick.get_button(9)==1:
            textPrint.print_info(screen, "Situation : Alert On", WHITE, 1)			
            sp.write("key10\n")
			
        if joystick.get_button(10)==1:
            textPrint.print_info(screen, "Situation : Stop", WHITE, 1)			
            sp.write("key11\n")
			
        if joystick.get_button(11)==1:
            textPrint.print_info(screen, "Situation : Start", WHITE, 1)
            sp.write("key12\n")
    pygame.display.flip()
    # Limit to 20 frames per second
    clock.tick(20)
pygame.quit ()
