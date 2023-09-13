# from pywinauto.application import Application
import ctypes, sys
import os

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


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



class cmd_merger_large_data(object):

    def __init__(self, audio_lst, end_file="test", form=".mp3"):
        self.audio_lst = audio_lst
        self.form = form

        '''
        issue might be here
        '''
        self.end_file = "\\{}".format(end_file + self.form)


        self.videos = " + ".join(str(i) for i in self.audio_lst)

        self.end_file_lst = self.end_file.split("\\")

        if len(self.end_file) > 1:

            # self.path_new_vid = "{}".format(self.end_file)
            self.path_new_vid = "{}".format(end_file + self.form)

        else:

            

            end_file = os.path.join(BASE_DIR, self.end_file)
            

            self.path_new_vid = "{}".format(end_file)


        self.commands = "copy /b {} {}".format(self.videos, self.path_new_vid)
        self.audio_merger_command = 'cmd /k {}'.format(self.commands)
        # self.audio_merger_command = 'cmd /c {}'.format(self.commands)

    def audio_merger_cmd(self):
        audio_cmd = self.audio_merger_command
        return audio_cmd

    def base_command(self):
        return self.commands

    def batch_cmd_pywinauto(self):
        base_command = self.base_command()
        cmd_start = "start cmd.exe\r"
        batch_cmd = cmd_start + base_command

        return batch_cmd

    def batch_cmds_os(self):
        batch_lines = ['start cmd.exe \n', self.commands + " \n", "exit"]
        # batch_lines = ['start cmd.exe \n', self.commands + " \n"]
        return batch_lines


class batch_gen_python(object):

    def __init__(self, commands, filename="imp.txt"):
        self.commands = commands
        self.filename = filename

    def textfile_maker(self):
        file1 = open(self.filename, "w")
        L = self.commands
        file1.writelines(L)
        file1.close()
        return self.filename

    def batch(self):
        self.textfile_maker()
        rename = self.filename
        pre, ext = os.path.splitext(rename)
        os.rename(rename, pre + '.bat')
        return pre + '.bat'

class batch_run(object):
    
    def __init__(self,audio_lst, end_file="test", form=".mp3"):

        self.audio_lst = audio_lst
        self.end_file = end_file
        self.form = form
        self.cmd_gen = cmd_merger_large_data(audio_lst, end_file=self.end_file, form= self.form)

    def cmd_generator(self):

        print(self.end_file)

        cmds = self.cmd_gen.batch_cmds_os()
        return cmds

    def batch(self):

        cmds = self.cmd_generator()
        batch_ = batch_gen_python(commands = cmds).batch()
        return batch_

    def run(self):

        batch_file = self.batch()
        os.system(batch_file)
        os.remove(batch_file)
        return


class admin_batch(object):

    def __init__(self,audio_lst, end_file="test", form=".mp3"):
        self.audio_lst = audio_lst
        self.end_file = end_file
        '''
        hard code test
        '''

        # 'main\\static\\convbook\\temp'
        self.form = form
        self.batch_run = batch_run(audio_lst = self.audio_lst, end_file= self.end_file, form= self.form)

        # self.batch_run = batch_run(audio_lst=self.audio_lst, end_file='main\\static\\convbook\\temp', form=self.form)

    def admin_run(self):

        try:
            self.batch_run.run()

        except Exception:

            print(self.end_file)

            batch_ = self.batch_run.batch()
            admin_commands(batch_).run_command()
            os.remove(batch_)

        return



    