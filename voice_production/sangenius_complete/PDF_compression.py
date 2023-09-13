'''

Modified & original work Copyright (c) 2022 Hemanto Bairagi


This code is the sole property of Hemanto Bairagi. 
Any unauthorized replication and use of any code used 
in any form will be a violation of my exclusive Copyright. 

'''

import cv2
import pytesseract
import os
import os.path
from pdf2image import convert_from_path
import subprocess
import os.path
import sys
import shutil
from PyPDF2 import PdfFileWriter, PdfFileReader, PdfFileMerger
import ctypes
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

    gs = os.path.join(BASE_DIR, "sangenius_complete\\gs\\gs10.00.0\\bin\\gswin64c.exe")
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
        pytesseract.pytesseract.tesseract_cmd = os.path.join(os.getcwd() , "Tesseract-OCR\\tesseract.exe")
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
        self.folder_name = file_name[:-4] + " folder"

    def folder_name_c(self):
        return self.folder_name


class copy_files_specific_folder(object):

    def __init__(self, file_name, destination_folder=None):
        self.file_name = file_name
        self.destination_folder = destination_folder

    def directory(self):
        directory = r'{}'.format(os.getcwd())

        '''may want to modify directory so that you can get a specific folder'''

        return directory

    def source(self):
        directory = self.directory()
        srs = str(directory + "\{}".format(self.file_name))
        return srs

    def destination(self):
        directory = self.directory()
        f_n = folder_name(self.file_name).folder_name_c()
        des = str(directory + "\{}".format(f_n))
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
        shutil.copy(srs, des)
        return ('Copied')


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
        return "file copied"

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
            image_name = 'page' + str(i) + '.jpg'
            image_names.append(image_name)
            images[i].save(image_name, 'JPEG')
            des = copy_files_specific_folder(self.file_name).destination()
            srs = copy_files_specific_folder(image_name).source()

            copy_files_specific_folder(image_name, des).copy()
            # os.remove(image_name)

        for i in image_names:
            os.remove(i)

        return image_names


class Compressed_pdf(object):

    def __init__(self, file_name):
        self.file_name = file_name
        # self.compressed_file  = file_name[:-4] + "_compressed.pdf"
        '''
        
        maybe modify the function so it works in certain directories
        
        '''
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

    '''
    
    add a save directory
    
    
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
            sub_file = self.filename[:-4] + "sub_{}".format(i) + self.filename[-4:]
            # print(sub_file)

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



class pdf_merge_compression(object):

    def __init__(self, filename, iterative_space):

        self.filename = filename
        self.iterative_space = iterative_space

    def PDF_split(self):

        split_software = PDF_splitter(filename = self.filename, iterative_space = self.iterative_space)
        sub_file_list = split_software.pdf_split()
        return sub_file_list

    def compress_sub_files(self):

        split_list = self.PDF_split()
        sub_compression_lst = []

        for i in split_list:

            pdf_compression_software = Compressed_pdf(file_name = i)
            comp_sub = pdf_compression_software.compressed_file
            sub_compression_lst.append(comp_sub)
            '''
            compression list
            '''
            pdf_compression_software.compr()

        for j in split_list:
            os.remove(j)

        merger = PdfFileMerger()

        for file in sub_compression_lst:
            merger.append(file)

        end_file = self.filename[:-4] + "_c.pdf"
        merger.write(end_file)
        merger.close()

        for file in sub_compression_lst:
            os.remove(file)

        return end_file

'''
Folder creator
'''

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






def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

class admin_commands(object):

    def __init__(self, command):

        self.command = command

    def run_command(self):
        if is_admin():
            os.system(self.command)

        else:
            # Re-run the program with admin rights
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        return



class multiple_pdfs(object):

    def __init__(self,new_files, iterative_space=250):

        self.new_files = new_files
        self.iterative_space=iterative_space

        ''''
        list of files to be compressed
        '''


    def compression(self):

        compressed_files = []
        for file_path in self.new_files:
            compression_software = pdf_merge_compression(filename=file_path, iterative_space=self.iterative_space)
            end_compressed_file = compression_software.compress_sub_files()

            print(end_compressed_file)

            compressed_files.append(end_compressed_file)
            os.remove(file_path)

        return compressed_files


class admin_pdf_compression_multi(object):

    def __init__(self,new_files, iterative_space=250):

        self.new_files = new_files
        self.iterative_space = iterative_space

    def multi_compression(self):

        compression_software = multiple_pdfs(new_files = self.new_files, iterative_space= self.iterative_space)
        compressed_files = compression_software.compression()
        return compressed_files

    def compressed_names(self):

        file_lst = self.new_files
        compressed_files = []

        for file in file_lst:

            compressed_file_name = Compressed_pdf(file).compressed_file
            compressed_files.append(compressed_file_name)

        return compressed_files

    def admin_pdf(self):

        try: 
            self.multi_compression()

        except Exception:

            admin_commands(self.multi_compression()).run_command()
        return self.compressed_names()


