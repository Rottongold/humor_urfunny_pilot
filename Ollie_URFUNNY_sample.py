from __future__ import absolute_import, division
from psychopy import locale_setup, visual, core, event
import numpy as np
from random import shuffle

win = None # Global variable for window (Initialized in main)
bg_color = [0, 0, 0]
win_w = 1920#2560
win_h = 1080#1440
refresh_rate = 165. # Monitor refresh rate (CRITICAL FOR TIMING)

#----------------------------------Define Helper Function--------------------------------------------
def MsToFrames(ms, fs):
    dt = 1000 / fs;
    return np.round(ms / dt).astype(int);

# ---------------------------------Initialize variables----------------------------------------------- 
win = visual.Window( 
        screen = 0,
        size=[win_w, win_h], 
        fullscr=False,
        color=[0, 0, 0],
        gammaErrorPolicy = "ignore"
    )

large = [14052]#, 11787, 14889, 11262, 11144, 9338, 10482, 13366, 14527, 8019]
small = [14445]#, 13740, 263, 9286, 11090, 5219, 3342, 4541, 13179, 11768]
mov_stim = []
dir_to_folder = './urfunny2_videos/'

training_mov = visual.MovieStim(
    win,
    './training_video.mp4',
    size=(1244, 700),
    flipVert=False,
    flipHoriz=False,
    pos = (0, 0.5),
    loop=False,
    noAudio=False,
    volume=0.1,
    autoStart=True)
    
for mov in large:
    vid_path = dir_to_folder + str(mov) + '.mp4'
    
    temp_mov = visual.MovieStim(
    win,
    vid_path,
    size=(1244, 700),
    flipVert=False,
    flipHoriz=False,
    pos = (0, 0.5),
    loop=False,
    noAudio=False,
    volume=0.1,
    autoStart=True)
    
    temp_mov.pos = (0, 0)
    
    mov_stim.append(temp_mov)
    
for mov in small:
    vid_path = dir_to_folder + str(mov) + '.mp4'
    
    temp_mov = visual.MovieStim(
    win,
    vid_path,
    size=(455, 256),
    flipVert=False,
    flipHoriz=False,
    loop=False,
    noAudio=False,
    volume=0.1,
    autoStart=True)
    
    mov_stim.append(temp_mov)
    
    shuffle(mov_stim)
    
fixation = visual.TextStim(win, "+", font='Open Sans', units='pix', 
                pos=(0,0), alignText='center',
                height=80, color=[1, 1, 1]
                )
    
Consent = visual.TextStim(win, "Sample Instructions, press space to continue", font='Open Sans', units='pix', 
                pos=(0,0), alignText='center',
                height=36, color=[1, 1, 1]
                )
                
Training_Ins = visual.TextStim(win, "Training Trials, press space to continue", font='Open Sans', units='pix', 
                pos=(0,0), alignText='center',
                height=36, color=[1, 1, 1]
                )

Instruction = visual.TextStim(win, "For each of the following trials, a video clip will be automatically played at the beginning of the trials. Please pay close attention to each of the clip, as you will be prompted to answer comprehension questions after each clip. In the meantime, there will be a slider bar at the bottom of each video. Pressing left or rigth arrow key will adjust the values on the slider bar. From 1 (very serious) to 5 (very funny), please indicate your feeling toward the video. Press space to continue",
                            font='Open Sans', units='pix', 
                pos=(0,0), alignText='center',
                height=36, color=[1, 1, 1]
                ) 
                
Question = visual.TextStim(win, "Attention Question. If the statement is True, press y, if the statement is false, press n.")

slider = visual.Slider(win=win, name='radio',
    size=(1.0, 0.1), pos=(0, -0.8),
    labels=['1','2','3','4','5'], ticks=(1, 2, 3, 4, 5),
    granularity=0, style=['rating'],
    color='LightGray', font='Open Sans',
    flip=False)
     
while True:
    Consent.draw()
    win.flip()
    
    if event.getKeys(['space']):
        break
    elif event.getKeys(['escape']):
        core.quit()
    else:
        continue

while True:
    Training_Ins.draw()
    win.flip()
    
    if event.getKeys(['space']):
        break
    elif event.getKeys(['escape']):
        core.quit()
    else:
        continue
        
slider.reset()
slider.markerPos = 2

for i in range(MsToFrames(2000, refresh_rate)):
    fixation.draw()
    win.flip()
    
    
while not training_mov.isFinished:
    
    #mov.play()
    training_mov.draw()
    slider.draw()
    win.flip()
    
    keys = event.getKeys()
    if keys:
        if 'left' in keys:
            slider.markerPos -= 1
        elif 'right' in keys:
            slider.markerPos += 1
        elif 'escape' in keys:
            core.quit()
            
training_mov.unload()
    
while True:
    Question.draw()
    win.flip()
    keys = event.getKeys()
    
    if 'y' in keys:
        break
    elif 'n' in keys:
        break
    elif 'escape' in keys:
        core.quit()
    else:
        continue

for mov in mov_stim:
    
    slider.reset()
    slider.markerPos = 2
    
    for i in range(MsToFrames(2000, refresh_rate)):
        fixation.draw()
        win.flip()
        
        
    while not mov.isFinished:
        
        #mov.play()
        mov.draw()
        slider.draw()
        win.flip()
        
        keys = event.getKeys()
        if keys:
            if 'left' in keys:
                slider.markerPos -= 1
            elif 'right' in keys:
                slider.markerPos += 1
            elif 'escape' in keys:
                core.quit()
                
    mov.unload()
        
    while True:
        Question.draw()
        win.flip()
        keys = event.getKeys()
        
        if 'y' in keys:
            break
        elif 'n' in keys:
            break
        elif 'escape' in keys:
            core.quit()
        else:
            continue
            

# make sure everything is closed down
win.close()
core.quit()