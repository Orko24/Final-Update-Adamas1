'''
Modified & original work Copyright (c) 2022 Hemanto Bairagi


This code is the sole property of Hemanto Bairagi. 
Any unauthorized replication and use of any code used 
in any form will be a violation of my exclusive Copyright.
'''


from sqlite3 import connect
import pandas as pd
import numpy as np
import ctypes, sys
import os
# from . import database_generation


class sql_access_cmd(object):

    def __init__(self, dataframe, name):
        self.dataframe = dataframe
        self.name = name

    def sql_cmd(self):
        df = self.dataframe
        col_insertion = "{}".format(', '.join([list(df.columns)[i] for i \
                                               in range(len(list(df.columns)))]))
        sql_read_cmd = 'SELECT {} FROM {}'.format(col_insertion, self.name)

        return sql_read_cmd


class client_data_structure(object):

    def __init__(self, data_1, var_name="test_data"):
        self.data_1 = data_1
        self.var_name = var_name

    def client_vals(self):
        client_vals = pd.DataFrame(data=self.data_1[1:, 1:], \
                                   index=self.data_1[1:, 0], columns=self.data_1[0, 1:])
        return client_vals

    def sql_cmd(self):
        client_val = self.client_vals()
        sql_cmd_prime = sql_access_cmd(dataframe=client_val, name=self.var_name)

        return sql_cmd_prime.sql_cmd()

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def execute_admin(command):
    if is_admin():

        command
        # for file_name in pdf_lst:
        #     sangenius_audio_book(file_name, iterative_space=100, intra_space=25).audio()

    else:
        # Re-run the program with admin rights
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)

    return
'''
Flask integration
'''

#
# DB_NAME_conv = "test_database_2.db"
# name = "test_data_5"
# titles = np.array(["","form", "vol_type","speech_rate", "vol__rate"])
# values = np.array(["client information","mp3",0,185,0.5])
# data_1 = np.array([titles, values])
# #
# data_str_gen = client_data_structure(data_1 = data_1, var_name = name)
# data_str = data_str_gen.client_vals()
#
#
# sql_selection_cmd = data_str_gen.sql_cmd()
# conn = connect(DB_NAME_conv)
#
#
# data_str.to_sql(name, conn)
#
#
# sql_data = pd.read_sql(sql_selection_cmd, conn)
# conn.close()
# os.remove(DB_NAME_conv)
#
# single_instance_data = dict(zip(list(sql_data), sql_data.to_numpy()[0]))
#
# # print(data_str)
# # print(sql_data)
# # print(list(sql_data))
# # print(type(sql_data))
# # print(sql_data.to_numpy()[0])
# # print(dict(zip(list(sql_data), sql_data.to_numpy()[0])))
#
# print(single_instance_data)
#
#
# # execute_admin(os.remove(DB_NAME_conv))
# #os.remove(DB_NAME_conv)
#
# # execute_admin(os.remove("test_database.db"))