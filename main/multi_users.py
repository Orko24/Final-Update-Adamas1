import os
from pathlib import Path
from .redis_tracker import *
import json
from .file_cleaners import *

# from .multi_users import *

import os
from pathlib import Path
import time
import datetime

import random
import string
import time
from datetime import date




class path_fixer(object):

    def __init__(self, folder_path):

        self.folder_path = folder_path

    def check_path(self):

        folder_existence = os.path.exists(self.folder_path)

        return folder_existence

    def existence_fix(self):

        check_path = self.check_path()

        if not check_path:
            folder_creation_destruction(self.folder_path).folder_creation()
            return self.folder_path
        else:
            return self.folder_path


class folder_cleaner(object):

    def __init__(self, folder_path):
        self.folder_path = folder_path

    def file_path_make(self):
        file_path = path_fixer(self.folder_path).existence_fix()

        return file_path

    def folder_clean(self):

        # file_path = path_fixer(self.folder_path).existence_fix()
        file_path = self.file_path_make()


        if file_path:
            file_removers(file_path).remove()

        return file_path


''':cvar
File sub-management system
'''


def id_generator(size=12, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

# class temp_user(object):
#
#     def __init__(self,user_name):
#
#         self.user_name = user_name

class folder_time_creation(object):

    def __init__(self, directory_path):

        self.directory_path = directory_path

    def time_path_creation(self):

        return os.path.getmtime(self.directory_path)



# def

class datetime_conversion(object):

    def __init__(self,datetime_object):

        self.datetime_object = datetime_object

    def c_times(self):

        return time.ctime(self.datetime_object)

    def strip_times(self):

        c_times = self.c_times()
        file_date = datetime.datetime.strptime(c_times, "%a %b %d %H:%M:%S %Y")
        return file_date


class directory_times(object):

    def __init__(self, directory):

        self.directory = directory

    def list_directory(self):

        return os.listdir(self.directory)

    def creation_times(self):

        list_directory = self.list_directory()
        time_creations = {}

        for i in list_directory:

            # print(os.path.join(self.directory, i))

            path_i = os.path.join(self.directory, i)

            times = folder_time_creation(path_i).time_path_creation()
            # ts = time.time()

            file_creation_time = datetime_conversion(times).strip_times()


            # print(path_i , times)

            time_creations[path_i] = file_creation_time

        # print(time_creations)

        return time_creations

    def time_diff_current(self):
        ts = time.time()
        current_time = datetime_conversion(ts).strip_times()
        creation_times = self.creation_times()

        keys = list(creation_times.keys())

        time_diffs = {}

        for i in keys:

            vals = creation_times[i]

            print("vals: ", vals)

            time_diff = current_time - vals
            hours = time_diff.total_seconds() / (60 * 60)

            print("hours: ", hours)

            time_diffs[i] = hours
            print(time_diffs)

            # time_diffs[i] = hours


        # print('time diff: ',time_diff)
        return time_diffs

class cleaner_schedule(object):

    def __init__(self, directory, time_limit = 48):

        self.directory = directory
        self.time_limit = time_limit

    def time_diffs(self):

        if len(os.listdir(self.directory)) > 0:

            creation_hours = directory_times(self.directory).time_diff_current()

            for i in list(creation_hours.keys()):
                vals = creation_hours[i]

                if vals > self.time_limit:

                    print('The folder {} is destroyed'.format(vals))

                    folder_creation_destruction(i).folder_destruction()


            return self.directory

        else:

            return self.directory



class initial_directory_manager(object):

    def __init__(self, directory, time_limit = 48):

        self.directory = directory
        self.time_limit = time_limit

    def manage_service(self):

        folder_cleaner(self.directory).file_path_make()
        cleaner_schedule(self.directory, time_limit=self.time_limit).time_diffs()

        file_lmt = 250 * 1024
        file_size_lmt = file_lmt * 1024 * 1024

        size_GBs = os.path.getsize(self.directory)

        if size_GBs > file_lmt:

            if len(os.listdir(self.directory)) != 0:
                for folders in os.listdir(self.directory):
                    os.remove(os.path.join(self.directory,folders))

            else:
                file_removers(self.directory).remove()
                folder_cleaner(self.directory).file_path_make()



        return self.directory




