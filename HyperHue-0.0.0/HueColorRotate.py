#!/usr/bin/python

import sys,getopt,logging
from phue import Bridge
from time import sleep

logging.basicConfig()

try:
 opts,args=getopt.getopt(sys.argv[1:],"l:h:i:s:",["lid=","hue=","int=","sat="])
except getopt.GetoptError: 
 print 'HueChange.py -l <light_id> -h <hue> -i <intensity> -s <saturation>'
 sys.exit(2)

LightId=1;
LightHue=0;
LightIntensity=0;
LightSaturation=0;

for opt,arg in opts:
 if opt=='--help':
  print 'HueChange.py -l <light_id> -h <hue> -i <intensity>'
  sys.exit()
 elif opt in ("-l", "--lid"):
  LightId=int(arg)
 elif opt in ("-h", "--hue"):
  LightHue=int(arg)
 elif opt in ("-i", "--int"):
  LightIntensity=int(arg)
 elif opt in ("-s", "--sat"):
  LightSaturation=int(arg)

print 'Rotating hues on light id %s, with intensity of %s, and saturation of %s ...' % (LightId,LightIntensity,LightSaturation)

b=Bridge('192.168.44.171')

# Get a flat list of the light objects
lights=b.get_light_objects('list')

light=lights[LightId]

light.on=False
light.on=True
sleep(1)
light.transitiontime=1
light.brightness=LightIntensity
light.saturation=LightSaturation
light.hue=LightHue
sleep(1)
light.transitiontime=50
light.hue=65000
sleep(1)

#b.set_light(lights[LightId].name,transitiontime=1)

#b.set_light(lights[LightId].name,'sat',LightSaturation)
#b.set_light(lights[LightId].name,'bri',LightIntensity)
#b.set_light(lights[LightId].name,'hue',1)

#for hue in range(0,65534,1000):
#b.set_light(lights[LightId].name,'hue',65534,transitiontime=1)

#command={'transitiontime':150,'on':True,'bri':LightIntensity}
#b.set_light(lights[LightId].name,command)

#command={'transitiontime':1}
#b.set_light(lights[LightId].name,command)


exit(0)

for light in lights_list:
 if (light.on == True):
#  LightName=b.get_light(light, 'name')
  LightName=light.name
  LightHue=512;
  b.set_light(LightName,'hue',LightHue);
  print "%s hue is now %s" % (LightName,LightHue)
 else:
  print "%s is OFF" % LightName

exit(0)
