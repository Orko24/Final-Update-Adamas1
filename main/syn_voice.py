'''

Modified & original work Copyright (c) 2022 Hemanto Bairagi


This code is the sole property of Hemanto Bairagi. 
Any unauthorized replication and use of any code used 
in any form will be a violation of my exclusive Copyright. 

'''

from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.files.storage import FileSystemStorage

from django.http import FileResponse
from django import forms

import pandas as pd
from voice_production.sangenius_controls import *
from .tasks import *
from .redis_tracker import *
from .file_cleaners import *

import json
from django.http import FileResponse
from django.http import HttpResponse
from PyPDF2 import PdfFileWriter, PdfFileReader, PdfFileMerger

import os
from pathlib import Path
from voice_production.sangenius_complete.admin_test import *
from .multi_users import *

BASE_DIR = Path(__file__).resolve().parent.parent


# UPLOAD_FOLDER = file_upload_path
ALLOWED_EXTENSIONS_TEXT = {'pdf'}

ALLOWED_EXTENSIONS_MEDIA = {"ogg","mp3","flac"}


'''
Introduce python audio upload limit, as well pdf limits
'''


def upload_file_pdf(request):
    # form = upload()

    count_pg = 0
    request.session["count_pg"] = count_pg


    output_file_directory = os.path.join(BASE_DIR, "main\\Website\\output_files")
    # os.path.join(BASE_DIR, "main\\Website\\Compression_pdf")
    synthetic_text_directory = os.path.join(BASE_DIR, "main\\static\\Synthetic_voice\\Synthetic_text")
    synthetic_audio_directory = os.path.join(BASE_DIR, "main\\static\\Synthetic_voice\\Synthetic_audio")
    temp_file_directory = os.path.join(BASE_DIR, "main\\static\\Synthetic_voice\\synthetic_temp_files")

    directories_managed = [output_file_directory, synthetic_text_directory, synthetic_audio_directory, temp_file_directory]

    for i in directories_managed:
        initial_directory_manager(i, time_limit = 48).manage_service()


    # file_removers(output_file_directory).remove()
    # file_removers(synthetic_text_directory).remove()
    # file_removers(synthetic_audio_directory).remove()
    # file_removers(temp_file_directory).remove()

    '''

    create an upload directory subsystem using a class object

    psuedo algorithm:

    1) take the path of the folder 
    2) measure how many sub folders/ items are in the folder
    3) create a random key and put it in the at the end of user_
    4) have all processing be done under that folder
    5) create sub folder in output folder for each file generated, using the random key
    6) of the user_
    7) shutil copy output into that folder
    8) serve it up as downloads
    9) cleaning alogorithm for folders that are 2 days old

    '''

    random_user_id = id_generator()
    folder_name = "user_{}".format(random_user_id)

    request.session['folder_name'] = folder_name
    request.session['synthetic_text_directory'] = synthetic_text_directory
    request.session['synthetic_audio_directory'] = synthetic_audio_directory
    request.session['temp_file_directory'] = temp_file_directory
    request.session['outputs'] = output_file_directory

    messages.info(request, "Please upload pdf with less than 6 pages at a time as this is an experimental feature")


    if request.method == "POST":
        pass
        if 'file' not in request.FILES:
            messages.error(request, " Nothing was uploaded please upload a pdf file")
            return redirect(request.path)

        elif request.FILES['file'] == '':

            messages.error(request, " No file was uploaded please upload a pdf file")

            return redirect(request.path)
        else:

            uploaded_file = request.FILES['file']
            name = uploaded_file.name
            size = uploaded_file.size
            Allowed_formats = [".pdf"]

            if name[-4:] not in Allowed_formats:
                messages.error(request, " Please upload a pdf file")
                return redirect(request.path)



            else:

                # messages.success(request, "The file has uploaded")
                fs = FileSystemStorage()

                '''
                maybe throw a loading page in here
                '''

                # \static\Synthetic_voice\Synthetic_text

                #maybe throw in user id

                fs.save(uploaded_file.name, uploaded_file)

                # output_file_directory = os.path.join(BASE_DIR, "main\\Website\\output_files")

                primary_upload = os.path.join(BASE_DIR, "main\\static\\{}".format(uploaded_file.name))
                # move_upload = os.path.join(BASE_DIR, "main\\static\\Synthetic_voice\\Synthetic_text")

                move_upload = os.path.join(synthetic_text_directory, folder_name)
                folder_cleaner(move_upload).file_path_make()

                print(move_upload)

                shutil.copy(primary_upload, move_upload)

                try:
                    os.remove(primary_upload)

                except Exception:

                    '''
                    maybe give a unique id to uploads then rename em once moved (yea add that in)
                    '''

                    admin_commands(os.remove(primary_upload))

                file_path = os.path.join(synthetic_text_directory,folder_name + "\\{}".format(uploaded_file.name))

                ''':check pdf upload page len

                '''
                length_pdf = PdfFileReader(file_path).numPages
                length_pdf_lmt = 6
                if length_pdf > length_pdf_lmt:
                    messages.error(request,
                                   "Please keep pdf page lengths below 6 for now as this feature is still experimental")
                    return redirect(request.path)
                messages.success(request, "The file has uploaded")

                page_id = id_generator(size=24)


                return redirect('Audio/{page_id}/'.format(page_id = page_id))

    return render(request, "main/voice_synthesis_pages/voice_synthesis.html", {})


def upload_file_audio(request,page_id):
    # form = upload()

    file_lmt = 20
    file_size_lmt = file_lmt * 1024 * 1024
    messages.warning(request, "The file upload limit is {} MB".format(file_lmt))
    messages.info(request, "The current limit will be upgraded once production and user interaction data demands it")

    # request.session['folder_name'] = folder_name
    # request.session['synthetic_text_directory'] = synthetic_text_directory
    # request.session['synthetic_audio_directory'] = synthetic_audio_directory
    # request.session['temp_file_directory'] = temp_file_directory

    folder_name = request.session.get('folder_name')
    synthetic_text_directory = request.session.get('synthetic_text_directory')
    synthetic_audio_directory = request.session.get('synthetic_audio_directory')
    temp_file_directory = request.session.get('temp_file_directory')


    if request.method == "POST":
        pass
        if 'file' not in request.FILES:
            messages.error(request, " Nothing was uploaded please upload a mp3 or ogg file")
            return redirect(request.path)

        elif request.FILES['file'] == '':

            messages.error(request, " No file was uploaded please upload a mp3 or ogg")

            return redirect(request.path)
        else:

            uploaded_file = request.FILES['file']
            name = uploaded_file.name
            size = uploaded_file.size
            Allowed_formats = [".ogg",".mp3"]

            if size >= file_size_lmt:

                messages.error(request, "The file size as exceeded limits please upload a smaller file")
                return redirect(request.path)


            if name[-4:] not in Allowed_formats:
                messages.error(request, " Please upload either an ogg or mp3 file")
                return redirect(request.path)

            else:

                messages.success(request, "The file has uploaded")
                fs = FileSystemStorage()

                '''
                maybe throw a loading page in here
                '''

                # \static\Synthetic_voice\Synthetic_text
                fs.save(uploaded_file.name, uploaded_file)

                
                primary_upload = os.path.join(BASE_DIR, "main\\static\\{}".format(uploaded_file.name))

                # synthetic_audio_directory = request.session.get('synthetic_audio_directory')


                move_upload = os.path.join(synthetic_audio_directory,folder_name)
                folder_cleaner(move_upload).file_path_make()

                shutil.copy(primary_upload, move_upload)
                os.remove(primary_upload)

                enc_id = id_generator(size=24)

                '''':redirect to processing page and a loading gif

                '''

                return redirect("Synthesis/{enc_id}".format(enc_id = enc_id))

    return render(request, "main/voice_synthesis_pages/voice_synthesis_audio_upload.html", {})

def synthesis(request, page_id, enc_id):



    '''

    Try to turn this into a loading page by using HTML CSS and Javascript

    use condition to check if audio and synthetic pdf folders are empty,

    if empty render the page, else redirect to a processor to send the download file.

    Redirect to a processing page
    Access both files
    Throw them into sangenius controls for synthetic voice after analysizing pdf properties and Audiosize

    '''

    # primary_upload = os.path.join(BASE_DIR, "main\\static\\{}".format(uploaded_file.name))

    folder_name = request.session.get('folder_name')
    synthetic_text_directory = request.session.get('synthetic_text_directory')
    synthetic_audio_directory = request.session.get('synthetic_audio_directory')
    temp_file_directory = request.session.get('temp_file_directory')

    # dir_text = os.listdir(os.path.join(BASE_DIR, "main\\static\\Synthetic_voice\\Synthetic_text"))
    # dir_audio = os.listdir(os.path.join(BASE_DIR, "main\\static\\Synthetic_voice\\Synthetic_audio"))

    dir_path_text = os.path.join(synthetic_text_directory, folder_name)
    dir_path_audio = os.path.join(synthetic_audio_directory, folder_name)

    dir_text = os.listdir(dir_path_text)
    dir_audio = os.listdir(dir_path_audio)

    empty_check = len(dir_text) == 0 and len(dir_audio) == 0

    if not empty_check == True:
        messages.success(request,"Processing beginning")

        file_text = dir_text[0]
        file_audio = dir_audio[0]
        # text_path = "main\\static\\Synthetic_voice\\Synthetic_text" + "\\{}".format(file_text)
        # audio_path = "main\\static\\Synthetic_voice\\Synthetic_audio" + "\\{}".format(file_audio)

        text_path = os.path.join(dir_path_text,"{}".format(file_text))
        audio_path = os.path.join(dir_path_audio, "{}".format(file_audio))

        # print('The Text path is: ', text_path)
        # print('The Audio path is: ', audio_path)

        print('File Text: ', file_text)
        print('File Audio: ', file_audio)

        if audio_path != audio_path.strip():


            original_name = os.path.join(BASE_DIR, "{}".format(audio_path))
            new_name = os.path.join(BASE_DIR, "{}".format(audio_path.strip()))

            os.rename(original_name, new_name)
            audio_path = audio_path.strip()

        print(audio_path)
        print(text_path)
        request.session['audio_path'] = audio_path
        request.session['text_path'] = text_path
        texts = text_path

        ''''
        temp bs
        '''

        # os.path.join(BASE_DIR, "main\\static\\Synthetic_voice\\synthetic_temp_files\\tests")
        '''
        Change Temp path
        '''

        user_temp_file = os.path.join(temp_file_directory, folder_name)

        folder_cleaner(user_temp_file).file_path_make()
        temp_path = os.path.join(user_temp_file, "tests")

        print(temp_path)

        # folder_cleaner(temp_file_directory).file_path_make()

        # temp_path = os.path.join(BASE_DIR, "main\\static\\Synthetic_voice\\synthetic_temp_files\\tests")

        asynchronous_result = synthetic_voice.delay(file_path=texts, audio_path=audio_path, temp_path = temp_path)
        messages.success(request, "File processing has begun, you will be notified once it is finished")
        reddis_vals = reddis_information(asynchronous_result)
        jobid = reddis_vals.job_id_()
        result_vals = reddis_vals.values_()
        request.session["task_id"] = jobid

        # cntx['task_id'] = jobid


        return redirect("Processing/")

    return render(request, "main/voice_synthesis_pages/experimental_loading_page.html", {})

def synthetic_processor(request, page_id, enc_id):

    cntx = {}
    jobid = request.session.get("task_id")
    cntx['task_id'] = jobid
    count = 0
    request.session['count'] = count

    return render(request, "main/Synthetic_integrations.html", cntx)


'''
could pass to another view page and have that page do the rendering as when view is run page is reloaded 
and asychronous task starts again; if so must replicated across... *shudders* all views

'''

def synthetic_processing_unit(request):

    count = request.session.get('count')
    task_id = request.GET.get('taskid', None)

    if task_id is not None and count == 0:

        request.session['count'] = request.session['count'] + 1
        print("count: ", request.session['count'])
        local_task_id = task_id

        try:
            job_id, status, result = redis_id_info_(id=local_task_id).vals()
            results_completion = results_tracker(result)
            # count = count + 1
            process_checker = process_completion(results_completion = results_completion, task_id = local_task_id)
            job_id, status, result = process_checker.results()

        except Exception:
            pass

        file_out_put = result
        request.session['results'] = file_out_put

        print(result)
        print(file_out_put)

        print("the result is: ", result)
        print("the file output is: ", file_out_put)

        redirect_url = "Downloads/"
        context = {'state': status, 'result': result, 'state_binary': results_tracker(result),
                   'redir': redirect_url,
                   }

        data = json.dumps(context)
        print("context: ", context)
        print("data: ", data)
        #
        request.session['result'] = result
        # messages.success(request, "File processing is complete your download will be initiating")
        return HttpResponse(data, content_type="application/json")




def synthetic_downloads(request, page_id, enc_id):


 
    try:

        output_file = os.path.join(BASE_DIR, request.session.get('results'))
        # output_file = request.session.get('results')
        audio_path = request.session.get("audio_path")
        texts = request.session.get("text_path")

        out_put_folder = os.path.join(request.session.get('outputs'), request.session.get('folder_name'))

        folder_cleaner(out_put_folder).file_path_make()

        # os.path.join(BASE_DIR, "main\\Website\\output_files")
        # out_put_folder = os.path.join(BASE_DIR, "main\\Website\\output_files")


        out_file_name = os.path.basename(os.path.normpath(output_file))

        # out_file_name = output_file.split("\\")[-1]

        '''
        may need to clean output folder of any trace files
        '''

        print("The output folder is: ", out_put_folder)
        print("The output file name: ", output_file)


        shutil.copy(src=output_file, dst=out_put_folder)

        

        os.remove(os.path.join(BASE_DIR, output_file))
        os.remove(os.path.join(BASE_DIR, texts))
        os.remove(os.path.join(BASE_DIR, audio_path))
        # os.remove(texts)
        # os.remove(audio_path)

        output_audio_path = os.path.join(out_put_folder, "{}".format(out_file_name))
        # output_audio_path = out_put_folder + "\\{}".format(out_file_name)
        
        print(output_file)
        print(output_file)
        response = FileResponse(open(output_audio_path, 'rb'), as_attachment=True)
        # messages.success(request, "File processing is complete your download will be initiating")

        return response

 
    except Exception:

        
        messages.success(request, "Your file should have already downloaded, if not please try processing again")
        return render(request, "main/voice_synthesis_pages/synthetic_downloads.html", {})



