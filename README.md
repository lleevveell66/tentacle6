BERTHA - Tentacle 6
-------------------

http://www.leper.org/BERTHA/

This is code for a "tentacle" of BERTHA (Basic Entity Realization for Home Automation).

This "tentacle" is being built on a Raspberry Pi B+ running Raspbian GNU/Linux 7.  The purpose of this 
tentacle is to bridge received X-10 data to Zigbee.  On the X-10 side, I have an old W800RF32 X-10 receiver
hooked into a USB port on the RPI via a QVS UR-2000M2 "USB to Serial" cable.  The W800RF32 is being used 
because it was the only receiver I could find with the range of my entire lot (house and yard).  It came with
and external antenna which could be mounted up high for better reception.  The document describing the protocol
on this receiver can be read, here: http://www.wgldesigns.com/protocols/w800rf32_protocol.txt (and a copy has 
placed in the doc/ directory.)  The problem is that they never fully understood the "extended X10" 
protocol and my DS10A Door/Window sensors would show up crazy.  Thus, I wrote my own program to properly
read both standard and extended X10 protocols received on the W800RF32.

I also wrote some scripts to control lighting via my Hue Hub from this RPI.  That is done via wifi.  I have 
many Wink/Quirky (GE) bulbs being controlled by the Hue Hub.  Tentacle 6 will amass X-10 sensor data for BERTHA, 
but also allow BERTHA to control Zigbee lighting via the Hue Hub.  Thus... a bridge.

You will want to do the following:

<pre>
1) edit WatchX10 and:
  - set $DEBUG=1
  - set your comport, if it's not /dev/ttyUSB0
  - change the log file, if you want
2) run WatchX10 and trip your X10 sensors in every way possible, marking down their IDs:
  - ex.   04/28/15 01:52:31 155:Unknown Device:ALERT
            date     time   id   desc       function or message
3) edit the bertha.devices file to give all of your devices some descriptions:
  - ex.    155:My Front Door
            id  desc
4) edit the bertha.actions file to give all of your unit/functions some actions to perform.
  - ex.    155:ALERT:MyDoorOpen
           155:NORMAL:MyDoorClosed
            id  function   action script
  - build actions scripts in the actions/ directory named the same as above, even if there is nothing you want 
    to do - make it an empty bash script that exits or something.  There is no error detection for these, yet.
  - feel free to use any of the Hue*.py scripts I have written for controlling Zigbee devices via Hue Hub, 
    but if you do,        change this line to match your Hub's IP address:
    b=Bridge('192.168.44.171')
5) re-run WatchX10 and watch the fun
</pre>

More details to come...  I'm new to git/Github, and am anxious just to push this out there, because I know 
there are others struggling with why the old W800RF32 driver will not properly report activity on DS10As.

The code is sloppy as shit.  There is VERY little documentation.  `\o/`

LEVEL6
https://github.com/lleevveell66
