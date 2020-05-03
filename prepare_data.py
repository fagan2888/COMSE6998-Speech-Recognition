import os
import sys
import glob
import shutil
import numpy as np
from tqdm import tqdm
from pydub import AudioSegment


currentPath = os.getcwd()
wavList = glob.glob(currentPath + '/org_audio/*.wav')
background_music = AudioSegment.from_wav(currentPath + '/background.wav')


file = open(currentPath + '/text', 'r')
scriptDict = {}
checkAudioSet = []


sys.stderr.write('[INFO] collecting all segments\n')
for line in file.readlines():
    audio_name, seg_start, seg_end = line.split(' ')[0].split('-')
    audio_path = currentPath + '/org_audio/' + audio_name + '.wav'
    
    if scriptDict.get(audio_path) is None:
        scriptDict[audio_path] = {}
        

    # some segments do not have any acoustic
    try:
        scriptDict[audio_path][(seg_start, seg_end)] = {
            'seg_start': seg_start,
            'seg_end': seg_end,
            'script': line.split(' ', 1)[1].strip(),
            'wav_name': line.split(' ')[0] + '.wav',
            'lab_name': line.split(' ')[0] + '.lab'
        }
    except IndexError:
        continue
    checkAudioSet.append(audio_path)
    
    

sys.stderr.write('[INFO] segmenting files\n')
if set(checkAudioSet) == set(wavList):
    i = 1
    
    for audio_path, segDict in tqdm(scriptDict.items()):
        
        audio = AudioSegment.from_wav(audio_path)
        
        # create folder
        dest_path = currentPath + '/segmented_audio/' + str(i)
        if os.path.exists(dest_path):
            shutil.rmtree(dest_path)
        os.mkdir(dest_path)
        
        
        for _, seg_info in segDict.items():
            
            # it works in milliseconds
            seg_start = np.floor(int(seg_info['seg_start']) / 100) * 1000
            seg_end = np.ceil(int(seg_info['seg_end']) / 100) * 1000
            
            
            # select the background music length
            back_start = np.random.randint(background_music.duration_seconds) * 1000
            back_end = np.floor(min(background_music.duration_seconds, back_start + 30)) * 1000
            tmpBackground = background_music[back_start: back_end]
            # reduce the background music volume
            tmpBackground = tmpBackground - 3
            
            
            # select the interval of audio
            tmpAudio = audio[seg_start: seg_end]
            # adding background music
            tmpAudio = tmpAudio.overlay(tmpBackground)
            # change to bits per sample to 16
            tmpAudio = tmpAudio.set_sample_width(sample_width=2)
            # export segmented audio with background music
            # with mono channel
            tmpAudio.export(dest_path + '/' + seg_info['wav_name'], format='wav') #, parameters=["-ac", "1", "-b", "16k"]
            
            
            # export script for the wav
            with open(dest_path + '/' + seg_info['lab_name'], 'w') as f:
                f.write(seg_info['script'].upper())
            
        i += 1
else:
    raise Exception('audio and text unmatched: \ntext set: %s\n\naudio set: %s\n' % (
        list(set(checkAudioSet)), list(set(wavList))
    ))