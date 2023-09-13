import subprocess
import os

class command_line_runner(object):

    def __init__(self, cmd):
        self.cmd = cmd

    def run(self):

        process = subprocess.Popen(self.cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)

        for line in process.stdout:
            print(line)

        return
    
# Python executivable class build just in case
class MP3_merge_software_activation(object):

    def __init__(self):

        self.MP3CAT_command = "go install github.com/dmulholl/mp3cat@latest"
        self.MP3WRAP_command = "mp3wrap.exe"

    def golang_solution_install(self):

        command_line_runner(self.MP3CAT_command).run()
        return
    
    def Cpp_sol_install(self):

        command_line_runner(self.MP3WRAP_command).run()
        return


# cmd_golang = "mp3cat merged_audio_1.mp3 merged_audio_2.mp3 merged_audio_3.mp3 -o joined_3.mp3"
# cmd_cpp = "mp3wrap joined_2.mp3 merged_audio_1.mp3 merged_audio_2.mp3 merged_audio_3.mp3"

# command_line_runner(cmd = cmd_golang).run()
# command_line_runner(cmd = cmd_cpp).run()

# class file_address_generator(object):

#     def __init__(self, file):
#         self.file = file

class file_generator(object):

    def __init__(self,directory):

        self.directory = directory

    def files(self):

        file_list = os.listdir(self.directory)
        return file_list
    
    def file_list_addresses(self):

        file_list = self.files()

        full_directory = list(map(lambda x: os.path.join(self.directory, x), file_list))

        return full_directory
    

class solution_commands(object):

    def __init__(self, file_list, directory = "", output_file = "output.mp3"):

        self.file_list = file_list
        self.output_file = os.path.join(directory,output_file)
        

    def file_string(self):

        # self.full_directory = self.file_list_addresses()

        file_string = " ".join(self.file_list)

        return file_string
    
    '''
    Golang solution
    '''

    def golang_cmd(self):

        # golang_cmd = "mp3cat " + self.file_string() + " -o {}".format(self.output_file)

        golang_cmd = "mp3cat {} -o {}".format(self.file_string(), self.output_file)
        return golang_cmd

    def golang_sol(self):

        golang_cmd = self.golang_cmd()

        command_line_program = command_line_runner(golang_cmd)
        command_line_program.run()
        
        return self.output_file



    def cpp_cmd(self):

        # cmd_cpp = "mp3wrap joined_2.mp3 merged_audio_1.mp3 merged_audio_2.mp3 merged_audio_3.mp3"

        cpp_cmd = "mp3wrap {} {}".format(self.output_file, self.file_string())
        return cpp_cmd
    
    def cpp_sol(self):

        cpp_cmd = self.cpp_cmd()

        command_line_program = command_line_runner(cpp_cmd)
        command_line_program.run()
        
        return self.output_file

    
    




        

    


