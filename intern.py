import time
import sys
import ibmiotf.application
import ibmiotf.device
import random
#Provide
organization = "xpp2bo"
deviceType = "raspberrypi"
deviceId = "212129"
authMethod = "token"
authToken = "12345678"

#Initialise GPIO

 

try:
    deviceOptions = {"org": organization, "type": deviceType, "id": deviceId, "auth-method": authMethod, "auth-token": authToken}
    deviceCli = ibmiotf.device.Client(deviceOptions)
    #............................................
    
except Exception as e:
    print("Caught exception connecting device: %s" % str(e))
    sys.exit()

deviceCli.connect()

def myCommandCallback(cmd):
    print("Command received: %s" % cmd.data)
    print(type(cmd.data))
    
    if cmd.data=="meteroff":
        print("meter is off")
        volt=0
        current=0
        data = { 'Voltage' : volt, 'Current' : current }
        #print(data)
        def myOnPublishCallback():
            print ("Published Voltage = %s V" %volt, "Current = %s A" % current, "to IBM Watson")
        

        success = deviceCli.publishEvent("DHT11", "json", data, qos=0, on_publish=myOnPublishCallback)
        if not success:
            print("Not connected to IoTF")
    exit()
    deviceCli.disconnect()
    

while True:

    #volt=random.randint(120, 230)
    volt=120
    #print(hum)
    #current=random.randint(30, 80)
    current=30
    power=int(volt/current)
    power_t=4
    cross_thresh='N'
    if (power>power_t):
            cross_thresh='Y'
    #Send voltage and current to IBM Watson
    data = { 'Voltage' : volt, 'Current' : current, 'Crossed_threshold' : cross_thresh }
    #print(data)
    def myOnPublishCallback():
        print ("Published Voltage = %s V" %volt, "Current = %s A" % current, "to IBM Watson")
        

    success = deviceCli.publishEvent("DHT11", "json", data, qos=0, on_publish=myOnPublishCallback)
    if not success:
        print("Not connected to IoTF")
    time.sleep(2)
    
        
        

    deviceCli.commandCallback = myCommandCallback
    
    
        

#Disconnect the device and applicatiom from the cloud
deviceCli.disconnect()
    
