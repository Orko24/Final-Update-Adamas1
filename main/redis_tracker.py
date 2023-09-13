'''

Modified & original work Copyright (c) 2022 Hemanto Bairagi


This code is the sole property of Hemanto Bairagi. 
Any unauthorized replication and use of any code used 
in any form will be a violation of my exclusive Copyright. 

'''

from rq.job import Job
from redis import Redis
import json
from socket import *
import socket
import time
import struct
# import redis


import os
import signal
from subprocess import Popen, PIPE
from psutil import process_iter
# from signal import SIGKILL

class reddis_information(object):

    def __init__(self, asyncronous_job):

        self.asyncronous_job = asyncronous_job
        self.redis = Redis()

    def job_id_(self):

        # print(self.asyncronous_job)

        job_id = self.asyncronous_job.id

        # print(job_id)

        return job_id

    def values_(self):

        job_id = self.job_id_()

        '''
        job_id, task id in celery
        '''
        # self.redis
        # print(job_id)
        job = Job.fetch(job_id, connection=Redis())
        job.refresh()
        status = job.get_status(refresh=True)
        #
        # if status == "finished":
        #     print(status)



        '''
        job.get_status(refresh=True) Possible values are queued, started, deferred, finished, stopped, scheduled,
        canceled and failed. If refresh is True fresh values are fetched from Redis.
        '''



        result = job.result

        '''
        job.result stores the return value of the job being executed, will return None prior to job execution.
        Results are kept according to the result_ttl parameter (500 seconds by default).

        '''

        return job_id, status,result

class redis_id_info_(object):

    def __init__(self, id):
        self.id = id
        # self.redis = Redis(host="localhost",port=6379)

    def vals(self):

        job_id = self.id
        job = Job.fetch(job_id, connection=Redis('localhost', 6379))
        job.refresh()
        status = job.get_status(refresh=True)

        # if status == "finished":
        #     print(status)

        '''
        job.get_status(refresh=True) Possible values are queued, started, deferred, finished, stopped, scheduled,
        canceled and failed. If refresh is True fresh values are fetched from Redis.
        '''

        result = job.result

        '''
        job.result stores the return value of the job being executed, will return None prior to job execution.
        Results are kept according to the result_ttl parameter (500 seconds by default).

        '''

        return job_id, status, result


def state(status):
    if status == "finished":
        return True
    return False

def results_tracker(results):

    if results != None:
        return True
    return False



class process_completion(object):

    def __init__(self, results_completion, task_id, sleep_time = 2):
        self.results_completion = results_completion
        self.task_id = task_id
        self.sleep_time = sleep_time

    def results(self):
        results_completion = self.results_completion
        task_id = self.task_id


        while not results_completion:



            # print("checking")

            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            socket_status = sock.connect_ex(('localhost', 6379))
            # print("socket_connected: ", socket_status)
            linger_enabled = 1
            linger_time = socket.SO_LINGER  # This is in seconds.
            linger_struct = struct.pack('ii', linger_enabled, linger_time)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_LINGER, linger_struct)
            sock.shutdown(SHUT_RDWR)
            sock.close()
            # print("socket closed")
            # print("socket val: ", socket_status)
            while socket_status != 0:
                # sock.close()

                # print("socket closed status activated: ", socket_status)

                '''
                should get no errors but continous while loop

                '''
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                sock.bind(('localhost', 6379))
                job_id, status, result = redis_id_info_(id=task_id).vals()

                if result != None:
                    socket_status = 0
                # job_id, status, result = task_id, "pending", None

            if socket_status == 0:

                # print("socket activated: ", socket_status)
                job_id, status, result = redis_id_info_(id=task_id).vals()
                # print(job_id, status, result)

                if result == None:

                    # print(socket_status)
                    time.sleep(self.sleep_time)


            # task_completion = state(status)
            results_completion = results_tracker(result)
            # print("current status: ", status)
            # print("current result: ", result)
            # print("current task completion state: ", results_completion)

        return job_id, status, result