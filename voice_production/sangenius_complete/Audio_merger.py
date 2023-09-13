import os.path
import soundfile as sf
import ctypes, sys


import os.path
import numpy as np
import os
import wave
from moviepy.editor import concatenate_audioclips, AudioFileClip
'''
Code in extention changer
'''
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent



class extension_changer(object):

    def __init__(self, filename, prefered_extension = ".mp3"):

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
        self.change_ext()
        new_name = self.new_name()
        audio_comp = audio_compression(new_name)
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

        print(self.filename)
        print(self.filename[:-4] + self.form_current)

        os.remove(self.filename[:-4] + self.form_current)


        return

    def compression(self):
        self.flac_g.flac_file()
        self.remove_old_file()
        # extension_changer(self.out_file, ".mp3").re_ext()
        extension_changer(self.out_file, self.filename[-4:]).re_ext()
        return self.filename


'''

code for smaller files

'''

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
        s3_wav_data = np.concatenate(s_wav_data)
        return s3_wav_data, frame_rates

    def export_merge(self):
        s3_wav_data, frame_rates = self.merge()
        s3 = self.output_file
        x = int(sum(frame_rates) / len(frame_rates))
        sf.write(s3, s3_wav_data, x)
        return


'''

just use the larger file merger for both medium and large


'''


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
        # self.end_file = "\\{}".format(end_file + self.form)
        self.end_file = "\\{}".format(end_file + self.form)
        self.videos = " + ".join(str(i) for i in self.audio_lst)

        #problematic code potentially 

        # self.path_new_vid = "{}".format(os.getcwd() + self.end_file)

        # os.path.join(BASE_DIR, self.end_file)

        # self.path_new_vid = "{}".format(os.path.join(BASE_DIR, self.end_file))

        self.path_new_vid = os.path.join(BASE_DIR, self.end_file)

        print(self.path_new_vid)


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

    def __init__(self, audio_lst, end_file="test", form=".mp3"):
        self.audio_lst = audio_lst
        self.end_file = end_file
        self.form = form
        self.cmd_gen = cmd_merger_large_data(audio_lst, end_file=self.end_file, form=self.form)

    def cmd_generator(self):
        cmds = self.cmd_gen.batch_cmds_os()
        return cmds

    def batch(self):
        cmds = self.cmd_generator()
        batch_ = batch_gen_python(commands=cmds).batch()
        return batch_

    def run(self):
        batch_file = self.batch()
        os.system(batch_file)
        os.remove(batch_file)
        return


class admin_batch(object):

    def __init__(self, audio_lst, end_file="test", form=".mp3"):
        self.audio_lst = audio_lst
        self.end_file = end_file
        self.form = form
        self.batch_run = batch_run(audio_lst=self.audio_lst, end_file=self.end_file, form=self.form)

    def admin_run(self):

        try:
            self.batch_run.run()

        except Exception:

            batch_ = self.batch_run.batch()
            admin_commands(batch_).run_command()
            os.remove(batch_)

        return



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
        clips = [AudioFileClip(c) for c in audio_clip_paths]
        final_clip = concatenate_audioclips(clips)
        final_clip.write_audiofile(output_path)



