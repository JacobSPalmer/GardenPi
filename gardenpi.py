import time
import serial
from ToolClasses import EmailUpdates as Email
from ToolClasses import Hardware
from ToolClasses import KeepTime as KT

#Settings:
seconds_to_water = 3
moisture_timer = 3
water_thresh = 20

#Initalize Variables (Don't Edit)
relay = Hardware.Relay(17, False)
timer_int = 1
moisture = 100
times_watered = 0

def water_plant(relay, seconds):
    relay.on()
    print("-----------Watering Plant-----------")
    print("Plant is receiving water! \n")
    time.sleep(seconds)
    print("Plant is done receiving water! \n")
    relay.off()
    print("GardenPi will rest for 5 minutes")
    print("------------------------------------ \n")
    time.sleep(300)

if __name__=='__main__':
    relay.off()
    
    print("-_-_-_-_-_-_GardenPi V1.0-_-_-_-_-_- \n")
    print("--------------Settings--------------")
    print("Running with the following settings:")
    print("Seconds to Water: {}".format(seconds_to_water))
    print("Moisture Threshold: {}%".format(water_thresh))
    print("Time Between Moisture Reading: {} Seconds".format(moisture_timer))
    print("------------------------------------ \n")
    
    ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
    ser.flush()
    
    timer_int = moisture_timer
    
    print("GardenPi will now take care of your plant! \n")
          
    
    while True:
        if ser.in_waiting > 0:
            moisture = int(ser.readline().decode('utf-8').rstrip())
            timeKeeper = KT.TimeKeeper(KT.TimeKeeper.get_current_time())
#             if(timer_int >= moisture_timer):
            print("{} : Moisture level at ".format(KT.TimeKeeper.get_current_time()) + str(moisture) + "% \n")
#                 timer_int = 1
#             else:
#                 timer_int = timer_int + 1
        
            if(moisture < water_thresh):
                timeKeeper.set_time_last_watered(KT.TimeKeeper.get_current_time())
                print("{} : Plant watering beginning!".format(timeKeeper.time_last_watered) + "\n")
                Email.send_water_email(timeKeeper.time_last_watered)
            
                water_plant(relay, seconds_to_water)
                times_watered = times_watered + 1
                
                if(times_watered > 6):
                    times_watered = 0
                    Email.send_checkwater_email()
                
                while(ser.in_waiting > 1):
                    buffer = ser.readline()
                    
                time.sleep(5)
                print("GardenPi is awake! \n")
        
