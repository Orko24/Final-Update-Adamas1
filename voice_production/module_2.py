'''

Modified & original work Copyright (c) 2022 Hemanto Bairagi


This code is the sole property of Hemanto Bairagi. 
Any unauthorized replication and use of any code used 
in any form will be a violation of my exclusive Copyright. 

'''

from voice_production.voice_sythesis_interface import *
from voice_production.sangenius_complete.Sangenius_test import *
from voice_production.sangenius_complete.Text_audio_fix import *
import soundfile as sf
import numpy as np
import os
import wave


class wave_merge(object):

    def __init__(self, audio_merger_lst, output_file="crazyjess.wav"):
        self.audio_merger_lst = audio_merger_lst
        self.output_file = output_file

    def wave_data(self):
        s_data = []
        _data = []
        frame_rates = []

        audio_lst = self.audio_merger_lst

        for i in audio_lst:
            s_wav_data, _ = sf.read(i, dtype='float32')
            s_data.append(s_wav_data)
            _data.append(_)

            with wave.open(i, "rb") as wave_file:
                frame_rate = wave_file.getframerate()
                frame_rates.append(frame_rate)

        return s_data, _data, frame_rates

    def merge(self):
        s_wav_data, _data, frame_rates = self.wave_data()

        if len(s_wav_data) != 0:

            s3_wav_data = np.concatenate(s_wav_data)
            return s3_wav_data, frame_rates

        else:

            return s_wav_data, frame_rates

    def export_merge(self):
        s3_wav_data, frame_rates = self.merge()
        s3 = self.output_file

        if len(frame_rates) != 0 :

            x = int(sum(frame_rates) / len(frame_rates))
            sf.write(s3, s3_wav_data, x)
            return s3
        else:
            # x = int(sum(frame_rates) / len(frame_rates))
            print(frame_rates)
            sf.write(s3, s3_wav_data, 16000)
            return s3




class synthetic_text(object):

    def __init__(self, text, char_lmt=10):
        self.text = text
        self.char_lmt = char_lmt

    def sentence_processing(self):
        word_lst = self.text.split(" ")
        sentence_lst = []
        count = 0
        count_lmt = self.char_lmt
        words = []
        for i in word_lst:
            words.append(i)
            count = count + 1
            if count == count_lmt:
                sentence_lst.append(words)
                words = []
                count = 0
        #sentence_lst
        refined_sen = []
        for sen in sentence_lst:
            sentence_ = ""
            for i in sen:
                sentence_ = sentence_ + i + " "
            refined_sen.append(sentence_)
        return refined_sen


class syn_speech_txt(object):

    def __init__(self, filename, char_lmt = 10):

        self.filename = filename
        self.char_lmt = char_lmt

    def text(self):

        '''
        compression actually happens within the text

        '''
        print(self.filename)

        text = book_audio(self.filename).text()

        print(text)

        '''
        compression within synthetic speech
        '''

        compressed_pdf = audio_book_producer(self.filename).compressed_file_name
        folder_n = folder_name(compressed_pdf).folder_name_c()

        print("This is the compressed pdf", compressed_pdf)

        print("Compressed folder name", folder_n)

        '''
        maybe issues here
        no shutil to move it here, idk what im trying to accomplish here, maybe remove text, worked in flask
        '''

        folder_creation_destruction(folder_n).folder_destruction()
        os.remove(compressed_pdf)

        print(compressed_pdf)



        return text

    def syn_feed(self):

        text = self.text()
        syn_text = synthetic_text(text=text, char_lmt=self.char_lmt)
        refined_sen = syn_text.sentence_processing()
        return refined_sen


class synthetic_audio_gen(object):

    def __init__(self, filename, audio_train, output_file = "crazyjess.wav", temp_files = "test"):

        self.filename = filename
        self.audio_train = audio_train
        self.output_file = output_file
        self.temp_files = temp_files
        self.temp_ext = ".wav"

    def synthetic_text(self):

        syn_text = syn_speech_txt(self.filename).syn_feed()

        print('current file name',self.filename)

        return syn_text

    def synthetic_waves(self):

        syn_text = self.synthetic_text()
        audio_lst = []

        for i in range(len(syn_text)):



            audio_name = "{}{}{}".format(self.temp_files,i, self.temp_ext)
            texts = syn_text[i]
            synth = voice_synthesis(audio_file_path=self.audio_train, filename=audio_name, input_text=texts)
            synth.voice_synthetic_text()
            audio_lst.append(audio_name)

        return audio_lst

    def wave_merge(self):

        audio_lst = self.synthetic_waves()
        wave_merge(audio_merger_lst=audio_lst, output_file=self.output_file).export_merge()

        for i in audio_lst:
            os.remove(i)

        return


    def exec_gen(self):

        #execute_admin(self.synth_gen_clean())
        execute_admin(self.wave_merge())

        return





