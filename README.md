yaas
====

Yet another ableton script

Compatible with Ableton Live 9

So, although there are many ableton script, I had my problems with them so I decided to create a new one.
Probably you will have problems with mine too :)

What I try to create:
- Easily configurable script
- Functionality at least MackieControl
- Additionally function needed for live performing/jamming like looping
- Inclusion of other scripts would be very nice, i.e. ClyphX
- Easy to extend, just add a class and use it in configuration

I would love to write things down in a blog or wiki, so that others like me have a faster start. I tend to concentrate to much on technical things than making music, but the target of this hole thing is to make jamming easier for me.

What it can do at the moment:
- configure keys and mappings in consts.py#
- select a Hash_Device, that means one of the devices in the set which has a name starting with '#'
  with a pedal or knob you can now change the first two device parameters 
- switch between chains on the device with midi keys
- define a max value for device controllers in the set (so you can adapt the mix to your surrounding, eg if you have an instrument loud enough to be heard already you can allow the full value. but if you can't hear your instrument you want to allow only a lower value so that you have a nice mix. 
  afterwards you can press your pedal or turn your nob to the maximum and get the perfect mix without thinking about it
- it shows a red rectangle. The clips in the rectangle are startable or stoppable via midi keys
- normal track operations
  stop, play, change first two returns, select certain track, enable record
- controller actions
  metonom on/off, set metronome, next track, previous track, next scene, previous scene, play scene, play clip

Examples for the FCB1010 (a footswitch with 10 buttons and two pedals) will show a examplethe possible mappings

If your interested in easily creating a controller and assigning its controls to ableton command,
please contact me and i will help you set it up
I need feedback and help :)

Next steps
I want to use this as a single point to control all my midi input controllers
Also add an android app for controlling ableton
Then enable sensors to communicate with the script

The big picture
Create or find new ways to control music
Electronic music is to abstract at the moment. You don't see what the artists do
But if they had meaningful installation the viewers would get much more of what the artists do really (or is it all a recorded track?)
Also
Create a environment for non-musician where they can explore and participate in music playfully
There are no wrong notes or bad timing. Everything you do is ok and will show up in the played musc
Many people can together play a song and have fun without having to learn music making


