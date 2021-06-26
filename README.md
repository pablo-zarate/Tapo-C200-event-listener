# Tapo-C200-motion-listener
ONVIF listener for Tapo C200 (and probably more cameras)


Ok, here is the deal, I am not native english speaker, so I'll try my best:

I made this script to listen for events on the TP-Link Tapo C200. This is not because I hate [HASS](https://www.home-assistant.io/) (which is awesome!) but to know how to do it. Also the example from [onvif-zeep-async](https://github.com/hunterjm/python-onvif-zeep-async) made it possible, this is just a fork of their work. Also many thanks to [pytapo](https://github.com/JurajNyiri/pytapo), the lib that made me not return the camera because of the lack of cloud support haha.

I tested this with a Raspberry Pi 4B, latest os. I assume you already know how to setup your camera for pytapo but if it is not the case, check [TP-Link's guide](https://www.tp-link.com/us/support/faq/2680/)

```
pip3 install pytapo
```
```
pip3 install onvif-zeep (dunno if needed for the second, but this were my steps)
```
```
pip3 install onvif-zeep-async 
```

Go to the [onvif-zeep-async](https://github.com/hunterjm/python-onvif-zeep-async) repo and download their wsdl folder. It is really important, as the onvif-zeep defs are broken. I also tested with the https://www.onvif.org/profiles/specifications/ and they work too. Please note that, if Python says it can't find some wdsl file, just surrender, make the folder and let it be. 

Code has a lot of comments, really dirty, needs a lot of improvement and because it was for my use, I left it with the import of cv2 and pushbullet, cos my use is to grab frames and sent them to my phone, the main feature a security camara needs to have. You can set it as a service, I left it overnight and the camera never complained.

If you know how to improve it, don't be shy, world needs more people like you.
