import sys
sys.path.append('./logidrivepy')
from logidrivepy import LogitechController
from logidrivepy import LogitechControllerStructs
import time
from ctypes import *
import paho.mqtt.client as paho
from struct import *

broker="10.0.0.42"
port=1883
def on_publish(client,userdata,result):             #create function for cal$
    print("data published \n")
    pass

def constrain(n, minn, maxn):
    return max(min(maxn, n), minn)

def convertForRaspi(n, minn, maxn, servoMin, servoMax, deadzoneMid):
    mid = servoMin + ((servoMax - servoMin)/2)

    if ((n < deadzoneMid) and (n > -1*deadzoneMid) ):
        return mid
    elif(n > deadzoneMid):
        print("Right Turn")
        value = mid + ((n/maxn) * (servoMax - mid))
        return value
    elif(n < -1*deadzoneMid):
        print("Left Turn")
        value = mid - ((n/minn) * (mid - servoMin))
        return value

def convertThrottle(fwd, reverse, minn, maxn, servoMin, servoMax, deadzoneMid):
    mid = servoMin + ((servoMax - servoMin)/2)
    #32767 -> -32768

    if((fwd == maxn) and (reverse == maxn)):
        return mid
    elif((fwd < maxn) and (reverse == maxn)): 
        #Forward 
        #TODO: Fix for when fwd is a negative number
        #value = mid + ((abs(fwd)/(maxn - minn)) * (servoMax - mid))
        value = 0
        return value
    elif((fwd == maxn) and (reverse < maxn)):
        #Backwards
        value = 0
        return value


def run_test():
    print("Hello World")

    controller = LogitechController()

    steering_initialize = controller.steering_initialize()
    logi_update = controller.logi_update()
    is_connected = controller.is_connected(0)
    controller.play_leds(0, 1000, 1000, 5000)
    button_triggered0 = controller.button_is_pressed(0, 0)
    

    #print(f"\n---Logitech Controller Test---")
    #print(f"steering_initialize: {steering_initialize}")
    #print(f"logi_update: {logi_update}")
    #print(f"button_triggered0: {button_triggered0}")
    

    state = controller.get_state_engines(0)
    #print(state.contents.lX)
    #print(state.contents.lY)
    #print(state.contents.lZ)

    #print("Sleeping")
    time.sleep(1)
    #print("Awake")

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
        steerConstrained = constrain(state.contents.lX, -12000, 12000)
        throtConstrained = constrain(state.contents.lY, -32767, 32767) #Top of pedal: 32767, Bottom of pedal = -32768
        steering = convertForRaspi(steerConstrained, -12000, 12000, 2, 13, 100)
        throttle = convertForRaspi(throtConstrained, -32767, 32767, 2, 13, 50)
        
        brake = 0.0
        print("values: ", state.contents.lX, ", ", state.contents.lY, ", ", brake)        
        print("values: ", steering, ", ", throttle, ", ", brake)
        throttle = 0
        values = pack(">fff", throttle, steering, brake)
        ret= client1.publish("RCControl", values)

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
    print("Hello")
    client1= paho.Client("steeringWheel")                           #create client ob$
    client1.on_publish = on_publish                          #assign function to$
    client1.connect(broker,port)
    run_test()