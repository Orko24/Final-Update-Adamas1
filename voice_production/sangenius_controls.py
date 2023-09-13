'''

Modified & original work Copyright (c) 2022 Hemanto Bairagi


This code is the sole property of Hemanto Bairagi. 
Any unauthorized replication and use of any code used 
in any form will be a violation of my exclusive Copyright. 

'''

from voice_production.module_2 import *
from voice_production.sangenius_complete.Text_audio_fix import *

# import os

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


## Finish the software off

class conventional_voice(object):
    
    def __init__(self, filename, iterative_space=100, intra_space=25,
                 form_now=".mp3", rate_sp=185, vol=1.0, voice_type=0, limit=150, modified_file = "temp.pdf"):
        self.filename = filename
        self.length_pdf = PdfFileReader(self.filename).numPages
        self.iterative_space = iterative_space
        self.intra_space = intra_space
        self.form_now = form_now
        self.rate_sp = rate_sp
        self.vol = vol
        self.voice_type = voice_type
        self.end_file = self.filename[:-4]
        self.limit = limit
        self.modified_file = modified_file

    def audioproduction(self):


        print('audioproduction has been activated')
        print('the self modified file is as follows: ')
        print(self.modified_file)

        sangenius_audio(filename = self.filename, rate_sp= self.rate_sp,
                        vol= self.vol, voice_type=self.voice_type,
                        iterative_space= self.iterative_space,
                        intra_space=self.intra_space, limit= self.limit,
                        form_now= self.form_now, modified_file = self.modified_file).admin_audio()

        print(self.filename[:-4] + self.form_now)

        return self.filename[:-4] + self.form_now


class synthetic_voice(object):
    
    def __init__(self,filename, audio_train, output_file = "crazyjess.wav", limit_page = 6, temp_files = "test"):

        self.filename = filename

        self.audio_train = audio_train

        self.output_file = output_file
        self.limit_page = limit_page
        self.temp_files = temp_files


    def audio_production(self):

        audio = synthetic_audio_gen(filename = self.filename, audio_train = self.audio_train,
                                    output_file = self.output_file, temp_files = self.temp_files)
        audio.exec_gen()

        ''':cvar
        generates synthetic audio in wave format
        '''

        return self.output_file

    def audio_gen(self):

        print("working")

        leng_pdf = PdfFileReader(self.filename).numPages

        if leng_pdf <= self.limit_page:
            self.audio_production()

        else:
            print("Please enter a pdf with less than {} pages, the current build of the website \n".format(self.limit_page) +
                  "cannot process it but maybe able to in the future as more features are offered")

        return

'''
synthetic voice for backend
'''

class backend_synthetic_voice(object):

    def __init__(self,filename, audio_train, output_file = "crazyjess.wav", limit_page = 6, form_now=".mp3",
                 temp_files = "test"):

        self.filename = filename
        #self.audio_train = audio_train
        
        # os.path.join(BASE_DIR, "{}".format(audio_train))
        
        self.audio_train = os.path.join(BASE_DIR, "{}".format(audio_train))


        self.output_file = output_file
        self.limit_page = limit_page
        self.form_now = form_now
        self.temp_files = temp_files


    def aud_production(self):

        '''

        synthetic speech produced here

        '''

        synth_voice = synthetic_voice(filename=self.filename, audio_train=self.audio_train,
                                      output_file=self.output_file, limit_page=self.limit_page,
                                      temp_files = self.temp_files)
        synth_voice.audio_gen()

        output_new = audio_compressor(filename = self.output_file).compression()
        print("the new output file is: ", output_new)
        extension_changer(output_new, prefered_extension=self.form_now).re_ext()
        os.rename(output_new[:-4] + self.form_now, self.filename[:-4] + self.form_now)
        return self.filename[:-4] + self.form_now



'''
the rest of it
'''


class voice_control(object):

    def __init__(self, filename, type_voice = "default", iterative_space=100, intra_space=25,
                 form_now=".mp3", rate_sp=185, vol=1.0, voice_type=0, limit=150,
                 audio_train = None, output_file = "crazyjess.wav", limit_page = 6, temp_files = "test"):

        self.filename = filename
        self.type_voice = type_voice
        self.iterative_space = iterative_space
        self.intra_space = intra_space
        self.form_now = form_now
        self.rate_sp = rate_sp
        self.vol = vol
        self.voice_type = voice_type
        self.limit = limit
        self.audio_train = audio_train
        self.output_file = output_file
        self.limit_page = limit_page
        self.temp_files = temp_files

    def conventional_menu_default(self):

        conv = conventional_voice(filename=self.filename, iterative_space=self.iterative_space,
                                  intra_space=self.intra_space, form_now=self.form_now,
                                  rate_sp=self.rate_sp, vol=self.vol, voice_type=self.voice_type,
                                  limit=self.limit)
        conv.audioproduction()

        return

    def conventional_menu_custom(self):

        file = self.filename

        def requests(file):

            form_request = "Please enter which form you would like your output file to be saved as: "
            rate_request = "Please enter at which rate you would like your file to speak: "
            vol_request = "Please enter volume (between 0 and 1): "
            voice_type_req = "Please enter volume type: 0 for male, 1 for female: "

            requests = [form_request, rate_request, vol_request, voice_type_req]

            val_requests = []
            for i in requests:
                # print(i)
                val_requests.append(input())
            val_requests[0] = str(val_requests[0])
            conv = conventional_voice(filename=file, form_now=val_requests[0],
                                      rate_sp=val_requests[1], vol=val_requests[2], voice_type=int(val_requests[3]))
            conv.audioproduction()
            return

        requests(file)
        return

    def conv_menu_custom_excp(self):

        #self.conventional_menu_custom()
        while True:
            try:
                self.conventional_menu_custom()
                break
            except:
                print("Some error has occured, please enter the values again")
        return

    def synth_voice(self):

        audio_request_message = "Please what which audio_file you would like to train to be the speech base: "
        print(audio_request_message)
        audio_request = str(input())
        #out_file = "crazyjess.wav"
        synth_voice = synthetic_voice(filename=self.filename, audio_train=audio_request,
                                      output_file=self.output_file, limit_page=self.limit_page,
                                      temp_files = self.temp_files)
        synth_voice.audio_gen()
        extension_changer(self.output_file, prefered_extension=self.form_now).re_ext()
        os.rename(self.output_file[:-4] + self.form_now, self.filename[:-4] + self.form_now)

        return

    def syn_exception(self):

        while True:
            try:
                self.synth_voice()
                break
            except:
                print("Some error has occured, please enter the values again")

        return


    def drop_menu(self):

        default_print_req = "Would you like default controls (enter default or custom): "
        print(default_print_req)
        type_synthesis = str(input())

        if type_synthesis == "default":
            print("Would you like default controls: ")
            control = input()
            if control == "Yes":
                self.conventional_menu_default()
            else:
                self.conv_menu_custom_excp()

        if type_synthesis != "default":
            self.syn_exception()

            '''
            rename outputfile
            '''

            #extension_changer(self.output_file, prefered_extension = self.form_now).re_ext()

            "rename output file, first test out menu"

        return



class adamas_pdf(object):

    def __init__(self, filename):
        self.filename = filename

    def audio_menu(self):
        voice_control(filename=self.filename).drop_menu()
        return

def main_menu():

    print("Please enter filename: ")
    filename = str(input())
    adamas_pdf(filename).audio_menu()
    return






