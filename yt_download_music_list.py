
#* Script for downloading list of YouTube videos using yt-dlp, converting them to mp4 using ffmpeg and then concatenating these videos into one single file
#* ver. 1.0
#? HOW TO USE:
#? Script scans the file videos_url_list.txt (line by line) and finds the video URL, then it downloads the video, converts it and concatenates with other videos
#? Run in the shell:
#? python3 yt_download_music_list.py
#! CAUTION 1: script uses ffmpeg and yt-dlp (the last one has to be in the same directory as the script itself)
#! CAUTION 2: ffmpeg activates the NVIDIA CUDA cores while converting videos

import os
import time
import datetime

# STEP 1: Download videos using yt-dlp
print('##############################')
print('# STEP 1: Videos Downloading #')
print('##############################')

os.makedirs('downloaded')

time_download_start_time = time.time()

with open('videos_url_list.txt', 'r', encoding='utf8') as file:
    
    name = 1

    for i in file:
        
        print('=== [DOWNLOADING: %d] ===' % name)
        os.system('yt-dlp.exe -o /output/'+str(name)+' '+i+'')
        print('=== [DOWNLOAD FINISHED: %d] ===' % name)

        name+=1

time_download_finish_time = time.time()


# STEP 2: Correct the PTS and FPS of converted files using ffmpeg
print('####################################################')
print('# STEP 2: Videos Converting and PTS/FPS Correction #')
print('####################################################')

if not os.path.exists(os.curdir+'converted_final'):
    os.makedirs('converted_final')

time_conv_corr_start_time = time.time()

for f in os.listdir('downloaded'):

    filename_downloaded = f.split('.')[0]

    print('=== [CONVERTING AND CORRECTING: %s] ===' % filename_downloaded)
    # NVIDIA h264 NVENC encoder with compression (-cq:v or -cq option)
    #os.system('ffmpeg -y -hwaccel cuda -i '+os.curdir+'/downloaded/'+f+' -vcodec h264_nvenc -preset p7 -cq 28 -vf "setpts=1.25*PTS" -r 30 '+os.curdir+'/converted_final/'+str(filename_downloaded)+'.mp4')
    # x264 encoder with compression (-crf option)
    os.system('ffmpeg -y -hwaccel cuda -i '+os.curdir+'/downloaded/'+f+' -vcodec libx264 -crf 28 -preset veryfast -vf "setpts=1.25*PTS" -r 30 '+os.curdir+'/converted_final/'+str(filename_downloaded)+'.mp4')
    print('=== [CONVERTING AND CORRECTION FINISHED: %s] ===' % filename_downloaded)

time_conv_corr_finish_time = time.time()


# STEP 3: Concatenate converted and corrected files into single one using ffmpeg
print('##################################################')
print('# STEP 3: Videos Concatenation into single video #')
print('##################################################')
    
with open(os.curdir+'/converted_final/videos.txt', 'w', encoding='utf8') as videos_list_concat:

    for f in os.listdir('converted_final'):
        if f.endswith('.mp4'):
            videos_list_concat.write('file \''+f+'\'\n')

time_concat_start_time = time.time()

os.system('ffmpeg -f concat -i '+os.curdir+'/converted_final/videos.txt -c copy '+os.curdir+'/converted_final/music_final.mp4')

time_concat_finish_time = time.time()


print(' ---> [DOWNLOAD TIME (H:M:S)]:', str(datetime.timedelta(seconds = (time_download_finish_time - time_conv_corr_start_time))))
print(' ---> [CONVERSION TIME (H:M:S)]:', str(datetime.timedelta(seconds = (time_conv_corr_finish_time - time_conv_corr_start_time))))
print(' ---> [CONCATENATION TIME (H:M:S)]:', str(datetime.timedelta(seconds = (time_concat_finish_time - time_concat_start_time))))
