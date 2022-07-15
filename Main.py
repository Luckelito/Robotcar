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

    LF_cable = 12 # brown: left forward
    LB_cable = 32 # red: left backward
    RF_cable = 35 # yellow: right forward
    RB_cable = 33 # orange: right backward
    rev_gun_cable = 38
    shoot_cable = 40

    LF_pwm = GPIO.PWM(LF_cable, 1_000)
    RF_pwm = GPIO.PWM(RF_cable, 1_000)
    GPIO.setup(LB_cable, GPIO.OUT)
    GPIO.setup(RB_cable, GPIO.OUT)
    GPIO.setup(rev_gun_cable, GPIO.OUT)
    GPIO.setup(shoot_cable, GPIO.OUT)

    # for al the connected joysticks
    for i in range(0, pygame.joystick.get_count()):
        # create an Joystick object in our list
        joysticks.append(pygame.joystick.Joystick(i))
        # initialize them all (-1 means loop forever)
        joysticks[-1].init()
        # print a statement telling what the name of the controller is
        print ("Detected joystick "),joysticks[-1].get_name(),"'"

    LF_pwm.start(0)
    RF_pwm.start(0)
    #is_running_LF = False
    #is_running_RF = False
    #is_running_LB = False
    #is_running_RB = False
    while keep_playing:    
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == 7: # Axis event
                if event.axis == 5:
                    LF_pwm.ChangeDutyCycle(event.value * 50 + 50)
                if event.axis == 4:
                    RF_pwm.ChangeDutyCycle(event.value * 50 + 50)

            elif event.type == 10: # Button down event
                #if event.button == 6 and not is_running_LF:
                #    is_running_LB = True
                #    cable_on(LB_cable)
                #if event.button == 7 and not is_running_RF:
                #    is_running_RB = True
                #    cable_on(RB_cable)
                if event.button == 11: # Use menu button to terminate program
                    keep_playing = False
                if event.button == 0: # A button
                    cable_on(rev_gun_cable)
                if event.button == 1: # B button
                    cable_on(shoot_cable)

            elif event.type == 11: # Button up event
                #if event.button == 6:
                #    is_running_LB = False
                #    cable_off(LB_cable)
                #if event.button == 7:
                #    is_running_RB = False
                #    cable_off(RB_cable)
                if event.button == 0: # A button
                    cable_off(rev_gun_cable)
                if event.button == 1: # B button
                    cable_off(shoot_cable)
                    
if __name__ == "__main__":
    try:
        main()
    finally:
        print("Cleanup")
        GPIO.cleanup()
