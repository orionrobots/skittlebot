# Skittlebot

A robot to find a target and ram it.

## Demo

See <iframe width="560" height="315" src="https://www.youtube.com/embed/z14HcflsRW0" frameborder="0" allowfullscreen="yes"></iframe>

## Starting point

There are a few examples here.
The main goodness is skittle_track.py.

## Pibakery Setup

First use the PiBakery recipe here to get up and running. Ensure to use your own wifi credentials for it. Use the Raspbian Full image.

Log into your Raspberry Pi using the skittlebot.local via VNC.
At this point - you will want to increse the video memory on the pi, and the resolution, then reboot (TODO = bake this into that recipe).

## Running it

After the reboot, open up a terminal in VNC.

    export PYTHONPATH=~/piconzero
    cd skittlebot
    python skittle_track.py

You will now see the app running.

Jog the windows so you can see three windowsl

* The console - printed output
* The main image, what the camera has plus data on what the robot has found.
* The mask image - this shows what the robot has filtered.

Place the object of the right colour in front of the camera - the mask may show this in white, and the main image a circle along with X,Y coordinates for it.

Focus on the main image window, and you can now tune the robot. This is required for it to focus on the expected object.

Keyboard:

    a,s - adjust the minimum hue (down, up)
    k,l - adjust the maximum hue
    q,w - adjust minimum saturation
    o,p - adjust maximum saturation
    z,x - adjust minimum value (brightness)
    n,m - adjust maximum brightness
    g   - engage motors
    esc - quit

Use these keys to get as close to the target object being totally highlighted in white, and as little of the background highlighted as you can get. The range minimum and maximum values are shown in the console. You can copy those into the setup for the code to run again. Note - you may need to tune again if light conditions change significantly.

Once you can clearly pick out the object and it's X-Y, you can then engage the motors using the "g" key.

## Other code

* track_colour.py is a desktop app to test this. You will need python, opencv and numpy installed to run this.
* controlled_variable.py - a cheeky class to put a variable under keyboard control for adjustment
* skittlebot.py - creates a Robot class to send signals to the robot. Has a safety wrapper to stop motors if there's a fault.
* test_opencv_pi.py - just a simple test to see if we can get an image from the pi camera.

## Theory of operation

* First the robot sets up, initialising the systems.
* It then enters a main loop:
    * Get a frame from the camera
    * Convert to HSV
    * Perform the mask transformation on this image.
    * open/close the mask to reduce noise and speckles.
    * Search for contours on the mask
    * Find the contour groups.
    * Chosoe the largest
    * Create circle around the contour.
    * if the circles radius is greater than a threshold:
        * If it's left of center
            * Turn left (if motors on)
        * elif it's right of center
            * Turn right (if motors on)
        * else:
            * Drive forward and ram (if motors on)
    * else:
        * Turn and seek targets (if motors on)
    * Check for keypresses from the ui and process them

## TODO

* Make it smoother - perhaps using a video mode and frame sampling could do this, but the rolling shutter may make things difficult. The slowest aspect is the latency in taking a shot, especially in less-than-daylight conditions.
* Add voice control - with a set of preprogrammed ranges.
* Add a training mode - ie snapshot, drag a line across a range of colour in an object and automatically create the range profile.
* make it push a ball - more skittle like. I was just after targets to knock over, but this sounds like fun.
* Do demos with line sensors and hc-sr04 involved, or build the simpler one based on the CamJam robot kit.