#!/usr/bin/python

import sys,getopt,logging
from phue import Bridge

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

print 'Changing light id %s to hue of %s, intensity of %s, and saturation of %s ...' % (LightId,LightHue,LightIntensity,LightSaturation)

b=Bridge('192.168.44.171')

# Get a flat list of the light objects
lights=b.get_light_objects('list')

b.set_light(lights[LightId].name,'hue',LightHue)
b.set_light(lights[LightId].name,'sat',LightSaturation)
b.set_light(lights[LightId].name,'on',False)

command={'transitiontime':150,'on':True,'bri':LightIntensity}
b.set_light(lights[LightId].name,command)

command={'transitiontime':1}
b.set_light(lights[LightId].name,command)

#for fade in range(0,LightIntensity,10):
# b.set_light(lights[LightId].name,'bri',fade)

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
