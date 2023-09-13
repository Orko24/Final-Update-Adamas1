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
    else:
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
    return


class sql_data_gen(object):

    def __init__(self, database_name, data, data_name="placeholder"):
        self.database_name = database_name
        self.data = data
        self.data_name = data_name
        self.data_str_gen = client_data_structure(data_1=self.data, var_name=self.data_name)

    def data_str(self):
        # data_str_gen = client_data_structure(data_1=self.data, var_name=self.data_name)
        # data_str = data_str_gen.client_vals()

        data_str = self.data_str_gen.client_vals()
        return data_str

    def sql_cmd(self):
        #         data_str_gen = client_data_structure(data_1 = self.data, var_name = self.data_name)
        #         data_str = data_str_gen.client_vals()

        data_str = self.data_str()
        # sql_selection_cmd = data_str.sql_cmd()

        sql_selection_cmd = self.data_str_gen.sql_cmd()

        return sql_selection_cmd

    def sql_gen(self):
        data_str = self.data_str()
        conn = connect(self.database_name)
        data_str.to_sql(self.data_name, conn)
        conn.close()
        return conn



class database_reader(object):

    # def __init__(self, conn, sql_selection_cmd, data_name="placeholder"):
    def __init__(self, database_name, sql_selection_cmd, data_name="placeholder"):

        #self.conn = conn
        self.database_name = database_name
        self.sql_selection_cmd = sql_selection_cmd
        self.data_name = data_name

    def read_(self):
        conn = connect(self.database_name)
        sql_data = pd.read_sql(self.sql_selection_cmd, conn)
        conn.close()
        single_instance_data = dict(zip(list(sql_data), sql_data.to_numpy()[0]))
        return single_instance_data

#
# DB_NAME_conv = "database_localization\\test_database_2.db"
# name = "test_data_1"
# titles = np.array(["","form", "vol_type","speech_rate", "vol__rate"])
# values = np.array(["client information","mp3",0,185,0.5])
# data_1 = np.array([titles, values])
#
# sql_data_ = sql_data_gen(database_name = DB_NAME_conv, data = data_1, data_name=name)
# sql_cmd = sql_data_.sql_cmd()
# cnn = sql_data_.sql_gen()
#
# # read_data = database_reader(data_s = data_s, conn = cnn, sql_selection_cmd = sql_cmd, data_name="placeholder")
# print(sql_cmd)
# read_data = database_reader(database_name = DB_NAME_conv, sql_selection_cmd = sql_cmd, data_name=name)
# sen = read_data.read_()
# os.remove(DB_NAME_conv)
# print(sen)




