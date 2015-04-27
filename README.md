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

More details to come...  I'm new to git/Github, and am anxious just to push this out there, because I know 
there are others struggling with why the old W800RF32 driver will not properly report activity on DS10As.

The code is sloppy as shit.  There is VERY little documentation.  `\o/`

Raymond Spangle
git@leper.org
