# Psychopy with URFUNNY stimulus

To run the paradigm, please download the standalone psychopy software from https://www.psychopy.org/download.html and have lsl (LabStreamingLayer) installed on your computer. You can install lsl through: 

`pip install pylsl`

After opening the software, please open the `Ollie_URFUNNY_sample` in the coder window and click "run" (the green circle on top of the editor) to run the paradigm. You can hit "escape" to quit the paradigm at any time. 

In default, the paradigm will only display the training video, and two stimuli, one in large size and one in small size as a demo. If you want to see all the stimulus, please include all the stimuli in line 26 and 27. 


## Update 8.7.2023
1. All the non-funny stimuli are replaced with funny stimuli since majority of the clips are serious 
2. Added Instruction 
3. Change event marker type to strings 

## Material
This is the paradigm for my pilot humor study. There are 20 stimuli included in the folder. Each stimuli lasts for 45 seconds. 

In each trial: 
1. 1s fixation cross at the center to guide subject's attention 
2. Autoplay the stimulus
3. In the mean time, slide bar at the bottom to indicate subjective funniness rating 
4. Attention question after the video stimulus 

In the pilot study, each video are either displayed in size (1244, 700) or (455, 256) to see which size works better. 

## Todo
1. (optional) add attention questions for each stimuli 