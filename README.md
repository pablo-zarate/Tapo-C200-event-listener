# Tapo-C200-motion-listener
ONVIF listener for Tapo C200 (and probably more cameras)


Ok, here is the deal, I am not native english speaker, so I'll try my best:

I made this script to listen for events on the TP-Link Tapo C200. This is not because I hate [HASS](https://www.home-assistant.io/) (which is awesome!) but to know how to do it. Also the example from [onvif-zeep-async](https://github.com/hunterjm/python-onvif-zeep-async) made it possible, this is just a fork of their work. Also many thanks to [pytapo](https://github.com/JurajNyiri/pytapo), the lib that made me not return the camera because of the lack of cloud support haha. 

#Requieremets
This is a listener, you need to have something turned on and in the same network. Also, better to fix the ip of the cam in your router.

I tested this with a Raspberry Pi 4B 2gb model, latest os. I assume you already know how to setup your camera for pytapo but if it is not the case, check [TP-Link's guide](https://www.tp-link.com/us/support/faq/2680/)

```
pip3 install pytapo
```
```
pip3 install onvif-zeep (dunno if needed for the second, but this were my steps)
```
```
pip3 install onvif-zeep-async 
```
(if you want to use my whole script, get opencv and pushbullet too)

Go to the [onvif-zeep-async](https://github.com/hunterjm/python-onvif-zeep-async) repo and download their wsdl folder. It is really important, as the onvif-zeep defs are broken. I also tested with the https://www.onvif.org/profiles/specifications/ and they work too. Run the script once, Python will tell you were to put the files. Run it again, it will tell you another directory. Run it again, it may work now, else copy all the files to that directory too. I know the ONVIFCamera() sets the path at the end, but this never worked for me properly. 

Code has a lot of comments, it is really dirty, needs a lot of improvement and because it was for my use, I left it with the import of cv2 and pushbullet, cos my use is to grab frames and sent them to my phone (the main feature any security camara needs to have). You can set this as a service, I left it overnight and the camera never complained.

If you know how to improve it, don't be shy, world needs more people like you.
