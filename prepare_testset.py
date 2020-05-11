import os
import sys
import glob
import pickle
import datetime
import numpy as np
from tqdm import tqdm
from pydub import AudioSegment


currentPath = os.getcwd()
org_path = currentPath + '/testset-orginal'
dest_path = currentPath + '/testset-cleaned'
audioList = glob.glob(org_path + '/*.wav') + glob.glob(org_path + '/*.mp3')


now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
sys.stderr.write('[INFO %s] start preparing testset\n' % now)
for audio_path in audioList:
    file_name = audio_path.split('/')[-1]
    file_name, audio_type = file_name.split('.')
    speaker_path = dest_path + '/' + file_name
    os.makedirs(speaker_path, exist_ok=True)
    
    
    
    if os.path.isfile(audio_path.replace(audio_type, 'txt')):
        lyric_path = audio_path.replace(audio_type, 'txt')
    elif os.path.isfile(audio_path.replace(audio_type, 'lab')):
        lyric_path = audio_path.replace(audio_type, 'lab')
    else:
        raise Exception('[ERROR] the %s lyrics does not exist' % file_name)
        

        
    if audio_type == 'wav':
        audio = AudioSegment.from_wav(audio_path)
    elif audio_type == 'mp3':
        audio = AudioSegment.from_mp3(audio_path)
    else:
        raise Exception('Cannot recognize the file extension: %s' % audio_type)
    
    audio = audio.set_sample_width(sample_width=2)
    audio.export(speaker_path + '/' + file_name + '.wav', format='wav')

    

    haveTimeLine = False
    timeLine = {}
    lyrics = ''

    lyricLines = open(lyric_path, 'r')
    if all([file_name + '-' in i for i in lyricLines.readlines()]):
        haveTimeLine = True


    lyricLines = open(lyric_path, 'r')
    for line in lyricLines.readlines():
        if haveTimeLine: 
            name_and_time, tmp_lyrics = line.split(' ', 1)
            name, start_time, end_time = name_and_time.split('-')

        else:
            tmp_lyrics = line


        tmp_lyrics = tmp_lyrics.replace('<unk>', '').upper().strip()
        if haveTimeLine:
            timeLine[tmp_lyrics] = (int(start_time)/100, int(end_time)/100)

        lyrics = lyrics + tmp_lyrics + '\n'


    with open(speaker_path + '/' + file_name + '.lab', 'w') as f:
        f.write(lyrics)

    if haveTimeLine:
        with open(speaker_path + '/' + file_name + '.pkl', 'wb') as f:
            pickle.dump(timeLine, f, protocol=pickle.HIGHEST_PROTOCOL)
            

now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
sys.stderr.write('[INFO %s] testset audioes are ready\n' % now)