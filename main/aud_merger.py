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

from django.http import HttpResponse
from django.http import FileResponse
import os
from pathlib import Path

# from .redis_tracker import *
# from .file_cleaners import *
# BASE_DIR = Path(__file__).resolve().parent.parent

# print(os.path.join(BASE_DIR, "main\\Website\\output_files"))

from .tasks import *
from .redis_tracker import *
from .file_cleaners import *
from .multi_users import *


BASE_DIR = Path(__file__).resolve().parent.parent
def upload_file(request):
    '''
    Try to upload multiple files to pdf commpressor
    '''

    output_base_path = "main\\Website\\output_files"
    upload_base_path = "main\\static\\Audio_Merge"

    output_file_directory = os.path.join(BASE_DIR, output_base_path)
    # os.path.join(BASE_DIR, "main\\Website\\Compression_pdf")
    upload_folder_directory = os.path.join(BASE_DIR, upload_base_path)
    # file_removers(output_file_directory).remove()
    # file_removers(upload_folder_directory ).remove()


    random_user_id = id_generator()
    folder_name = "user_{}".format(random_user_id)

    request.session['output_base_path'] = output_base_path
    request.session['upload_base_path'] = upload_base_path

    request.session['folder_name'] = folder_name
    request.session['uploads'] = upload_folder_directory
    request.session['outputs'] = output_file_directory



    directories_managed = [output_file_directory, upload_folder_directory]

    for i in directories_managed:
        initial_directory_manager(i, time_limit = 48).manage_service()

    '''
    Introduce multiple file size limits and try the drag and drop stuff via html and javascript
    '''
    Allowed_formats = [".mp3"]
    file_lmt = 10 * 1024
    file_size_lmt = file_lmt * 1024 * 1024
    total_file_size = 0


    messages.info(request, "Please wait if you are merging massive files, enjoy!")
    messages.info(request, "Please keep mp3 names without spaces maintain web stability")
    messages.warning(request,
                     "Please keep total file sizes below {} GB as that is the current limit offered".format(
                         round(file_size_lmt/(1024 * 1024 * 1024))))

    if request.method == "POST":

        if 'files[]' not in request.FILES:
            messages.error(request, 'No file part')
            return redirect(request.path)

        files = request.FILES.getlist('files[]')

        '''
        
        Experimental file size limits
        
        '''

        '''
        put a file size checker right here, if the files exceed it send that shit back to the homepage
        '''

        messages.info(request, "Do note the more files you upload the longer the upload wait time will be")

        for file in files:
            name = file.name
            size = file.size
            total_file_size = size + total_file_size

            if name == '':
                messages.error(request, 'No selected file')
                return redirect(request.path)

            if file.name[-4:] not in Allowed_formats:

                messages.error(request, "Please enter all files in the mp3 format")
                return redirect(request.path)

        if total_file_size >= file_size_lmt:

            messages.error(request, "Total file size exceeded file upload limit, please try in chunks")
            return redirect(request.path)


        count = 0
        for file in files:

            name = file.name

            if name == '':
                messages.error(request, 'No selected file')
                return redirect(request.path)

            if file.name[-4:] in Allowed_formats:
                fs = FileSystemStorage()
                file_name = file.name
                print(file_name)
                if file_name != "{}.mp3".format(count):

                # if file_name != file_name.strip():

                    # file_name = file_name.strip()
                    file_name = "{}.mp3".format(count)

                    print(file_name)

                fs.save(file_name, file)

                # os.join.path(BASE_DIR, "main\\static\\{}".format(file_name))
                # os.join.path(BASE_DIR, "\\main\\static\\Audio_Merge")

                primary_uploads = os.path.join(BASE_DIR, "main\\static\\{}".format(file_name))

                localized_upload = os.path.join(upload_folder_directory, folder_name)
                folder_cleaner(localized_upload).file_path_make()

                shutil.copy(primary_uploads,localized_upload)

                # shutil.copy(os.path.join(BASE_DIR, "main\\static\\{}".format(file_name)),
                #             os.path.join(BASE_DIR, "main\\static\\Audio_Merge"))


                # os.remove(os.path.join(BASE_DIR, "main\\static\\{}".format(file_name)))

                os.remove(primary_uploads)

                # file_path = os.getcwd() + "\\main\\static\\Audio_Merge\\{}".format(file_name)
                count = count + 1

        messages.success(request, "The files have uploaded")

        page_id = id_generator(size = 24)

        return redirect('Merge/{page_id}/'.format(page_id = page_id))

    return render(request, "main/Audio_merger/Audio_merger.html", {})


def audio_processing(request, page_id):
    '''
    merger_software
    Say that this is beta version and it should work if all of its consistent mp3 files provided the lengths
    are consistent when uploading. Smarter algorithms for media processing will be coming online soon
    if merger folder has less than 2 audio files,
    delete the file and redirect to upload
    measure the duration of each audio file, if average duration is more than 4 mins employ the larger one
    if less than convert files to wave files and merge them
    if total duration of all files exceeds 30 mins,
    divide files into groups that constitute 30 mins; merge them into files for 30 mins and take those larger files
    merge them using the cmd tool
    Go back and add Guard rails, i.e upload limitations like pdf size for the voice synthesis and upload file limits
    (cap it at 700 MBs to mess with the competition)
    '''
    # os.join.path(BASE_DIR, "main\\static\\Audio_Merge")

    # upload_folder_pdf = os.path.join(BASE_DIR, "main\\static\\Audio_Merge")

    localized_directory = os.path.join(request.session.get('uploads'), request.session.get('folder_name'))

    # upload_folder_pdf = request.session.get('uploads')

    upload_folder_pdf = localized_directory

    files_prime = os.listdir(upload_folder_pdf)
    for i in files_prime:
        if i != i.strip():
            os.rename(i, i.strip())
    files_ = os.listdir(upload_folder_pdf)

    print(files_)
    file_sizes = []
    file_paths = []
    for i in files_:
        print(i)

        file_path_ = os.path.join(upload_folder_pdf, "{}".format(i))
        # print(file_paths)
        file_paths.append(file_path_)
        st = os.stat(file_path_)
        file_size = st.st_size
        file_sizes.append(file_size)

    # print(file_sizes)
    file_sizes_avg = np.mean(np.array(file_sizes))
    filze_size_total = np.sum(np.array(file_sizes))
    file_lmt = 30
    file_size_lmt = file_lmt * 1024 * 1024

    '''
    conditional processing
    '''

    request.session['file_paths'] = file_paths
    request.session['files_'] = files_
    request.session['upload_folder_pdf'] = upload_folder_pdf
    request.session['file_size_lmt'] = file_size_lmt
    ''''
    Large
    '''

    enc_id = id_generator(size = 24)

    if filze_size_total > file_size_lmt and file_sizes_avg < file_size_lmt:

        '''''
        Create algorithm that measures everyfile
        then sections off names when the sum of those files hits file size limits
        concentate them using moviepy
        then merge the resultant files using admin batch
        '''
        # messages.info(request, "The file size limit is: {} bytes and the \
        #                       average file size is: {} \
        #                       bytes, total file size is : {}".format(file_size_lmt, file_sizes_avg, filze_size_total))

        return redirect('Mid_files/{enc_id}/'.format(enc_id = enc_id))



    if file_sizes_avg > file_size_lmt:


        # messages.info(request,"The file size limit is: {} bytes and the \
        #               average file size is: {} \
        #               bytes, total file size is : {}".format(file_size_lmt, file_sizes_avg, filze_size_total))

        return redirect('Large_files/{enc_id}/'.format(enc_id = enc_id))


    ''''
    small files
    '''
    if file_sizes_avg < file_size_lmt:

        # messages.info(request, "The file size limit is: {} bytes and the \
        #                       average file size is: {} \
        #                       bytes, total file size is : {}".format(file_size_lmt, file_sizes_avg, filze_size_total))


        return redirect('Small_files/{enc_id}/'.format(enc_id = enc_id))

    return render(request, "main/Audio_merger/Audio_processing_page.html", {})



def large_file_processing(request,page_id, enc_id): #<---- "AudioMerge/Merge/Large_files/"

    # end_file_name = "merged_audio.mp3"


    # folder_name = request.session.get('folder_name')
    # upload_folder_directory = request.session.get('uploads')
    # output_file_directory = request.session.get('outputs')
    #
    # output_base_path = request.session.get('output_base_path')
    # upload_base_path = request.session.get('upload_base_path')
    #
    # localized_outputs = os.path.join(output_file_directory, folder_name)
    # folder_cleaner(localized_outputs).file_path_make()
    #
    # '''
    #
    # this is the issue
    #
    # '''
    #
    # local_file = os.path.join(output_base_path, folder_name)
    #
    # # end_file = "main\\Website\\output_files\\merged_audio"
    #
    # end_file = os.path.join(local_file, "merged_audio")
    #
    #
    file_paths = request.session.get('file_paths')
    #


    folder_name = request.session.get('folder_name')
    upload_folder_directory = request.session.get('uploads')
    output_file_directory = request.session.get('outputs')

    output_base_path = request.session.get('output_base_path')
    upload_base_path = request.session.get('upload_base_path')

    localized_outputs = os.path.join(output_file_directory, folder_name)
    folder_cleaner(localized_outputs).file_path_make()

    '''

    this is the issue

    '''

    local_file = os.path.join(output_base_path, folder_name)

    # end_file = "main\\Website\\output_files\\merged_audio"

    end_file = os.path.join(BASE_DIR, local_file, "merged_audio")

    p = Path(end_file)

    # print(list(p.parts)[1:])
    #
    # print(os.path.join(*list(p.parts)[1:]))

    end_file = os.path.join(*list(p.parts)[1:])



    # cntx = {}
    asynchronous_result = Large_file_merger.delay(file_paths = file_paths, end_file=end_file)
    messages.success(request, "File processing has begun, you will be notified once it is finished")
    reddis_vals = reddis_information(asynchronous_result)
    jobid = reddis_vals.job_id_()
    request.session['task_id'] = jobid
    return redirect('Large_Async/')


def large_async(request,page_id, enc_id):

    jobid = request.session.get('task_id')
    cntx = {}
    cntx['task_id'] = jobid
    return render(request, "main/audiomerger_integrations_large_files.html", cntx)



def large_file_asyncronous(request):

    print("testing")
    task_id = request.GET.get('taskid', None)
    print(task_id)

    if task_id is not None:

        try:
            job_id, status, result = redis_id_info_(id=task_id).vals()
            results_completion = results_tracker(result)
            process_checker = process_completion(results_completion=results_completion, task_id=task_id)
            job_id, status, result = process_checker.results()
        except Exception:
            pass

        file_out_put = result
        request.session['results'] = file_out_put

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




def large_file_downloads(request,page_id, enc_id):

    # file_paths = request.session.get('file_paths')
    # end_file_name = "merged_audio.mp3"

    # for i in file_paths:
    #     os.remove(i)
    # merged_path = os.getcwd() + "\\main\\Website\\output_files\\{}".format(end_file_name)
    # response = FileResponse(open(merged_path, 'rb'), as_attachment=True)

    # request.session['folder_name'] = folder_name
    # request.session['uploads'] = upload_folder_directory
    # request.session['outputs'] = output_file_directory

    folder_name = request.session.get('folder_name')
    upload_folder_directory = request.session.get('uploads')
    output_file_directory = request.session.get('outputs')

    localized_outputs = os.path.join(output_file_directory, folder_name)
    folder_cleaner(localized_outputs).file_path_make()




    try:

        file_paths = request.session.get('file_paths')
        end_file_name = "merged_audio.mp3"

        for i in file_paths:
            os.remove(i)

        # os.path.join(BASE_DIR,"main\\Website\\output_files\\{}".format(end_file_name))
        # merged_path = os.path.join(BASE_DIR,"main\\Website\\output_files\\{}".format(end_file_name))

        merged_path = os.path.join(localized_outputs,end_file_name)





        response = FileResponse(open(merged_path, 'rb'), as_attachment=True)

        return response
    except Exception:
        messages.success(request, "Your file should have already downloaded, if not please try processing again")
        return render(request, "main/Audio_merger/Audio_processing_page.html", {})






def mid_file_processing(request,page_id, enc_id):
    '''''
    Create algorithm that measures everyfile
    then sections off names when the sum of those files hits file size limits
    concentate them using moviepy
    then merge the resultant files using admin batch
    '''

    files_ = request.session.get('files_')
    upload_folder_pdf = request.session.get('upload_folder_pdf')

    # upload_folder_pdf = request.session.get('uploads')

    file_size_lmt = request.session.get('file_size_lmt')

    file_sizes = []
    file_paths = []

    for i in files_:
        print(i)

        file_path_ = os.path.join(upload_folder_pdf, "{}".format(i))
        # print(file_paths)
        file_paths.append(file_path_)
        st = os.stat(file_path_)
        file_size = st.st_size
        file_sizes.append(file_size)

    total_file_lst = []
    total_size = 0
    sub_list = []

    for file_pos in range(len(file_sizes)):

        sizes = file_sizes[file_pos]
        file_name = file_paths[file_pos]
        sub_list.append(file_name)
        total_size = sizes + total_size

        if total_size > file_size_lmt:
            total_file_lst.append(sub_list)
            total_size = 0
            sub_list = []

    if len(sub_list) != 0:
        total_file_lst.append(sub_list)

    print(total_file_lst)

    request.session['total_file_lst'] = total_file_lst

    return redirect('Processing/')


def mid_file_calculation(request,page_id, enc_id):
    folder_name = request.session.get('folder_name')
    upload_folder_directory = request.session.get('uploads')
    output_file_directory = request.session.get('outputs')

    output_base_path = request.session.get('output_base_path')
    upload_base_path = request.session.get('upload_base_path')

    localized_outputs = os.path.join(output_file_directory, folder_name)
    folder_cleaner(localized_outputs).file_path_make()

    '''

    this is the issue

    '''

    local_file = os.path.join(output_base_path, folder_name)

    # end_file = "main\\Website\\output_files\\merged_audio"

    end_file = os.path.join(BASE_DIR, local_file, "merged_audio")

    p = Path(end_file)

    # print(list(p.parts)[1:])
    #
    # print(os.path.join(*list(p.parts)[1:]))

    end_file = os.path.join(*list(p.parts)[1:])


    # end_file = os.path.join("Users\\Owner\\Desktop\\Adamas_production_1\\main\\Website", "output_files\\merged_audio")

    upload_folder_pdf = request.session.get('upload_folder_pdf')
    total_file_lst = request.session.get('total_file_lst')

    print('Calculation section', total_file_lst)

    asynchronous_result = mid_file_merger.delay(total_file_lst, upload_folder_pdf, end_file)
    messages.success(request, "File processing has begun, you will be notified once it is finished")
    reddis_vals = reddis_information(asynchronous_result)
    jobid = reddis_vals.job_id_()
    request.session["jobid"] = jobid
    return redirect('Mid_Async/')


def mid_async(request,page_id, enc_id):
    jobid = request.session.get('jobid')
    cntx = {}
    cntx['task_id'] = jobid
    return render(request, "main/audiomerger_integrations_mid_files.html", cntx)


def mid_file_asyncronous(request):
    print("testing")
    task_id = request.GET.get('taskid', None)

    print(task_id)

    if task_id is not None:

        try:
            job_id, status, result = redis_id_info_(id=task_id).vals()
            results_completion = results_tracker(result)
            process_checker = process_completion(results_completion=results_completion, task_id=task_id)
            job_id, status, result = process_checker.results()

        except Exception:
            pass

        file_out_put = result
        request.session['results'] = file_out_put
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


def mid_downloads(request,page_id, enc_id):
    # upload_folder_pdf = request.session.get('upload_folder_pdf')
    # file_removers(upload_folder_pdf).remove()
    # end_file_name = "merged_audio.mp3"
    # merged_path = os.getcwd() + "\\main\\Website\\output_files\\{}".format(end_file_name)
    # # print(merged_path)
    # response = FileResponse(open(merged_path, 'rb'), as_attachment=True)
    # messages.success(request, "File processing is complete your download will be initiating")


    folder_name = request.session.get('folder_name')
    upload_folder_directory = request.session.get('uploads')
    output_file_directory = request.session.get('outputs')

    output_base_path = request.session.get('output_base_path')
    upload_base_path = request.session.get('upload_base_path')

    localized_outputs = os.path.join(output_file_directory, folder_name)
    folder_cleaner(localized_outputs).file_path_make()

    try:

        file_paths = request.session.get("file_paths")
        for i in file_paths:
            os.remove(i)

        upload_folder_pdf = request.session.get('upload_folder_pdf')
        file_removers(upload_folder_pdf).remove()
        end_file_name = "merged_audio.mp3"
        # merged_path = os.getcwd() + "\\main\\Website\\output_files\\{}".format(end_file_name)
        # print(merged_path)

        merged_path = os.path.join(localized_outputs, end_file_name)

        # merged_path = os.path.join(BASE_DIR, "main\\Website\\output_files\\{}".format(end_file_name))

        response = FileResponse(open(merged_path, 'rb'), as_attachment=True)
        # messages.success(request, "File processing is complete your download will be initiating")

        return response
    except Exception:
        messages.success(request, "Your file should have already downloaded, if not please try processing again")
        return render(request, "main/Audio_merger/Audio_processing_page.html", {})




def small_file_processing(request, page_id, enc_id):
    # cntx = {}
    files_ = request.session.get("files_")
    # end_file = "main\\Website\\output_files\\merged_audio.mp3"

    '''
    
    localized file variable
    
    
    '''

    folder_name = request.session.get('folder_name')
    upload_folder_directory = request.session.get('uploads')
    output_file_directory = request.session.get('outputs')

    output_base_path = request.session.get('output_base_path')
    upload_base_path = request.session.get('upload_base_path')

    localized_outputs = os.path.join(output_file_directory, folder_name)
    folder_cleaner(localized_outputs).file_path_make()

    end_file = os.path.join(output_base_path, folder_name, "merged_audio.mp3")




    upload_folder_pdf = request.session.get("upload_folder_pdf")
    asynchronous_result = small_files.delay(files_, end_file, upload_folder_pdf)
    # return redirect('Downloads/')
    messages.success(request, "File processing has begun, you will be notified once it is finished")
    reddis_vals = reddis_information(asynchronous_result)
    jobid = reddis_vals.job_id_()
    request.session['jobid'] = jobid
    return redirect('Small_Async/')


def small_async(request,page_id, enc_id):
    jobid = request.session.get('jobid')
    cntx = {}
    cntx['task_id'] = jobid
    return render(request, "main/audiomerger_integrations_small_files.html", cntx)


def small_file_asyncronous(request):
    print("testing")
    task_id = request.GET.get('taskid', None)
    print(task_id)

    if task_id is not None:

        try:
            job_id, status, result = redis_id_info_(id=task_id).vals()
            results_completion = results_tracker(result)
            process_checker = process_completion(results_completion=results_completion, task_id=task_id)
            job_id, status, result = process_checker.results()
        except Exception:
            pass

        file_out_put = result
        request.session['results'] = file_out_put

        print(result)
        print(file_out_put)

        redirect_url = "Downloads/"
        context = {'state': status, 'result': result, 'state_binary': results_tracker(result),
                   'redir': redirect_url,
                   }

        data = json.dumps(context)
        print("context: ", context)
        print("data: ", data)
        request.session['result'] = result
        # messages.success(request, "File processing is complete your download will be initiating")
        return HttpResponse(data, content_type="application/json")


def small_file_downloads(request,page_id, enc_id):



    folder_name = request.session.get('folder_name')
    upload_folder_directory = request.session.get('uploads')
    output_file_directory = request.session.get('outputs')

    output_base_path = request.session.get('output_base_path')
    upload_base_path = request.session.get('upload_base_path')

    localized_outputs = os.path.join(output_file_directory, folder_name)
    folder_cleaner(localized_outputs).file_path_make()




    try:

        file_paths = request.session.get("file_paths")
        for i in file_paths:
            os.remove(i)

        end_file_name = "merged_audio.mp3"

        # os.path.join(BASE_DIR, "main\\Website\\output_files\\{}".format(end_file_name))
        # merged_path = os.path.join(BASE_DIR, "main\\Website\\output_files\\{}".format(end_file_name))

        merged_path = os.path.join(localized_outputs,end_file_name)

        response = FileResponse(open(merged_path, 'rb'), as_attachment=True)

        return response
    except Exception:
        messages.success(request, "Your file should have already downloaded, if not please try processing again")
        return render(request, "main/Audio_merger/Audio_processing_page.html", {})
