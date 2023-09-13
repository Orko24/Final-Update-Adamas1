'''

Modified & original work Copyright (c) 2022 Hemanto Bairagi


This code is the sole property of Hemanto Bairagi. 
Any unauthorized replication and use of any code used 
in any form will be a violation of my exclusive Copyright. 

'''

import os
from voice_production.sangenius_complete.admin_test import *
from voice_production.sangenius_complete.Text_audio_fix import *
from pathlib import Path
import zipfile


class file_removers(object):

    def __init__(self, directory):
        self.directory = directory

    def remove(self):

        basedir = os.path.abspath(os.path.dirname(__file__))

        '''
        make this linux compatible
        '''

        total_files =  os.listdir(self.directory)

        print(len(total_files))
        total_file_paths = []

        excess_folders = []

        if len(total_files) != 0:

            for f in total_files:
                if not os.path.isfile(os.path.join(self.directory, f)):
                    excess_folders.append(f)

            print(excess_folders)
            if len(excess_folders) != 0:
                for i in excess_folders:
                    # print(self.directory + "\\{}".format(i))
                    folder_creation_destruction(os.path.join(self.directory, "{}".format(i))).folder_destruction()



            total_files = os.listdir(self.directory)
            for i in total_files:
                full_paths = os.path.join(basedir, "{}\\{}".format(self.directory, i))
                total_file_paths.append(full_paths)

            # print(total_file_paths)
            
            for file_re in total_file_paths:

                try:
                    os.remove(file_re)

                except Exception:
                    time.sleep(2)
                    try:
                        if file_re[-4:] == ".zip":
                            zipped_file = file_re
                            with open(zipped_file, mode="r") as file:
                                zip_file = zipfile.ZipFile(file)
                                for member in zip_file.namelist():
                                    filename = os.path.basename(member)
                                    if not filename:
                                        continue
                                    source = zip_file.open(member)
                            os.remove(zipped_file)
                        else:
                            pass
                    except Exception:
                        pass

            return True
        else:
            return False



