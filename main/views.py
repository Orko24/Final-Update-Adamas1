'''

Modified & original work Copyright (c) 2022 Hemanto Bairagi


This code is the sole property of Hemanto Bairagi. 
Any unauthorized replication and use of any code used 
in any form will be a violation of my exclusive Copyright. 

'''


# from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from .tasks import *
from celery.result import AsyncResult

from main.service import Regression
from rq.job import Job
from redis import Redis
import json
from django_rq import job




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

        job = Job.fetch(job_id, connection=self.redis)
        job.refresh()
        status = job.get_status(refresh=True)

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
        self.redis = Redis()

    def vals(self):

        job_id = self.id

        job = Job.fetch(job_id, connection=self.redis)
        job.refresh()
        status = job.get_status(refresh=True)

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


'''
views prototype

'''

def home(request):

    # messages.success(request, "Message sent.")
    # messages.error(request, "Error. Message not sent.")

    if request.method == 'POST':


        if "submit" in request.POST:
            messages.success(request, "Message sent.")
            messages.error(request, "Error. Message not sent.")

            messages.warning(request, "Warning message sent.")
            messages.info(request, "Info Message sent.")

            messages.success(request, "Message sent.")
            messages.error(request, "Error. Message not sent.")

            messages.warning(request, "Warning message sent.")
            messages.info(request, "Info Message sent.")

            return redirect('Regression/')


    return render(request, "main/home.html", {})






def Reg_page(request):

    cntx = {}
    asynchronous_result = test_calc3.delay(True)
    reddis_vals = reddis_information(asynchronous_result)

    jobid = reddis_vals.job_id_()
    result_vals = reddis_vals.values_()
    request.session['task_id'] = jobid

    cntx['task_id'] = jobid

    print(cntx)

    """
    run asychronous task may as well, might be able to pass task id into regression_results.html
    """
    request.session['selected_project_id'] = jobid

    # return redirect("Processing/")

    # ajax_integration_page = "main/dq_integration.html"
    ajax_integration_page = "main/audiomerger_integrations.html"
    # ajax_integration_page = "main/conventional_integrations.html"
    # ajax_integration_page = "main/pdf_integration.html"
    # ajax_integration_page = "main/Synthetic_integrations.html"



    # return render(request, "main/dq_integration.html", cntx)
    return render(request, ajax_integration_page, cntx)

    # return render(request, "main/regression_results.html")

def state(status):

    if status == "finished":
        return True
    return False

def Dq_processor(request):

    print("testing")
    # task_id = request.GET.get('task_id', None)
    task_id = request.GET.get('taskid', None)
    print(task_id)


    if task_id is not None:

        job_id, status, result = redis_id_info_(id = task_id).vals()


        context = {'state': status, 'result': result, 'state_binary': state(status)}


        task_completion = state(status)

        while not task_completion:

            print("checking")

            job_id, status, result = redis_id_info_(id=task_id).vals()


            print(job_id, status, result)
            print(state(status))
            task_completion = state(status)

        redirect_url = "Landing/"
        context = {'state': status, 'result': result, 'state_binary': state(status),
                   'redir': redirect_url,
                   }

        data = json.dumps(context)
        print("context: ", context)
        print("data: ", data)
    #
        return HttpResponse(data, content_type="application/json")

    else:
        return HttpResponse('No job id given.')



def Regression_processor(request):

    start_time = time.time()
    R = Regression()
    rmse = R.get_rmse()
    context = {"rmse": rmse,
               "time": time.time() - start_time}

    '''

    data dumped by \loading\ url

    '''


    reg_id = request.session.get("task_id")
    print('Loading page task id is :', reg_id)

    print(redis_id_info_(reg_id).vals())

    print(context)


    # page_text_synth = "main/Loading_pages/Synth_loader.html"
    # page_text_synth = "main/Loading_pages/convo_loader_1.html"
    # page_text_synth = "main/Loading_pages/audio_merge_loader.html"

    # page_text_synth = "main/Loading_pages/pdf_cub_loader.html"
    #
    # return render(request, page_text_synth, {})


    data = json.dumps(context)
    return HttpResponse(data, content_type="application/json")


def Finish(request):

    task_id = request.session.get('selected_project_id')

    print(task_id)

    job_id, status, result = redis_id_info_(id=task_id).vals()

    print(job_id, status, result)

    return render(request, "main/Regression_processor.html", {})
