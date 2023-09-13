'''

Modified & original work Copyright (c) 2022 Hemanto Bairagi


This code is the sole property of Hemanto Bairagi. 
Any unauthorized replication and use of any code used 
in any form will be a violation of my exclusive Copyright. 

'''

from PDFNetPython3.PDFNetPython import PDFDoc, Optimizer, SDFDoc, PDFNet
import cv2
import pytesseract
import os
import os.path
import shutil
from pdf2image import convert_from_path
import soundfile as sf

import PyPDF2
from gtts import gTTS
from PyPDF2 import PdfFileWriter, PdfFileReader
import pyttsx3
from moviepy.editor import concatenate_audioclips, AudioFileClip

import subprocess
import os.path
import sys
import shutil
import time
from voice_production.sangenius_complete.admin_test import *
from voice_production.sangenius_complete.Audio_merger import *
from audio_merger_app import *

from pathlib import Path

import os

BASE_DIR = Path(__file__).resolve().parent.parent


def get_ghostscript_path():
    gs_names = ['gs', 'gswin32', 'gswin64']
    for name in gs_names:
        if shutil.which(name):
            return shutil.which(name)
    raise FileNotFoundError(f'No GhostScript executable was found on path ({"/".join(gs_names)})')


def compress(input_file_path, output_file_path, power=0):
    """Function to compress PDF via Ghostscript command line interface"""
    quality = {
        0: '/default',
        1: '/prepress',
        2: '/printer',
        3: '/ebook',
        4: '/screen'
    }

    # Basic controls
    # Check if valid path
    if not os.path.isfile(input_file_path):
        print("Error: invalid path for input PDF file")
        sys.exit(1)

    # Check if file is a PDF by extension
    if input_file_path.split('.')[-1].lower() != 'pdf':
        print("Error: input file is not a PDF")
        sys.exit(1)

    # gs = get_ghostscript_path()

    gs = os.path.join(BASE_DIR, "sangenius_complete\\gs\\gs10.00.0\\bin\\gswin64c.exe")

    # gs = 'C:\\Program Files\\gs\\gs10.00.0\\bin\\gswin64c.exe'

    print(gs)

    # gs = os.path.join(BASE_DIR, "sangenius_complete/gs.exe")



    print("Compress PDF...")
    initial_size = os.path.getsize(input_file_path)
    subprocess.call([gs, '-sDEVICE=pdfwrite', '-dCompatibilityLevel=1.4',
                    '-dPDFSETTINGS={}'.format(quality[power]),
                    '-dNOPAUSE', '-dQUIET', '-dBATCH',
                    '-sOutputFile={}'.format(output_file_path),
                     input_file_path]
    )
    final_size = os.path.getsize(output_file_path)
    ratio = 1 - (final_size / initial_size)
    print("Compression by {0:.0%}.".format(ratio))
    print("Final file size is {0:.1f}MB".format(final_size / 1000000))
    print("Done.")




class image_reader(object):

    def __init__(self, image):
        self.image = image

    def text(self):

        # pytesseract.pytesseract.tesseract_cmd = r"Tesseract-OCR\tesseract.exe"

        pytesseract.pytesseract.tesseract_cmd = os.getcwd() + "\\Tesseract-OCR\\tesseract.exe"

        #pytesseract.pytesseract.tesseract_cmd = r"C:\Users\Owner\Desktop\acr_libaries\Tesseract-OCR\tesseract.exe"

        img = cv2.imread(self.image)
        text = pytesseract.image_to_string(img)
        return text


class folder_creation_destruction(object):

    def __init__(self, path):
        self.path = path

    def folder_creation(self):
        if not os.path.exists(self.path):
            os.makedirs(self.path)
        return

    def folder_destruction(self):
        try:
            shutil.rmtree(self.path)
            print("Deleted '%s' directory successfully" % self.path)
        except:
            print("The system cannot find the file specified")
        return


class folder_name(object):

    def __init__(self, file_name):
        self.file_name = file_name
        self.folder_name = file_name[:-4] + "_folder"

    def folder_name_c(self):
        return self.folder_name


class copy_files_specific_folder(object):

    def __init__(self, file_name, destination_folder=None):
        self.file_name = file_name
        self.destination_folder = destination_folder

    def directory(self):
        directory = r'{}'.format(os.getcwd())

        print('directory activated')

        # print(directory)

        '''may want to modify directory so that you can get a specific folder'''

        return directory

    def source(self):
        directory = self.directory()

        file_lst = self.file_name.split('\\')

        print('the file list is: ', file_lst)

        if len(file_lst) > 1:

            print("The thing activated")

            srs = self.file_name

            # srs = str(directory + "\\{}".format(self.file_name))

        else:
            srs = str(directory + "\\{}".format(self.file_name))

        # srs = str(directory + "\\{}".format(self.file_name))

        print('The source is: ', srs)

        # print(srs)

        return srs

    def destination(self):
        directory = self.directory()


        f_n = folder_name(self.file_name).folder_name_c()

        '''
        code dependency might be annoying may have to rewrite where the compression folders are going 
        '''

        file_lst = f_n.split('\\')
        print('testing', f_n)

        if len(file_lst) > 1:
            print("The thing activated")
            des = f_n

        else:
            des = str(directory + "\{}".format(f_n))
        print('The destination is: ', des)
        return des

    def copy(self):
        if self.destination_folder == None:
            destination = self.destination()
        else:
            destination = self.destination_folder

        '''
        could use shutil to copy stuff
        '''

        srs = self.source()
        des = destination

        print("copy issues starting")

        shutil.copy(srs, des)
        print('Copied')
        return 


class PDF2image(object):

    def __init__(self, file_name):
        self.file_name = file_name

    def fold_n(self):
        fold_n = folder_name(self.file_name).folder_name_c()
        return fold_n

    def folder_maker(self):
        fold_n = self.fold_n()
        folder_maker = folder_creation_destruction(fold_n)
        return folder_maker

    def folder(self):
        folder_maker = self.folder_maker()
        folder = folder_maker.folder_creation()
        return folder

    def copy_func(self):
        self.folder()
        copy_func = copy_files_specific_folder(self.file_name)
        copy_func.copy()
        return print("file copied")

    def destination(self):
        des = copy_files_specific_folder().destination()
        return des

    def source(self):
        srs = copy_files_specific_folder.source()
        return srs

    def PDFimage_compression(self):
        images = convert_from_path(self.file_name)
        image_names = []
        self.copy_func()

        for i in range(len(images)):


            '''
            Crucial piece of local code that makes it all work
            '''

            '''
            gotta modify crucial piece to create a localized folder and do all work within said folder 
            '''
            print('SPACE ')
            print('SPACE ')
            print('SPACE ')
            print('SPACE ')
            print('SPACE ')

            print("Directory name with file name: ", self.file_name)

            # Path(self.file_name).parents[0]
            print("Directory name with file name: ", Path(self.file_name).parents[0])

            print('SPACE ')
            print('SPACE ')
            print('SPACE ')
            print('SPACE ')
            print('SPACE ')

            # directory = r'{}'.format(os.getcwd() + "\\main\\static\\convbook\\")

            directory = r'{}'.format(Path(self.file_name).parents[0])

            # image_name = 'page' + str(i) + '.jpg'

            # os.path.join(directory, 'page' + str(i) + '.jpg')

            # image_name = directory + 'page' + str(i) + '.jpg'

            image_name = os.path.join(directory, 'page' + str(i) + '.jpg')
            print(image_name)

            image_names.append(image_name)



            images[i].save(image_name, 'JPEG')
            des = copy_files_specific_folder(self.file_name).destination()
            srs = copy_files_specific_folder(image_name).source()

            copy_files_specific_folder(image_name, des).copy()
            #os.remove(image_name)

        '''
        admin tool it
        '''
        def removal(image_names):

            for i in image_names:
                try:
                    os.remove(i)
                except:
                    # pass
                    admin_commands(os.remove(i)).run_command()

            return

        removal(image_names)

        return image_names


class Compressed_pdf(object):

    def __init__(self, file_name):

        self.file_name = file_name
        self.compressed_file = file_name[:-4] + "_c.pdf"
        self.folder_name = folder_name(self.compressed_file).folder_name_c()

    def compr(self):

        '''
        compression files
        '''
        compr_file = compress(self.file_name, self.compressed_file, power=4)
        return compr_file

    def PDF_image(self):
        self.compr()
        PDF2image(self.compressed_file).PDFimage_compression()
        return

    def compressed_fold_name(self):
        return self.folder_name



class image_reader(object):

    def __init__(self, image):
        self.image = image

    def text(self):
        pytesseract.pytesseract.tesseract_cmd = r"Tesseract-OCR\tesseract.exe"
        img = cv2.imread(self.image)
        text = pytesseract.image_to_string(img)
        return text


class info_organizer(object):

    def __init__(self, image_dic, new_image_lst):

        self.image_dic = image_dic
        self.new_image_lst = new_image_lst

    def page_to_val(self):

        new_image_lst = self.new_image_lst
        image_dic = self.image_dic
        new_lst = []
        page_to_val = {}

        for variable in range(len(self.new_image_lst)):
            a = len(self.new_image_lst[variable])
            dic_key = list(self.image_dic.keys())[variable]
            val = self.image_dic[dic_key]
            pg_num = dic_key[-a:][4:(a - 4)]
            page_to_val[pg_num] = val
        return page_to_val

    def str_int(self):

        page_to_val = self.page_to_val()
        str_int = {}
        for string in list(page_to_val.keys()):
            str_int[int(string)] = string
        return str_int

    def val_image(self):
        str_int = self.str_int()
        val_image = {}
        page_to_val = self.page_to_val()

        for i in list(sorted(list(str_int.keys()))):
            string_key = str_int[i]
            page_to_val[string_key]
            val_image[i] = page_to_val[string_key]

        return val_image


class directory_extraction(object):

    def __init__(self, folder_name):
        self.folder_name = folder_name
        self.file_lst = os.listdir(folder_name)

    def directory_info(self):

        new_image_lst = []
        directory_images = []
        for i in self.file_lst:
            if i[-4:] == ".jpg":
                direct = "{}\\".format(self.folder_name) + i
                new_image_lst.append(i)
                directory_images.append(direct)

        return new_image_lst, directory_images

    def new_image_lst(self):

        directory_info = self.directory_info()
        return directory_info[0]

    def directory_images(self):

        directory_info = self.directory_info()
        return directory_info[1]


class page_text(object):

    def __init__(self, file_name):
        self.file_name = file_name
        self.compression_test = Compressed_pdf(file_name)

        '''
        compression begins here
        '''


        self.PDF_image = self.compression_test.PDF_image()


        self.folder_name = self.compression_test.compressed_fold_name()
        self.direct_stuff = directory_extraction(self.folder_name)
        self.new_image_lst = self.direct_stuff.new_image_lst()
        self.directory_images = self.direct_stuff.directory_images()

    def val_text(self):
        image_dic = {}
        for direct in self.directory_images:
            image_text = image_reader(direct).text()
            image_dic[direct] = image_text

        return image_dic

    def text(self):
        image_dic = self.val_text()
        new_image_lst = self.new_image_lst
        page_vals = info_organizer(image_dic, new_image_lst).val_image()
        return page_vals


class book_str(object):

    def __init__(self, file_name):
        self.file_name = file_name

    def text(self):
        page_vals = page_text(self.file_name).text()
        x = list(page_vals.values())
        y = ' '.join(map(str, x))
        return y


class text_audio(object):

    def __init__(self, full_text, audio_name, lang="en", speed=False):
        self.full_text = full_text
        self.audio_name = audio_name
        self.lang = lang
        self.speed = speed

    def audio_file(self):
        myobj = gTTS(text=self.full_text, lang=self.lang, slow=self.speed)
        myobj.save(self.audio_name)
        return myobj


class pytext(object):

    def __init__(self, text, audio_name="test.mp4", rate_sp=185, vol=1.0, voice_type=0):
        self.text = text
        self.audio_name = audio_name

        self.rate_sp = rate_sp
        self.vol = vol
        self.voice_type = voice_type
        self.engine = pyttsx3.init()

        self.engine.setProperty('rate', self.rate_sp)
        self.engine.setProperty('volume', self.vol)
        voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', voices[self.voice_type].id)

    def rate(self):
        rate = self.engine.getProperty('rate')
        return rate

    def volume(self):
        volume = self.engine.getProperty('volume')
        return volume

    def voices(self):
        voices = self.engine.getProperty('voices')
        return voices

    def eng_properties(self):
        self.engine.say('My current speaking rate is ' + str(self.rate_sp) + 'volume is ' + \
                        str(self.vol) + "voice is " \
                        + str(self.voice_type))
        self.engine.runAndWait()
        return

    def text_speech(self):
        self.engine.say(self.text)
        self.engine.runAndWait()
        return

    def audio_file(self):
        self.engine.save_to_file(self.text, self.audio_name)
        self.engine.runAndWait()
        return print("Completed as requested")


class book_audio(object):

    def __init__(self, file_name, form = ".mp3", rate_sp=185, vol=1.0, voice_type=0):

        ''':cvar

        pass in pytext variables

        '''

        self.file_name = file_name
        self.form = form
        self.rate_sp = rate_sp
        self.vol = vol
        self.voice_type = voice_type
        self.au_n = self.file_name[:-4] + self.form

    def text(self):

        # print(self.file_name)
        text = book_str(self.file_name).text()
        return text

    def audio(self):
        text = self.text()

        if len(text) != 0:

            pytext(text, audio_name=self.au_n, rate_sp=self.rate_sp, vol=self.vol, voice_type=self.voice_type).audio_file()
        
        else:
            text = "There has been some error caused by the user, perhaps a blank page or non english documents \
                were uploaded, either please try again and troubleshoot \
                    it on your end, thank you for your patience"

            pytext(text, audio_name=self.au_n, rate_sp=self.rate_sp, vol=self.vol, voice_type=self.voice_type).audio_file()
        
        
        return "Completed"


class extension_changer(object):

    def __init__(self, filename, prefered_extension):

        self.filename = filename
        self.prefered_extension = prefered_extension
        self.oldbase = os.path.splitext(self.filename)

    def newname(self):
        newname = self.filename.replace(self.oldbase[1], self.prefered_extension)
        return newname

    def re_ext(self):
        output = os.rename(self.filename, self.newname())
        return output


class audio_compression(object):

    def __init__(self, new_name):
        self.new_name = new_name

    def flac_converter(self):
        data, samplerate = sf.read(self.new_name)
        sf.write(self.new_name[:-4] + ".flac", data, samplerate)
        return self.new_name[:-4] + ".flac"


class flac_generator(object):

    def __init__(self, filename, form=".wav"):
        self.filename = filename
        self.form = form

    def renamer(self):

        chang_soft = extension_changer(self.filename, self.form)
        return chang_soft

    def new_name(self):
        new_name = self.renamer().newname()
        return new_name

    def change_ext(self):
        change_ext = self.renamer().re_ext()
        return change_ext

    def audio_compressor(self):


        ''''

        if not wave file use the code below:

        if self.filename[-4:] == ".wav" then audio compress with the old name

        '''

        if self.filename[-4:] != ".wav":
            self.change_ext()
            new_name = self.new_name()
            audio_comp = audio_compression(new_name)


        if self.filename[-4:] == ".wav":
            audio_comp = audio_compression(self.filename)


        return audio_comp

    def flac_file(self):
        audio_comp = self.audio_compressor()
        flac_file = audio_comp.flac_converter()
        return flac_file


class audio_compressor(object):

    def __init__(self, filename):
        self.filename = filename
        self.form = self.filename[-4:]
        self.flac_g = flac_generator(self.filename)
        self.out_form = ".flac"
        self.out_file = self.filename[:-4] + self.out_form
        self.form_current = self.flac_g.form

    def flac_file(self):
        return self.flac_g.flac_file()

    def remove_old_file(self):

        time.sleep(2)

        os.remove(self.filename[:-4] + self.form_current)
        return

    def compression(self):
        self.flac_g.flac_file()
        self.remove_old_file()
        # extension_changer(self.out_file, ".mp3").re_ext()
        extension_changer(self.out_file, self.filename[-4:]).re_ext()
        return self.filename

'''

maybe use flac files to convert wav file to flac file then to mp3

'''


class audio_book_producer(object):

    def __init__(self, file_name, form_now=".mp3", rate_sp=185, vol=1.0, voice_type=0):
        self.file_name = file_name
        self.form_now = form_now

        self.rate_sp = rate_sp
        self.vol = vol
        self.voice_type = voice_type

        self.audio_name = self.file_name[:-4] + self.form_now
        self.book_audio = book_audio(self.file_name, form=self.form_now, \
                                     rate_sp = self.rate_sp, vol = self.vol, voice_type = self.voice_type)

        '''
        file compression
        '''

        self.compressed_file_name = Compressed_pdf(self.file_name).compressed_file
        self.compressed_folder_name = Compressed_pdf(self.file_name).folder_name

    def audio(self):
        book_audio = self.book_audio
        return book_audio.audio()

    def audio_compress(self):
        audio = self.audio()
        audio_compressor(self.audio_name).compression()
        return self.audio_name

    def audio_book(self):
        self.audio_compress()
        folder_creation_destruction(self.compressed_folder_name).folder_destruction()
        os.remove(self.compressed_file_name)

        text_msg = self.file_name + " has been converted to an audiobook with a {}".format(self.form_now + "extension")

        return text_msg

'''
PDF management system

'''


class pdf_maker(object):

    def __init__(self, file_name, outfile_name, p_start=0, p_end=10):
        self.file_name = file_name
        self.outfile_name = outfile_name
        self.p_start = p_start
        self.p_end = p_end
        self.input_pdf = PdfFileReader(self.file_name)
        self.output = PdfFileWriter()

    def add_pages(self):
        for i in range(self.p_start, self.p_end):
            self.output.addPage(self.input_pdf.getPage(i))
        return self.output

    def pdf_output(self):
        self.add_pages()

        with open(self.outfile_name, "wb") as output_stream:
            self.output.write(output_stream)
        return


class PDF_splitter(object):

    def __init__(self, filename, iterative_space):

        self.filename = filename
        self.length_pdf = PdfFileReader(self.filename).numPages
        self.iterative_space = iterative_space

        self.sub_pdf_list = list(range(self.length_pdf))[::self.iterative_space] + [self.length_pdf]
        self.length = len(list(enumerate(self.sub_pdf_list)))

    def slice_ranges(self):

        y = []
        for i in range(self.length - 1):
            x = list(enumerate(self.sub_pdf_list))
            y.append((x[i][1], x[i + 1][1]))

        pdf_num_lst = {}
        for a, b in list(enumerate(y)):
            pdf_num_lst[a] = b

        sub_filelst = {}
        file_space_lst = {}
        for i in list(pdf_num_lst.keys()):

            '''
            maybe use a directory system
            '''

            sub_file = self.filename[:-4] + "sub_{}".format(i) + self.filename[-4:]
            #print(sub_file)

            sub_filelst[i] = sub_file

        for i in list(pdf_num_lst.keys()):
            file_space_lst[sub_filelst[i]] = pdf_num_lst[i]

        return file_space_lst

    def slice_creator(self):

        file_space_lst = self.slice_ranges()
        for i in list(file_space_lst.keys()):
            sub_file = i
            a, b = file_space_lst[i]
            pdf_maker(self.filename, outfile_name=sub_file, p_start=a, p_end=b).pdf_output()
        return

    def sub_file_lst(self):

        file_space_lst = self.slice_ranges()
        return list(file_space_lst.keys())

    def pdf_split(self):

        self.slice_creator()
        return self.sub_file_lst()




#audio_combo

'''

Audio combiner is the problematic piece of code

Might be able to use pydub audio to fix this up

'''

class audio_combiner(object):

    def __init__(self, audio_clip_paths, output_path):
        self.audio_clip_paths = audio_clip_paths
        self.output_path = output_path

    def concatenate_audio_moviepy(self):
        audio_clip_paths = self.audio_clip_paths
        output_path = self.output_path

        """Concatenates several audio files into one audio file using MoviePy
        and save it to `output_path`. 
        Note that extension (mp3, etc.) must be added to `output_path`"""

        '''Try to merge the clips instead'''


        clips = [AudioFileClip(c) for c in audio_clip_paths]
        # extend out the logic

        final_clip = concatenate_audioclips(clips)
        final_clip.write_audiofile(output_path)

        '''
        testing piece code
        
        '''

        print(audio_merger)

        # print(output_path)
        #
        # admin_batch(audio_clip_paths, end_file=output_path).admin_run()


class audio_producer(object):

    def __init__(self, file_name, interative_space=45, form_now=".mp3", rate_sp=185, vol=1.0, voice_type=0):

        self.file_name = file_name
        self.interative_space = interative_space
        self.form_now = form_now
        self.rate_sp = rate_sp
        self.vol = vol
        self.voice_type = voice_type

        self.PDF_split = PDF_splitter(self.file_name, self.interative_space)
        self.sublst = self.PDF_split.sub_file_lst()
        self.slices = self.PDF_split.slice_creator()

        print('The sublst: ', self.sublst)
        print('The sub slices: ', self.slices)

    def audio_book_production(self):

        for i in range(len(self.sublst)):
            audio_book_producer(self.sublst[i], form_now=self.form_now, \
                                rate_sp=self.rate_sp, \
                                vol=self.vol, voice_type=self.voice_type).audio_book()
        return

    def audio_names(self):
        self.audio_book_production()
        form_lst = []
        for i in range(len(self.sublst)):
            x = audio_book_producer(self.sublst[i], form_now=self.form_now, \
                                    rate_sp=self.rate_sp, \
                                    vol=self.vol, voice_type=self.voice_type).form_now
            form_lst.append(x)
        forms = list(enumerate(form_lst))
        sublsts = list(enumerate(self.sublst))
        audio_names = []

        if len(sublsts) == len(forms):
            for i in range(len(sublsts)):
                if forms[i][0] == sublsts[i][0]:
                    extension = forms[i][1]
                    sub_name = sublsts[i][1]
                    audio_file_name = sub_name[:-4] + extension
                    audio_names.append(audio_file_name)
        return audio_names


class sangenius_data_speech(object):

    def __init__(self, filename, interative_space=45, form_now=".mp3", rate_sp=185, vol=1.0, voice_type=0):

        self.filename = filename
        self.interative_space = interative_space
        self.form_now = form_now
        self.rate_sp = rate_sp
        self.vol = vol
        self.voice_type = voice_type
        self.output_file = self.filename[:-4] + self.form_now
        self.audio_c = audio_producer(self.filename, interative_space=self.interative_space,
                                      form_now=self.form_now, rate_sp=self.rate_sp, vol=self.vol,
                                      voice_type=self.voice_type)

    def subfile_lst(self):

        sublst = self.audio_c.sublst
        return sublst

    def aud_names(self):

        a_names = self.audio_c.audio_names()
        return a_names


    '''
    These sections use audio_combiner to concacnate files
    
    '''

    def audio_combinator(self):

        # sublst = self.subfile_lst()
        a_names = self.aud_names()
        audio_comb = audio_combiner(a_names, self.output_file)
        audio_comb.concatenate_audio_moviepy()
        return a_names

    def trash_removal(self):

        sublst = self.subfile_lst()
        # a_names = self.aud_names()
        a_names = self.audio_combinator()

        for i in sublst:
            os.remove(i)
        for j in a_names:
            os.remove(j)

        return

    def audio_book_clean(self):

        # self.audio_combinator()
        self.trash_removal()
        return





