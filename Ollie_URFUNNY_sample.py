from __future__ import absolute_import, division
from psychopy import locale_setup, visual, core, event
import numpy as np
import pylsl
from random import shuffle

win = None # Global variable for window (Initialized in main)
bg_color = [0, 0, 0]
win_w = 1920#2560
win_h = 1080#1440
refresh_rate = 144. # Monitor refresh rate (CRITICAL FOR TIMING)

#----------------------------------Define Helper Function--------------------------------------------
def MsToFrames(ms, fs):
    dt = 1000 / fs;
    return np.round(ms / dt).astype(int);

# ---------------------------------Initialize lsl ---------------------------------------------------
info = pylsl.StreamInfo(name='humor_pilot', type='Markers', channel_count=1,
                      channel_format=pylsl.cf_string, source_id='example_stream_001')
outlet = pylsl.StreamOutlet(info)

#markers = {
#        'test' : [-1],
#        'training': [-9999],
#        'fix': [-100],
#        'on': [-200],
#        'humor': [-28],
#        'nonhumor': [-66],
#        'large': [-9],
#        'small': [-1],
#        'T': [-7],
#        'F': [-13],
#    }

# ---------------------------------Initialize variables----------------------------------------------- 
win = visual.Window( 
        screen = 0,
        size=[win_w, win_h], 
        fullscr= False,
        color=[0, 0, 0],
        gammaErrorPolicy = "ignore"
    )

humor = [14445, 263, 9286, 11090, 14889, 11262, 11144, 3774, 10200, 5260, 14225, 7821, 1300, 5445, 14302, 1772, 3960, 2289, 6691, 3810]

large = [14445, 263, 9286, 11090, 14889, 11262, 11144, 3774, 10200, 5260]
small = [14225, 7821, 1300, 5445, 14302, 1772, 3960, 2289, 6691, 3810]

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
    
    temp_mov = {
        "id" : mov,
        "size" : "large",
        "movie" : visual.MovieStim(
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
    }
    
    mov_stim.append(temp_mov)
    
for mov in small:
    vid_path = dir_to_folder + str(mov) + '.mp4' 
    
    temp_mov = {
        "id": mov,
        "size" : "small",
        "movie" : visual.MovieStim(
                win,
                vid_path,
                size=(455, 256),
                flipVert=False,
                flipHoriz=False,
                loop=False,
                noAudio=False,
                volume=0.1,
                autoStart=True)
    }
    
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
                
Training_Ins = visual.TextStim(win, "The following trial is a training trial, press space to continue", font='Open Sans', units='pix', 
                pos=(0,0), alignText='center',
                height=36, color=[1, 1, 1]
                )
                
Post_training_Ins = visual.TextBox2(win, "Good job! You finished the training trial. If you have any questions, please don't hesitate to ask the experimenter immediately. \n\n If you think you are ready for the official experiment, press space to continue", font='Open Sans', units='pix', 
                pos=(0,0), alignment='center',
                letterHeight=30, color=[1, 1, 1]
                )

Instruction = visual.TextBox2(win, "In the following session, some video clips extracted from TED Talk series will be automatically played in sequence. Your task is to indicate your feeling of seriousness/funniness of the video clip on the slider (shown below) using a 5 points scale (1 indicates super serious, and 5 indicates super funny) as the video is playing. You can change your rating by pressing the left or right arrow key to change the rating. Feel free to play with it now! \n\n Please note that the slider will remain on the screen for 1 extra second after the video ended to allow you indicate your feeling toward the end of the clip. After each video clip, an attention question will be asked to ensure you were paying attention. \n\n Please ask the experimenter now if you have any questions. We will also have a training session before the official experiment. \n\n  Press space to continue",
                            font='Open Sans', units='pix', letterHeight = 30,
                pos=(0,0), alignment='center',color=[1, 1, 1]
                ) 
                
Question = visual.TextStim(win, "Attention Question. \n If the statement is True, press y, if the statement is False, press n.")

slider = visual.Slider(win=win, name='radio',
    size=(1.0, 0.1), pos=(0, -0.8),
    labels=['1','2','3','4','5'], ticks=(1, 2, 3, 4, 5),
    granularity=0, style=['rating'],
    color='LightGray', font='Open Sans',
    flip=False)

# ---------------------------------------Instruction---------------------------------------------
slider.reset()
slider.markerPos = 3

while True:
    Instruction.draw()
    slider.draw()
    win.flip()
    
    keys = event.getKeys()
    if keys:
        if 'left' in keys:
            slider.markerPos -= 1
        elif 'right' in keys:
            slider.markerPos += 1
        elif 'space' in keys:
            break
        elif 'escape' in keys:
            core.quit()

# -----------------------------------------Training--------------------------------------------
outlet.push_sample(pylsl.vectorstr(["Training"]))
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
slider.markerPos = 3

for i in range(MsToFrames(1000, refresh_rate)):
    if str(i) == '0':
        outlet.push_sample(pylsl.vectorstr(["fixation"]))
    
    fixation.draw()
    win.flip()

outlet.push_sample(pylsl.vectorstr(["onset"]))
while not training_mov.isFinished:
    
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
            
    outlet.push_sample(pylsl.vectorstr([str(slider.getMarkerPos())]))
            
training_mov.unload()
outlet.push_sample(pylsl.vectorstr(["offset"]))

for i in range(MsToFrames(1000, refresh_rate)):

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
            
    outlet.push_sample(pylsl.vectorstr([str(slider.getMarkerPos())]))

while True:
    Question.draw()
    win.flip()
    keys = event.getKeys()
    
    if 'y' in keys:
        outlet.push_sample(pylsl.vectorstr(['T']))
        break
    elif 'n' in keys:
        outlet.push_sample(pylsl.vectorstr(['F']))
        break
    elif 'escape' in keys:
        core.quit()
    else:
        continue

while True:
    Post_training_Ins.draw()
    win.flip()
    
    if event.getKeys(['space']):
        break
    elif event.getKeys(['escape']):
        core.quit()
    else:
        continue
        
# ----------------------------- Experiment ----------------------------------------
for mov in mov_stim:

    outlet.push_sample(pylsl.vectorstr(['_'.join([str(mov["id"]), str(mov["size"])])]))
    mov = mov['movie']
    
    slider.reset()
    slider.markerPos = 3
    
    for i in range(MsToFrames(1000, refresh_rate)):
        fixation.draw()
        win.flip()

        if str(i) == '0':
            outlet.push_sample(pylsl.vectorstr(['fixation']))
        
    outlet.push_sample(pylsl.vectorstr(['onset']))    
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
        outlet.push_sample(pylsl.vectorstr([str(slider.getMarkerPos())]))
        
    outlet.push_sample(pylsl.vectorstr(['offset']))
    mov.unload()
    
    for i in range(MsToFrames(1000, refresh_rate)):
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
                
        
    while True:
        Question.draw()
        win.flip()
        keys = event.getKeys()
        
        if 'y' in keys:
            outlet.push_sample(pylsl.vectorstr(['T']))
            break
        elif 'n' in keys:
            outlet.push_sample(pylsl.vectorstr(['F']))
            break
        elif 'escape' in keys:
            core.quit()
        else:
            continue
            

# make sure everything is closed down
win.close()
core.quit()