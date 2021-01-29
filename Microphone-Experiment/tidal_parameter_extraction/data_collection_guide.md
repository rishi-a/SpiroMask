## Data Collection Guide for Tidal breathing samples

#### We are collecting tidal samples for parameter extraction as well as for training speech-nonspeech classifier. 

Masks types used - N95 , cloth masks


    This is a lap 

    #10 s - break           0-10     
    
    #30 s - tidal breathing 10-40    breath normally through nose. 
    
    #10 s - break           40-50    
    
    #30 s - speaking        50-80	 read some paragraph
    
    #10 s - break           80-90 
    
    #30 s - tidal with noise 90-120  breath normally with some background noise playing in laptop (crowd noise on Youtube)

We collect 3 laps for each mask type

File save format

Rohit_Tidal_N95_lap1.wav


### for collecting data, use record_audio.py script.
connect the arduino and put corresponding port in the code.
Data will start recording when you press Enter.

After a lap is completed press Ctrl-C to stop recording
you can see the plot, refer to the plots in "fig/" folder, this is what the plots should look like.
Save the file with corresponding save format.

Thanks!
