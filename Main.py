import pygame
import math
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

    GPIO.setup(LF_cable, GPIO.OUT)
    GPIO.setup(LB_cable, GPIO.OUT)
    GPIO.setup(RF_cable, GPIO.OUT)
    GPIO.setup(RB_cable, GPIO.OUT)
    GPIO.setup(rev_gun_cable, GPIO.OUT)
    GPIO.setup(shoot_cable, GPIO.OUT)
    LF_pwm = GPIO.PWM(LF_cable, 100)
    LB_pwm = GPIO.PWM(LF_cable, 100)
    RF_pwm = GPIO.PWM(RF_cable, 100)
    RB_pwm = GPIO.PWM(RF_cable, 100)

    # for al the connected joysticks
    for i in range(0, pygame.joystick.get_count()):
        # create an Joystick object in our list
        joysticks.append(pygame.joystick.Joystick(i))
        # initialize them all (-1 means loop forever)
        joysticks[-1].init()
        # print a statement telling what the name of the controller is
        print ("Detected joystick "),joysticks[-1].get_name(),"'"

    LF_pwm.start(100)
    LB_pwm.start(100)
    RF_pwm.start(100)
    RB_pwm.start(100)

    joystick_x_value = 0
    joystick_y_value = 0
    while keep_playing:    
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.JOYAXISMOTION: 
                if event.axis == 0: # Joystick x-axis
                    joystick_x_value = round(event.value, 2) * 100
                if event.axis == 1: # Joystick y-axis
                    joystick_y_value = round(event.value, 2) * 100
                if event.axis == 0 or event.axis == 1:
                    if joystick_x_value >= 0 and joystick_y_value < 0: # first quadrant
                        #print("Left", 0)
                        LF_pwm.ChangeDutyCycle(0)
                        LB_pwm.ChangeDutyCycle(100)
                        right_speed = 100 - (joystick_x_value / math.sqrt(50)) ** 2
                        if right_speed > 0:
                            #print("Right", 100 - right_speed)
                            RF_pwm.ChangeDutyCycle(100 - right_speed)
                            RB_pwm.ChangeDutyCycle(100)
                        else:
                            #print("Right", -(100 + right_speed))
                            RF_pwm.ChangeDutyCycle(100 + right_speed)
                            RB_pwm.ChangeDutyCycle(100)

                    elif joystick_x_value >= 0 and joystick_y_value >= 0: # second quadrant
                        #print("Right", "-0")
                        RB_pwm.ChangeDutyCycle(0)
                        RF_pwm.ChangeDutyCycle(100)
                        left_speed = -(100 - (joystick_x_value / math.sqrt(50)) ** 2)
                        if left_speed > 0:
                            #print("Left", 100 - left_speed)
                            LF_pwm.ChangeDutyCycle(100 - left_speed)
                            LB_pwm.ChangeDutyCycle(100)
                        else:
                            #print("Left", -(100 + left_speed))
                            LF_pwm.ChangeDutyCycle(100 + left_speed)
                            LB_pwm.ChangeDutyCycle(100)

                    elif joystick_x_value < 0 and joystick_y_value >= 0: # third quadrant
                        #print("Left", "-0")
                        LB_pwm.ChangeDutyCycle(0)
                        LF_pwm.ChangeDutyCycle(100)
                        right_speed = -(100 - (joystick_x_value / math.sqrt(50)) ** 2)
                        if right_speed > 0:
                            #print("Right", 100 - right_speed)
                            RF_pwm.ChangeDutyCycle(100 - left_speed)
                            RB_pwm.ChangeDutyCycle(100)
                        else:
                            #print("Right", -(100 + right_speed))
                            RF_pwm.ChangeDutyCycle(100 + left_speed)
                            RB_pwm.ChangeDutyCycle(100)

                    elif joystick_x_value < 0 and joystick_y_value < 0: # forth quadrant
                        #print("Right", 0)
                        RF_pwm.ChangeDutyCycle(0)
                        RB_pwm.ChangeDutyCycle(100)
                        left_speed = 100 - (joystick_x_value / math.sqrt(50)) ** 2
                        if left_speed > 0:
                            #print("Left", 100 - left_speed)
                            LF_pwm.ChangeDutyCycle(100 - left_speed)
                            LB_pwm.ChangeDutyCycle(100)
                        else:
                            #print("Left", -(100 + left_speed))
                            LF_pwm.ChangeDutyCycle(100 + left_speed)
                            LB_pwm.ChangeDutyCycle(100)

            elif event.type == pygame.JOYBUTTONDOWN:
                if event.button == 11: # Use menu button to terminate program
                    keep_playing = False
                if event.button == 0: # A button
                    print("A")
  #                  cable_on(rev_gun_cable)
                if event.button == 1: # B button
                    print("B")
   #                 cable_on(shoot_cable)

            elif event.type == pygame.JOYBUTTONUP: 
                if event.button == 0: # A button
                    pass
    #                cable_off(rev_gun_cable)
                if event.button == 1: # B button
                    pass
     #               cable_off(shoot_cable)
                    
if __name__ == "__main__":
    try:
        main()
    finally:
        print("Cleanup")
        #GPIO.cleanup()
