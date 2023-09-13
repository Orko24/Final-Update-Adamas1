'''

Modified & original work Copyright (c) 2022 Hemanto Bairagi


This code is the sole property of Hemanto Bairagi. 
Any unauthorized replication and use of any code used 
in any form will be a violation of my exclusive Copyright. 

'''

from .service import Regression
from django_rq import job

from voice_production.sangenius_complete.PDF_compression import *
from voice_production.sangenius_controls import *
from voice_production.sangenius_complete.Audio_merger import *

import os
import sys
from pathlib import Path

# import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

@job
def test_calc3(source):


    R = Regression()
    rmse = R.get_rmse()

    return rmse


@job
def a_s_pc(new_files):

    function = admin_pdf_compression_multi(new_files)
    compressed_files = function.admin_pdf()
    return compressed_files

''''
conventional

'''

@job
def conv_default(full_file_path, temp_file = "temp.pdf"):

    custom_voice = conventional_voice(filename=full_file_path, modified_file = temp_file)
    file_out_put = custom_voice.audioproduction()

    return file_out_put


@job
def conv_custom(full_file_path, values, temp_file = "temp.pdf"):

    form_val = str("." + values[0])
    vol_type = int(values[1])
    sr = int(values[2])
    vr = float(values[3])

    custom_voice = conventional_voice(filename=full_file_path, rate_sp=sr, vol=vr, voice_type=vol_type,
                                      form_now=form_val, modified_file = temp_file)

    file_out_put = custom_voice.audioproduction()

    return file_out_put

'''
async note functions

1) conventional audio default:



'''

@job
def synthetic_voice(file_path, audio_path, temp_path = "test"):

    synth_voice = backend_synthetic_voice(filename=os.path.abspath(file_path), audio_train=audio_path, temp_files = temp_path)
    output_file = os.path.abspath(synth_voice.aud_production())

    # os.path.abspath(output_file)

    return output_file




@job
def Large_file_merger(file_paths, end_file):

    admin_batch(file_paths, end_file=end_file).admin_run()
    end_file_name = "merged_audio.mp3"

    return end_file_name

@job
def mid_file_merger(total_file_lst, upload_folder_pdf, end_file, end_file_name = "merged_audio.mp3"):



    count_2 = 0
    resultant_files = []

    print("asynchronous function activated")
    end_file_name = "merged_audio.mp3"
    for files in total_file_lst:

        print(upload_folder_pdf)

        end_file_output = os.path.join(upload_folder_pdf, "{}.mp3".format(count_2))

        print(end_file_output)

        print('The file being produced is: ', end_file_output)

        '''
        maybe throw these lines of code and see what happens
        
        admin_batch(file_paths, end_file=end_file).admin_run()
        end_file_name = "merged_audio.mp3"
        
        if it works then wallah, still finish up java tho as an alternative engine
        
        '''

        admin_batch(files, end_file=end_file_output).admin_run()
        # end_file_name = "merged_audio.mp3"

        '''
        audio merge files here python subprocess goes here once you finish Java compilation
        convert mp3 files to wav files before throwing it into java or have java convert it
        or use C++ to convert MP3 files to wav files before throwing it into Java, which maybe easier
        
        '''

        # audio_combiner(audio_clip_paths=files, output_path=end_file_output).concatenate_audio_moviepy()
        resultant_files.append(end_file_output)
        count_2 = count_2 + 1


    print('the resultant files are: ', resultant_files)

    out_put_folder = os.path.join(BASE_DIR, "main\\Website\\output_files")

    admin_batch(audio_lst=resultant_files, end_file=end_file).admin_run()



    return end_file_name

@job
def small_files(files_, end_file, upload_folder_pdf):

    file_paths_ = []
    for files in files_:
        file_path_ = upload_folder_pdf + "\\{}".format(files)
        file_paths_.append(file_path_)

    audio_combiner(audio_clip_paths=file_paths_, output_path=end_file).concatenate_audio_moviepy()
    return end_file





