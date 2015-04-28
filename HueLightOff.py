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


b=Bridge('192.168.44.171')

# Get a flat list of the light objects
lights=b.get_light_objects('list')

LightName=lights[LightId].name
print 'Changing light id %s (%s) to OFF ...' % (LightId,LightName)

b.set_light(LightId,'on',False)
lights[LightId].on=False
#b.set_light(lights[LightId].name,'bri',LightIntensity)
#b.set_light(lights[LightId].name,'hue',LightHue)
#b.set_light(lights[LightId].name,'sat',LightSaturation)

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
