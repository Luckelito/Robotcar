import pygame
import time
import RPi.GPIO as GPIO

def cable_on(curr_cable):
    GPIO.output(curr_cable, True)

def cable_off(curr_cable):
    GPIO.output(curr_cable, False)

def main():
    pygame.init()
    joysticks = []
    clock = pygame.time.Clock()
    keep_playing = True

    GPIO.setmode(GPIO.BOARD)

    LF_cable = 11 # brown: left forward
    LB_cable = 13 # red: left backward
    RF_cable = 16 # yellow: right forward
    RB_cable = 15 # orange: right backward

    GPIO.setup(LF_cable, GPIO.OUT)
    GPIO.setup(LB_cable, GPIO.OUT)
    GPIO.setup(RF_cable, GPIO.OUT)
    GPIO.setup(RB_cable, GPIO.OUT)

    # for al the connected joysticks
    for i in range(0, pygame.joystick.get_count()):
        # create an Joystick object in our list
        joysticks.append(pygame.joystick.Joystick(i))
        # initialize them all (-1 means loop forever)
        joysticks[-1].init()
        # print a statement telling what the name of the controller is
        print ("Detected joystick "),joysticks[-1].get_name(),"'"

    is_running_LF = False
    is_running_RF = False
    is_running_LB = False
    is_running_RB = False
    while keep_playing:    
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == 7: # Axis event
                if event.axis == 5:
                    if int(event.value * 1000) != -1000 and not is_running_LB:
                        is_running_LF = True
                        cable_on(LF_cable)
                    else:
                        is_running_LF = False
                        cable_off(LF_cable)
                if event.axis == 4:
                    if int(event.value * 1000) != -1000 and not is_running_RB:
                        is_running_RF = True
                        cable_on(RF_cable)
                    else:
                        is_running_RF = False
                        cable_off(RF_cable)

            elif event.type == 10: # Button down event
                if event.button == 6 and not is_running_LF:
                    is_running_LB = True
                    cable_on(LB_cable)
                if event.button == 7 and not is_running_RF:
                    is_running_RB = True
                    cable_on(RB_cable)
                if event.button == 1: # Use button b to terminate program
                    keep_playing = False

            elif event.type == 11: # Button up event
                if event.button == 6:
                    is_running_LB = False
                    cable_off(LB_cable)
                if event.button == 7:
                    is_running_RB = False
                    cable_off(RB_cable)
                    
if __name__ == "__main__":
    try:
        main()
    finally:
        print("Cleanup")
        GPIO.cleanup()
