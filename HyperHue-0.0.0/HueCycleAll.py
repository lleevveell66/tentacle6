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

b=Bridge('192.168.44.171')

# Get a flat list of the light objects
lights=b.get_light_objects('list')

light1=lights[0]
light2=lights[1]

light1.on=False
light2.on=False
light1.on=True
light2.on=True
sleep(1)
light1.transitiontime=1
light2.transitiontime=1
light1.brightness=LightIntensity
light2.brightness=LightIntensity
light1.saturation=LightSaturation
light2.saturation=LightSaturation
light1.hue=LightHue
light2.hue=LightHue
sleep(1)

LightHue=1
LightHue2=LightHue+1000
light1.transitiontime=10
light2.transitiontime=10
light1.hue=LightHue
light2.hue=LightHue
sleep(1)
light1.hue=LightHue2
light2.hue=LightHue2

while(1):
 if(LightHue2>65000):
  LightHue=1
  LightHue2=LightHue+1000
 else:
  LightHue=LightHue2
  LightHue2=LightHue+1000
  light1.transitiontime=10
  light2.transitiontime=10
  light1.hue=LightHue2
  light2.hue=LightHue2
  print 'Rotating hues l=%s, i=%s, s=%s, h1=%s, h2=%s' % (LightId,LightIntensity,LightSaturation,LightHue,LightHue2)
  sleep(1)

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
