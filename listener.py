import asyncio, logging, time
import datetime as dt
from datetime import timezone
from pytz import UTC
from zeep import xsd
from onvif import ONVIFCamera
#import cv2
#from pytapo import Tapo
#from pushbullet import Pushbullet


#pb = Pushbullet('your token here')
user = "camUsername"
password = "camPassword"
host = "cam.IPa.ddr.ess"

#camera just needs to be set once, no prob
#tapo = Tapo(host, user, password)

#enable this if you want to see the XML output from the service
#really REALLY helpful to debug.
#logging.getLogger("zeep").setLevel(logging.DEBUG)

#common pullpoint handlers, useful for debug
#http://192.168.100.35:1025/event-1025_1025
#http://192.168.100.35:1024/event-1024_1024


#to save frames with the event, you can delete it
def saveFrame(frame):
    fileDate = dt.datetime.now()
    fileDate = fileDate.strftime("%d-%m_%H-%M-%S")
    fileName = f'cap_{fileDate}.jpg'
    cv2.imwrite(fileName, frame)
    with open(fileName, "rb") as pic:
        file_data = pb.upload_file(pic, "picture.jpg")
    push = pb.push_file(**file_data)
    print("Capture sent: "+ str(fileName))
    

async def run():
    
    #bools for the loops, so I don't get mixed, may change it 
    mainCond = True
    seCond = True

    #starts main loop
    while mainCond:
        
        #check if motion is off to kill it
        #if tapo.getMotionDetection()['enabled'] == "off":
        #    print("bye bye")
        #    return
        
        try: 
            mycam = ONVIFCamera(host,2020,user,password)
        except:
            print("ONVIF cannot connect")
        #sets connection
        await mycam.update_xaddrs()
        

        #check if events work with camera
        if not await mycam.create_pullpoint_subscription():
            print("PullPoint not supported")
            return

        #welcome msg
        print("Loop begins")
               
        
        #creates all the paperwork for the event handler
        pullpoint = mycam.create_pullpoint_service()
        await pullpoint.SetSynchronizationPoint()
        req = pullpoint.create_type("PullMessages")
        
        #this data comes from the ONVIF specification
        req.MessageLimit = 100
        req.Timeout = dt.timedelta(seconds=60)
    
        #Subs to the pullpoint event
        #the sub is what makes the connection doesn't end
        subscription = mycam.create_subscription_service("PullPointSubscription")
        
        #here comes the magic
        while seCond:
            
            #we kill everything if motion in the cam is turned off
            #if tapo.getMotionDetection()['enabled'] == "off":
            #    print("bye bye")
            #    await subscription.Unsubscribe()
            #    await mycam.close()
            #    return
            
            #check for messages
            print("cam ok pull of messages begins")
            messages = await pullpoint.PullMessages(req)
            
            #checks the list received, unfortunately, cannot
            #read that list to look for motion event,
            #may work directly using plain zeep and filter
            if messages.NotificationMessage:
                messages.NotificationMessage.clear()
                print("Event triggered")
    
                #I tried not closing connection, just recycling the
                #subscription, but it sends a TON of events and I couldn't
                #read them, this needs more work.
                await subscription.Unsubscribe()
                await mycam.close()
                
                                
                #set your actions here
                #maybe a CV2 to snap a frame
                #and send it over pushbullet
                #or email, you choose ;)
                
                #five pics, they take like 4 seconds each,
                #may work on resizing it to take less time
                #for i in range(1,6):
                    #rstp
                #    try:
                #        cap = cv2.VideoCapture(f'rtsp://{user}:{password}@{host}:554/stream1')
                #        ret, frame = cap.read()
                #        saveFrame(frame)
                #        cap.release()

                #     except:
                #         print("rtsp cannot connect")
                #         pass
                    
                    
                #get out of the loop                
                break
            
            else:
                print("nothing new in 60s")
                #renew sub. this will never end, it sets
                #next day always
                await subscription.Renew(setTime())
                             
       
        print("resetting")
        
        #to allow reconnect of the camera, 3 seconds are the min
        #if later we can read motion event without closing connection
        #this will be over and it'll be real time :) 
        time.sleep(3)
        

#just to get the time for expiring subscription, may work on something like hass does
#substracting seconds to renew daily so it doesn't bother the service that much,
#but for now it works 
def setTime():
    timenew = ((dt.datetime.utcnow() + dt.timedelta(days=1))
    .isoformat(timespec="seconds").replace("+00:00", "Z"))
    return timenew

#starts the loop, it will never end, the whiles wouldn't let it,
#... I supose.
#def main(): #in case you want to load it in another way
if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())
