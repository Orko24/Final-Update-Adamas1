'''

Modified & original work Copyright (c) 2022 Hemanto Bairagi


This code is the sole property of Hemanto Bairagi. 
Any unauthorized replication and use of any code used 
in any form will be a violation of my exclusive Copyright. 

'''

from voice_production.sangenius_complete.admin_test import *
#from ghost_compression import *
from voice_production.sangenius_complete.Text_audio_fix import *


class file_modifier(object):

    def __init__(self, file, form=".mp3", modified_file = "temp.pdf"):
        self.file = file
        #self.modified_file = self.file.replace(" ", "")
        '''
        change temp.pdf to get location data from directory after finishing up the flask framework
        '''

        self.modified_file = modified_file

        self.form = form
        self.audio_file = self.file[:-4] + self.form

    def _mod_file(self):
        return self.modified_file

    def _rename(self):

        print("uploaded file name", self.file)
        print("modified file name", self.modified_file)

        os.rename(self.file, self.modified_file)

        print("File renamed apparently")

        return


class audio_rename(object):

    def __init__(self, compr_audio_file, file, modified_file = "temp.pdf"):
        self.compr_audio_file = compr_audio_file
        self.file = file
        self.form = self.compr_audio_file[-4:]
        self.modified_file = modified_file



        self.file_mod = file_modifier(file=self.file, form=self.form, modified_file = self.modified_file)
        # self.modified_file = self.file_mod.modified_file
        self.audio_file = self.file_mod.audio_file

    def rename_aud_comp(self):

        print("compressed_audio_file in the rename audio_comp: ", self.compr_audio_file)
        print("new filename in the rename audio_comp: ", self.audio_file)

        os.rename(self.compr_audio_file, self.audio_file)
        return


class large_file_merger(object):

    def __init__(self, filename, iterative_space=350, intra_space=35,
                 form_now=".mp3", rate_sp=185, vol=1.0, voice_type=0, end_file = None):

        self.filename = filename
        self.iterative_space = iterative_space
        self.intra_space = intra_space
        self.form_now = form_now
        self.rate_sp = rate_sp
        self.vol = vol
        self.voice_type = voice_type
        if end_file == None:
            self.end_file = self.filename[:-4]
        else:
            self.end_file = end_file

    def _clean_audio(self):

        PDF_s = PDF_splitter(filename=self.filename, iterative_space=self.iterative_space)
        pdf_files = PDF_s.pdf_split()
        output_files = []

        for i in pdf_files:
            sangenius_data_speech(i, interative_space=self.intra_space,
                                  form_now=self.form_now,rate_sp=self.rate_sp,
                                  vol=self.vol, voice_type=self.voice_type).audio_book_clean()

        for i in pdf_files:
            output_file = i[:-4] + self.form_now
            output_files.append(output_file)

        return output_files

    def extra_files(self):

        PDF_s = PDF_splitter(filename=self.filename, iterative_space=self.iterative_space)
        #pdf_files = PDF_s.pdf_split()

        pdf_files = PDF_s.sub_file_lst()

        output_files = []

        for i in pdf_files:
            output_file = i[:-4] + self.form_now
            output_files.append(output_file)

        return output_files,pdf_files

    def merge_batch(self):

        print("End_file name: ", self.end_file)

        aud_names = self._clean_audio()
        batch_process = admin_batch(audio_lst=aud_names, end_file=self.end_file, form=self.form_now)
        batch_process.admin_run()
        return


    def clean_merge(self):

        self.merge_batch()
        output_files, pdf_files = self.extra_files()

        for i in output_files:
            os.remove(i)

        for j in pdf_files:
            os.remove(j)

        return print("Requested task has been completed")


class sangenius_audio_book(object):

    '''
    Additional point, fix the filename bs so spaces are taken out and then renamed, use conditions;
    if no spaces and so on so forth
    '''

    def __init__(self, filename, iterative_space=100, intra_space=25,
                 form_now=".mp3", rate_sp=185, vol=1.0, voice_type=0, limit= 150, end_file = None):

        self.filename = filename
        self.length_pdf = PdfFileReader(self.filename).numPages
        self.iterative_space = iterative_space
        self.intra_space = intra_space
        self.form_now = form_now
        self.rate_sp = rate_sp
        self.vol = vol
        self.voice_type = voice_type

        if end_file == None:
            self.end_file = self.filename[:-4]
        else:
            self.end_file = end_file

        self.limit = limit

    def large_file(self):

        merger = large_file_merger(filename=self.filename, iterative_space=self.iterative_space,
                                   intra_space=self.intra_space, form_now=self.form_now, rate_sp=self.rate_sp,
                                   vol=self.vol, voice_type=self.voice_type, end_file= self.end_file)
        merger.clean_merge()
        return

    def small_file(self):

        sangenius_data_speech(filename=self.filename, interative_space=self.intra_space,
                              form_now=self.form_now, rate_sp=self.rate_sp,
                              vol=self.vol, voice_type=self.voice_type).audio_book_clean()

        return


    def audio(self):


        if self.length_pdf >= self.limit:
            self.large_file()
        if self.length_pdf <= self.limit:
            self.small_file()

        return "Requested task has been completed"


def execute_admin(command):
    if is_admin():

        command
        # for file_name in pdf_lst:
        #     sangenius_audio_book(file_name, iterative_space=100, intra_space=25).audio()

    else:
        # Re-run the program with admin rights
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)

    return




class sangenius_audio(object):

    def __init__(self, filename, iterative_space=100, intra_space=25,
                 form_now=".mp3", rate_sp=185, vol=1.0, voice_type=0, limit=150, modified_file = "temp.pdf",
                 end_file = None):

        self.filename = filename
        self.length_pdf = PdfFileReader(self.filename).numPages
        self.iterative_space = iterative_space
        self.intra_space = intra_space
        self.form_now = form_now
        self.rate_sp = rate_sp
        self.vol = vol
        self.voice_type = voice_type

        if end_file == None:
            self.end_file = self.filename[:-4]
        else:
            self.end_file = end_file

        self.limit = limit
        self.modified_file = modified_file

    def audio(self):
        form_control = self.form_now

        file_mod = file_modifier(file=self.filename, form=form_control, modified_file = self.modified_file)
        '''
        here it is
        '''
        file_mod._rename()
        file = file_mod._mod_file()

        print('SPACE ')
        print('SPACE ')
        print('SPACE ')
        print('SPACE ')
        print('SPACE ')

        print("temp file name is: ", file)
        print("End file is: ", self.end_file)

        print('SPACE ')
        print('SPACE ')
        print('SPACE ')
        print('SPACE ')
        print('SPACE ')

        sang_audio = sangenius_audio_book(file, iterative_space=self.iterative_space, intra_space=self.intra_space,
                                          form_now=form_control, rate_sp=self.rate_sp, vol=self.vol,
                                          voice_type=self.voice_type, limit=self.limit)

        print("filename_self:", self.filename[:-4])

        compr_audio = sang_audio.end_file + form_control

        print("sang_audio.end_file: ", sang_audio.end_file)
        print('Compressed audio file: ', compr_audio)
        print('Modified file: ', self.modified_file)

        sang_audio.audio()
        audio_rename(compr_audio_file=compr_audio, file=self.filename,
                     modified_file = self.modified_file).rename_aud_comp()

        # rename file back to default
        os.rename(file, self.filename)

    def admin_audio(self):
        execute_admin(self.audio())
        return





