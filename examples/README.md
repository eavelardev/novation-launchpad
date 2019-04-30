
You need a software synthesizer for convert convert MIDI data into sound. 
You can use `fluidsynth`:

```
fluidsynth --server --audio-driver=alsa -o audio.alsa.device=hw:0 /usr/share/sounds/sf2/FluidR3_GM.sf2
```
or
```
fluidsynth --server --audio-driver=jack --connect-jack-outputs /usr/share/sounds/sf2/FluidR3_GM.sf2
```

see the 
[Ted's Linux MIDI Guide](http://tedfelix.com/linux/linux-midi.html)
for more information

I use `Patchage` for link de MIDI ports.

In the examples I use the Launchpad Mk2, you can edit the examples for your device model.

For some examples you need to install `numpy` or `opencv-python` with `pip`, check the code.
