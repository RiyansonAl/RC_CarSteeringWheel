import sys
sys.path.append('./logidrivepy')
from logidrivepy import LogitechController
from logidrivepy import LogitechControllerStructs
import time
from ctypes import *


def run_test():
    print("Hello World")

    controller = LogitechController()

    steering_initialize = controller.steering_initialize()
    logi_update = controller.logi_update()
    is_connected = controller.is_connected(0)
    controller.play_leds(0, 1000, 1000, 5000)
    button_triggered0 = controller.button_is_pressed(0, 0)
    

    print(f"\n---Logitech Controller Test---")
    print(f"steering_initialize: {steering_initialize}")
    print(f"logi_update: {logi_update}")
    print(f"button_triggered0: {button_triggered0}")
    

    state = controller.get_state_engines(0)
    print(state.contents.lX)
    print(state.contents.lY)
    print(state.contents.lZ)



    print("Sleeping")
    time.sleep(1)
    print("Awake")

    while(button_triggered0 == False):

        logi_update = controller.logi_update()
        button_triggered0 = controller.button_is_pressed(0, 0)
        button_triggered1 = controller.button_triggered(0, 1)
        
        #print(f"logi_update: {logi_update}")
        #print(f"button_triggered0: {button_triggered1}")
        

        state = controller.get_state_engines(0)
        buttons = state.contents.rgbButtons
        rglSlider = state.contents.rglSlider
        #print(dir(state.contents))
        #print(state.contents.lX)       #Steering
        #print(state.contents.lY)       #Acclerator
        #print(rglSlider[0])            #Clutch
        #print(state.contents.lZ)
        #print(buttons[0])              #Button 0
        #print(buttons[1])              #Button 1
        #print(buttons[2])              #Button 2


        time.sleep(0.1)


    print(f"is_connected: {is_connected}")

    if steering_initialize and logi_update and is_connected:
        print(f"All tests passed.\n")
    else:
        print(f"Did not pass all tests.\n")

    controller.steering_shutdown()


def spin_controller(controller):
    for i in range(-100, 102, 2):
        controller.LogiPlaySpringForce(0, i, 100, 40)
        controller.logi_update()
        time.sleep(0.1)


def spin_test():
    controller = LogitechController()

    controller.steering_initialize()
    print("\n---Logitech Spin Test---")
    spin_controller(controller)
    print("Spin test passed.\n")

    controller.steering_shutdown()







if __name__ == "__main__":
    run_test()