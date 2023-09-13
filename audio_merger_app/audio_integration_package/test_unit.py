from vertical_integration_API import *

def list_printer(lst):

    for x in lst:
        print("\n")
        print(x)

    return




# directory_path = "C:\\Users\\Owner\\Desktop\\adamas_local_copy\\adamas_cloud\\mid_file_processing_test"

# files = file_generator(directory_path).file_list_addresses()

# solutions = solution_commands(files, directory=directory_path, output_file= "output_1.mp3")

# files_string = solutions.file_string()
# golang_cmd = solutions.golang_cmd()
# cpp_cmd = solutions.cpp_cmd()

# list_printer(files)
# print('\n')
# print(files_string)
# print('\n')
# print(golang_cmd)
# print("\n")
# print(cpp_cmd)
# print("\n")


# see if the solution is scalable

directory_path = "C:\\Users\\Owner\\Desktop\\adamas_local_copy\\adamas_cloud\\mid_file_processing_test"

files = file_generator(directory_path).file_list_addresses()

output_file_golang = "output_golang.mp3"
output_file_cpp = "output_cpp.mp3"

sol_golang_cmd = solution_commands(file_list=files, directory=directory_path, output_file=output_file_golang)

sol_cpp_cmd = solution_commands(file_list=files, directory=directory_path, output_file=output_file_cpp)

sol_golang_cmd.golang_sol()
sol_cpp_cmd.cpp_sol()




