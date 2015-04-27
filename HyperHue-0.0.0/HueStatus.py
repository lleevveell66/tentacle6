#!/usr/bin/python
from phue import Bridge
b=Bridge('192.168.44.171')

# Get a flat list of the light objects
lights_list = b.get_light_objects('list')

for light in lights_list:
 if (light.on == True):
#  LightName=b.get_light(light, 'name')
  LightName=light.name
  print "%s is ON" % LightName
 else:
  print "%s is OFF" % LightName

exit(0)
