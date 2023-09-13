'''

Modified & original work Copyright (c) 2022 Hemanto Bairagi


This code is the sole property of Hemanto Bairagi. 
Any unauthorized replication and use of any code used 
in any form will be a violation of my exclusive Copyright. 

'''

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.files.storage import FileSystemStorage

from django.http import FileResponse
from django.http import HttpResponse
from .tasks import *

from .redis_tracker import *
import json
from .file_cleaners import *

from .multi_users import *

import os
from pathlib import Path
import random
import string

# USER_NUMBER = 0

BASE_DIR = Path(__file__).resolve().parent.parent


# def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
#     return ''.join(random.choice(chars) for _ in range(size))




def Conventinal_audio(request):

    # return render(request, "main/Conventional_Audiobook.html", {})

    '''
    delete any files in output folder


    '''

    output_file_directory = os.path.join(BASE_DIR, "main\\Website\\output_files")
    upload_folder_directory = os.path.join(BASE_DIR, "main\\static\\convbook")

    directories_managed = [output_file_directory, upload_folder_directory]

    for i in directories_managed:
        initial_directory_manager(i, time_limit = 48).manage_service()



    '''
    
    timer cleaner
    
    '''

    # folder_cleaner(upload_folder_directory).folder_clean()
    # folder_cleaner(output_file_directory).folder_clean()



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
    request.session['uploads'] = upload_folder_directory
    request.session['outputs'] = output_file_directory

    page_id = id_generator(size = 24)


    if request.method == 'POST':

        if "Default" in request.POST:
            message_default = 'You have chosen Default settings, you will be redirected to the pdf upload page'
            messages.success(request, message_default)


            return redirect('ConventionalAudiobook_upload/Default/{page_id}'.format(page_id = page_id))

        if "Custom" in request.POST:

            message_custom = 'You have chosen Custom settings, please upload your pdf and enter your desired values '
            messages.success(request, message_custom)
            return redirect('ConventionalAudiobook_upload/Custom/{page_id}'.format(page_id = page_id))


    return render(request, "main/conventional_audio_pages/Conventional_Audiobook.html", {})
    # return render(request, "main/Conventional_Audiobook.html", {})


'''

'/ConventionalAudiobook_upload' upload form

going to need to 2 paths 

'''

def upload_default(request, page_id):


    file_lmt = 850
    file_size_lmt = file_lmt * 1024 * 1024
    messages.info(request, "Please wait if you are merging massive files, enjoy!")
    messages.warning(request, "The file upload limit is {} MB".format(file_lmt))
    
    # form = upload()
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


            if size >= file_size_lmt:

                messages.error(request, "The file size as exceeded limits please upload a smaller file")
                return redirect(request.path)


            if name[-4:] not in Allowed_formats:
                messages.error(request, " Please upload a pdf file")
                return redirect(request.path)

            else:

                messages.success(request, "The file has uploaded")
                fs = FileSystemStorage()

                '''
                maybe throw a loading page in here
                '''
                print(uploaded_file)






                fs.save(uploaded_file.name, uploaded_file)


                folder_name = request.session.get('folder_name')
                upload_folder_directory = request.session.get('uploads')
                output_file_directory = request.session.get('outputs')

                folder_name = request.session.get('folder_name')
                new_folder_path = os.path.join(upload_folder_directory, folder_name)


                folder_cleaner(new_folder_path).file_path_make()

                request.session['localized_uploads'] = new_folder_path


                # media_root =


                primary_location = os.path.join(BASE_DIR , "main\\static\\{}".format(uploaded_file.name))

                shutil.copy(primary_location, new_folder_path)

                os.remove(primary_location)

                enc_id = id_generator(size = 24)

                return redirect('Default_Processing/{enc_id}/'.format(enc_id = enc_id))




    return render(request, "main/conventional_audio_pages/conv_audio_file_upload.html", {})


'''

default processing page


'''

def default_processing(request, page_id, enc_id):

    basedir = os.path.abspath(os.path.dirname(__file__))
    # upload_folder_directory = os.getcwd() + "\\main\\static\\convbook"


    '''replace this with new folder '''

    # upload_folder_directory = os.path.join(BASE_DIR, "main\\static\\convbook")

    upload_folder_directory = request.session.get('uploads')

    local_directory = request.session.get('localized_uploads')
    files = os.listdir(local_directory)
    request.session['files'] = files

    print(files)
    if len(files) != 0:

        full_file_path = os.path.join(basedir, "{}\\{}".format(local_directory, files[0]))
        print(full_file_path)
        cntx = {}

        '''
        temp.pdf
        '''

        ''':cvar
        the following 2 commands determined where thing is processed.
        
        '''

        # temp_path = os.path.join(BASE_DIR, "main\\static\\convbook\\temp.pdf")

        temp_path = os.path.join(local_directory, "temp.pdf")

        asynchronous_result = conv_default.delay(full_file_path, temp_file = temp_path)



        messages.success(request, "File processing has begun, you will be notified once it is finished")
        reddis_vals = reddis_information(asynchronous_result)
        jobid = reddis_vals.job_id_()
        # result_vals = reddis_vals.values_()
        # cntx['task_id'] = jobid

        request.session['default_jobid'] = jobid
        return redirect('Async/')
        # return render(request, "main/conventional_integrations.html", cntx)


    return render(request, "main/conventional_audio_pages/conv_audio_file_upload.html", {})


def async_default_load(request,page_id, enc_id):
    cntx = {}
    jobid = request.session.get('default_jobid')
    cntx['task_id'] = jobid


    return render(request, "main/conventional_integrations.html", cntx)




def conventional_processing(request):

    task_id = request.GET.get('taskid', None)

    if task_id is not None:

        try:
            job_id, status, result = redis_id_info_(id=task_id).vals()
            results_completion = results_tracker(result)
            process_checker = process_completion(results_completion = results_completion, task_id = task_id)
            job_id, status, result = process_checker.results()
        except Exception:
            pass

        file_out_put = result
        request.session['results'] = file_out_put

        '''
        add javascript and json response
        '''

        print('this is the result: ',result)
        print('this is the file_out_put: ',file_out_put)

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

    return render(request, "main/conventional_integrations.html", {})



def default_downloads(request, page_id, enc_id):

    files = request.session.get('files')
    file_out_put = request.session.get('results')
    basedir = os.path.abspath(os.path.dirname(__file__))


    if len(files) != 0:


        try:


            file_name = os.path.basename(os.path.normpath(file_out_put))
            srs = file_out_put
            outputs = request.session.get('outputs')


            folder_name = request.session.get('folder_name')
            new_outputs = os.path.join(outputs, folder_name)
            folder_cleaner(new_outputs).file_path_make()
            request.session['localized_outputs'] = new_outputs


            # audio_file = request.session.get('outputs')
            audio_file = new_outputs

            shutil.copy(srs, audio_file)

            basedir = os.path.abspath(os.path.dirname(__file__))


            # upload_folder_directory = os.path.join(BASE_DIR, "main\\static\\convbook")



            file_removers(request.session.get('localized_uploads')).remove()

            output_audio_path = os.path.join(audio_file, "{}".format(file_name))
            print(output_audio_path)
            response = FileResponse(open(output_audio_path, 'rb'), as_attachment=True)

            return response


        except Exception:
            messages.success(request, "Your file should have already downloaded, if not please try processing again")
            return render(request, "main/conventional_audio_pages/downloads_custom.html", {})

    # return render(request, "main/conventional_audio_pages/conv_audio_file_upload.html", {})



''''
CUSTOM FUNCTIONS BENEATH THIS
'''




def upload_custom(request, page_id):
    # form = upload()

    file_lmt = 850
    file_size_lmt = file_lmt * 1024 * 1024
    messages.info(request, "Please wait if you are merging massive files, enjoy!")
    messages.warning(request, "The file upload limit is {} MB".format(file_lmt))

    if request.method == "POST":
        pass
        if 'file' not in request.FILES:
            messages.error(request, " Nothing was uploaded please upload a pdf file")
            redirect(request.path)

        elif request.FILES['file'] == '':

            messages.error(request, " No file was uploaded please upload a pdf file")
            redirect(request.path)
        else:

            uploaded_file = request.FILES['file']
            name = uploaded_file.name
            size = uploaded_file.size
            Allowed_formats = [".pdf"]

            if size >= file_size_lmt:

                messages.error(request, "The file size as exceeded limits please upload a smaller file")
                return redirect(request.path)


            if name[-4:] not in Allowed_formats:
                messages.error(request, " Please upload a pdf file")
                redirect(request.path)

            else:

                messages.success(request, "The file has uploaded")
                fs = FileSystemStorage()

                '''
                maybe throw a loading page in here
                '''
                fs.save(uploaded_file.name, uploaded_file)




                folder_name = request.session.get('folder_name')
                upload_folder_directory = request.session.get('uploads')
                output_file_directory = request.session.get('outputs')

                folder_name = request.session.get('folder_name')
                new_folder_path = os.path.join(upload_folder_directory, folder_name)


                folder_cleaner(new_folder_path).file_path_make()

                request.session['localized_uploads'] = new_folder_path


                # media_root =


                primary_location = os.path.join(BASE_DIR , "main\\static\\{}".format(uploaded_file.name))

                shutil.copy(primary_location, new_folder_path)

                os.remove(primary_location)



                # shutil.copy(os.path.join(BASE_DIR, "main\\static\\{}".format(uploaded_file.name)),
                #             os.path.join(BASE_DIR, "main\\static\\convbook"))
                #
                # os.remove(os.path.join(BASE_DIR ,"main\\static\\{}".format(uploaded_file.name)))

                # file_path = os.getcwd() + "\\main\\static\\convbook\\{}".format(uploaded_file.name)

                enc_id = id_generator(size = 24)

                return redirect('Custom_Setting/{enc_id}/'.format(enc_id = enc_id))

    return render(request, "main/conventional_audio_pages/conv_audio_file_upload.html", {})


def custom_setting(request, page_id, enc_id):

    print(request.POST.get("Field1_name"))

    forms = request.POST.get('Field1_name')
    sp_rate = request.POST.get('Field2_name')
    vol_rate = request.POST.get('Field3_name')
    voltype = request.POST.get('vol_type')

    valid_extensions = ["mp3", "ogg"]

    print(forms,sp_rate,vol_rate,voltype)

    voltype_cond = (voltype == str(0) or voltype == str(1))
    spr_cond = type(sp_rate) is str
    vol_rate_cond = type(vol_rate) is str


    if voltype_cond:
        vol_type_int = int(voltype)
        # print(vol_type_int)
    else:
        vol_type_int = None
    if spr_cond:
        try:
            spr_cond_int = int(sp_rate)
        except:
            messages.error(request,"Some error happened, please try again")
            return redirect(request.path)
    else:
        spr_cond_int = None
    if vol_rate_cond:
        try:
            vol_rate_fl = float(vol_rate)
        except:
            messages.error(request,"Some error happened, please try again")
            return redirect(request.path)
            # return render_template('conventional_audio_pages/custom_setting_page.html')
    else:
        vol_rate_fl = None
    values = [forms, vol_type_int, spr_cond_int, vol_rate_fl]

    if None not in values:
        print("ready for processing")
        if request.method == 'POST':
            if forms not in valid_extensions:
                print(forms,valid_extensions)
                text_message = "That is not a valid audio extension ( valid extensions are 'mp3', 'ogg')\
                you will be redirected; please enter values again"
                messages.error(request,text_message)
                return redirect(request.path)

            if spr_cond_int < 0 or spr_cond_int > 400:
                messages.error(request,"Please enter a speech rate between 0 and 400, please enter values again")
                return redirect(request.path)
            ''' debug this why it accepted 2 '''
            if vol_rate_fl < 0 or vol_rate_fl > 1:
                messages.error(request,"Please enter a value between 0 and 1 for the volume rate")
                return redirect(request.path)
            messages.success(request,"Information accepted")





            '''Implement file path algorithm into redis so custom work can begin'''


            basedir = os.path.abspath(os.path.dirname(__file__))
            # upload_folder_directory = os.getcwd() + "\\main\\static\\convbook"

            upload_folder_directory = os.path.join(BASE_DIR , "main\\static\\convbook")

            upload_folder_directory = request.session.get('uploads')

            local_directory = request.session.get('localized_uploads')
            files = os.listdir(local_directory)
            request.session['files'] = files



            files = os.listdir(local_directory)
            full_file_path = os.path.join(basedir, "{}\\{}".format(local_directory, files[0]))

            '''
            asynchronous initialization
            '''
            cntx = {}

            ''''
            temp
            '''

            # temp_path = os.path.join(BASE_DIR, "main\\static\\convbook\\temp.pdf")
            temp_path = os.path.join(local_directory, "temp.pdf")

            asynchronous_result = conv_custom.delay(full_file_path, values , temp_file = temp_path)
            messages.success(request, "File processing has begun, you will be notified once it is finished")
            reddis_vals = reddis_information(asynchronous_result)
            jobid = reddis_vals.job_id_()


            request.session['jobid'] = jobid
            cntx['task_id'] = jobid
            print(cntx)

            sec_id = id_generator(size = 24)
            return redirect("Custom_processing/{sec_id}/".format(sec_id = sec_id))

    return render(request, "main/conventional_audio_pages/custom_setting_page.html", {})

def custom_code_processing(request, page_id, enc_id, sec_id):

    cntx = {}
    jobid = request.session.get('jobid')
    cntx['task_id'] = jobid
    return render(request, "main/conventional_integrations_custom.html", cntx)


def custom_ajax_processing(request):

    print("testing")
    task_id = request.GET.get('taskid', None)

    print(task_id)

    if task_id is not None:

        try:
            job_id, status, result = redis_id_info_(id=task_id).vals()
            results_completion = results_tracker(result)
            process_checker = process_completion(results_completion = results_completion, task_id = task_id)
            job_id, status, result = process_checker.results()
        except Exception:
            pass

        file_out_put = result
        request.session['results'] = file_out_put

        '''
        add javascript and json response
        '''

        print(result)
        print(file_out_put)

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

    return render(request, "main/conventional_integrations.html", {})


def downloads_custom(request, page_id, enc_id, sec_id):



    try:

        # file_out_put = request.session.get('result')
        # basedir = os.path.abspath(os.path.dirname(__file__))

        files = request.session.get('files')
        file_out_put = request.session.get('results')
        basedir = os.path.abspath(os.path.dirname(__file__))

        file_name = os.path.basename(os.path.normpath(file_out_put))
        srs = file_out_put
        outputs = request.session.get('outputs')

        folder_name = request.session.get('folder_name')
        new_outputs = os.path.join(outputs, folder_name)
        folder_cleaner(new_outputs).file_path_make()
        # request.session['localized_outputs'] = new_outputs

        # audio_file = request.session.get('outputs')
        audio_file = new_outputs
        shutil.copy(srs, audio_file)
        basedir = os.path.abspath(os.path.dirname(__file__))
        file_removers(request.session.get('localized_uploads')).remove()

        output_audio_path = os.path.join(audio_file, "{}".format(file_name))
        print(output_audio_path)
        response = FileResponse(open(output_audio_path, 'rb'), as_attachment=True)

        return response


    except Exception:
        messages.success(request, "Your file should have already downloaded, if not please try processing again")
        return render(request, "main/conventional_audio_pages/downloads_custom.html", {})




