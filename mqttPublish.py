import paho.mqtt.client as paho
from struct import *

broker="10.0.0.42"
port=1883
def on_publish(client,userdata,result):             #create function for cal$
        print("data published \n")
        pass

if __name__ == "__main__":
    print("Hello")
    client1= paho.Client("computer")                           #create client ob$
    client1.on_publish = on_publish                          #assign function to$
    client1.connect(broker,port)

    throttle = -320555
    steering = 755
    brake = 0
    values = pack(">iii", throttle, steering, brake)
    
    print(values)
    ret= client1.publish("testTopic", values)                   #publish

    #ret= client1.publish("testTopic","Hello")                   #publish
