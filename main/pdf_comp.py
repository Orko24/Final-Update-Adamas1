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
from .redis_tracker import *
import json
from .tasks import *
from .file_cleaners import *
from pathlib import Path
from .multi_users import *

BASE_DIR = Path(__file__).resolve().parent.parent

# ALLOWED_EXTENSIONS = {'pdf'}
#
#
# def allowed_file(filename):
#     return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def upload_file(request):



    output_file_directory = os.path.join(BASE_DIR, "main\\Website\\output_files")
    # os.path.join(BASE_DIR, "main\\Website\\Compression_pdf")
    upload_folder_directory = os.path.join(BASE_DIR, "main\\static\\Compression_pdf")


    random_user_id = id_generator()
    folder_name = "user_{}".format(random_user_id)

    request.session['folder_name'] = folder_name
    request.session['uploads'] = upload_folder_directory
    request.session['outputs'] = output_file_directory


    directories_managed = [output_file_directory, upload_folder_directory]

    for i in directories_managed:
        initial_directory_manager(i, time_limit = 48).manage_service()

    messages.info(request,"Please wait if you are uploading large files, Enjoy!")
    messages.info(request, "Please keep pdf names as short as possible to maintain web stability")

    '''
        Introduce multiple file size limits and try the drag and drop stuff via html and javascript
    '''

    Allowed_formats = [".pdf"]
    file_lmt = 10 * 1024
    file_size_lmt = file_lmt * 1024 * 1024
    total_file_size = 0

    messages.warning(request,
                     "Please keep total file sizes below {} GB as that is the current limit offered".format(
                         round(file_size_lmt / (1024 * 1024 * 1024))))

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

        for file in files:
            name = file.name
            size = file.size
            total_file_size = size + total_file_size

            print(name)

            if name == '':

                messages.error(request, 'No selected file')
                return redirect(request.path)

            if file.name[-4:] not in Allowed_formats:
                messages.error(request, "The file {} is not a .pdf".format(name))
                messages.error(request, "Please enter all files in the pdf format")
                return redirect(request.path)

        if total_file_size >= file_size_lmt:
            messages.error(request, "Total file size exceeded file upload limit, please try in chunks")
            return redirect(request.path)



        print(files)
        count = 0

        for file in files:

            ''''
            issues maybe
            '''

            name = file.name
            size = file.size
            Allowed_formats = [".pdf"]

            if name == '':
                messages.error(request, 'No selected file')
                return redirect(request.path)


            if file.name[-4:] in Allowed_formats:
                fs = FileSystemStorage()

                '''
                maybe throw a loading page in here
                '''
                file_name = file.name
                # new_file_name = file_name
                print("file name: ", file_name)

                comma_count = file_name.count(',')

                print("commma found: ", comma_count)

                char_lm = 100

                if len(file_name) > char_lm:

                    new_file_name = "{}_{}{}".format(file_name[0:10], count, file_name[-4:])

                    if new_file_name.count(" ")> 1:

                        new_file_name = file_name.replace(' ', '_')
                    print("file name: ", new_file_name)
                    print('File names: ', new_file_name)
                    file_name = new_file_name
                    count = count + 1
                    messages.info(request, "A file was renamed to maintain web stability")

                '''could throw fs.save into the if statements to clean stuff up, else: fs.save'''

                if len(file_name) < char_lm and comma_count > 0:
                    new_file_name = "{}_{}{}".format(file_name[:-4].replace(',', '_'), count, file_name[-4:])

                    if new_file_name.count(" ")> 1:

                        new_file_name = file_name.replace(' ', '_')

                    print("file name: ", new_file_name)
                    count = count + 1
                    messages.success(request, "There was been a problem in comma detection, \
                    thus the file has been renamed to {}".format(new_file_name))
                    file_name = new_file_name




                # file_name = new_file_name
                fs.save(file_name, file)
                print(file_name)

                '''
                maybe put an exception
                '''
                # print()

                primary_upload = os.path.join(BASE_DIR,  "main\\static\\{}".format(file_name))


                move_upload = os.path.join(upload_folder_directory, folder_name)

                # folder_cleaner(new_folder_path).file_path_make()
                folder_cleaner(move_upload).file_path_make()

                # shutil.copy(os.path.join(BASE_DIR,  "main\\static\\{}".format(file_name)),
                # os.path.join(BASE_DIR, "main\\static\\Compression_pdf"))

                # shutil.copy(primary_upload, move_upload)
                # os.remove(primary_upload)


                try:
                    shutil.copy(primary_upload, move_upload)
                    os.remove(primary_upload)

                except:

                    messages.error(request, "Some error has occured, you will be redirected to the upload page")
                    return redirect(request.path)


                # file_path = os.getcwd() + "\\main\\static\\Compression_pdf\\{}".format(file_name)


                ''''
                redirect to processing page and a loading gif
                '''

        messages.success(request, "The files have uploaded")

        page_id = id_generator(size=24)

        request.session['page_id'] = page_id

        return redirect('Compression/{page_id}/'.format(page_id = page_id))

    return render(request, "main/PDF_compressor/PDF_compression.html", {})


def PDF_compression(request, page_id):

    # request.session['folder_name'] = folder_name
    # request.session['uploads'] = upload_folder_directory
    # request.session['outputs'] = output_file_directory

    folder_name = request.session.get('folder_name')
    upload_folder_directory = request.session.get('uploads')
    output_file_directory = request.session.get('outputs')

    localized_directory = os.path.join(upload_folder_directory, folder_name)



    files_ = os.listdir(localized_directory)

    upload_folder_pdf = localized_directory

    print(files_)

    if len(files_) != 0:

        new_files = []
        for file in files_:

            # print("file length", len(file))
            file_path = os.path.join(upload_folder_pdf, "{}".format(file))
            # print(file_path)

            if file_path != file_path.replace(" ", "_"):
                os.rename(file_path, file_path.replace(" ", "_"))
                file_path = file_path.replace(" ", "_")

            length_limit = 100

            # if len(file) > length_limit and file != file.strip():
            if len(file) > length_limit:
                new_file_path = os.path.join(upload_folder_pdf, "{}".format(file[:length_limit - 5].replace(" ", "_") + file[-4:]))

                print(file.strip())
                print(file.replace(" ", "_"))

                os.rename(file_path, new_file_path)
                file_path = new_file_path

                # print(new_file_path)
            new_files.append(file_path)

        request.session['new_files'] = new_files

        asynchronous_result = a_s_pc.delay(new_files)
        messages.success(request, "File processing has begun, you will be notified once it is finished")
        reddis_vals = reddis_information(asynchronous_result)
        jobid = reddis_vals.job_id_()
        request.session['jobid'] = jobid

        # enc_id = request.session.get('page_id')

        enc_id = id_generator(size=24)

        return redirect("Compression_module/{enc_id}".format(enc_id = enc_id))

    return render(request, "main/PDF_compressor/PDF_compression.html", {})


def pdf_compressor_mod(request, page_id,enc_id):

    new_files = request.session.get('new_files')
    jobid = request.session.get('jobid')

    cntx = {}
    # asynchronous_result = a_s_pc.delay(new_files)
    # reddis_vals = reddis_information(asynchronous_result)
    # jobid = reddis_vals.job_id_()
    cntx['task_id'] = jobid
    print(cntx)

    request.session['selected_pdf_id'] = jobid
 

    return render(request, "main/pdf_integration.html", cntx)



def state(status):
    if status == "finished":
        return True
    return False


def pdf_loader(request):
    print("testing")
    # task_id = request.GET.get('task_id', None)
    task_id = request.GET.get('taskid', None)

    # task_id = request.GET.get('taskid')

    print(task_id)

    if task_id is not None:

        # messages.success(request, "File processing is complete your download will be initiating")

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


def pdf_downloads(request, page_id, enc_id):


    folder_name = request.session.get('folder_name')
    upload_folder_directory = request.session.get('uploads')
    output_file_directory = request.session.get('outputs')

    localized_directory = os.path.join(upload_folder_directory, folder_name)




    

    try:

        # upload_folder_pdf = os.path.join(BASE_DIR, "main\\static\\Compression_pdf")

        upload_folder_pdf = localized_directory
        zip_output = "PDF_compressed_zip"

        zip_path = os.path.join(upload_folder_pdf, "{}".format(zip_output))
        
        folder_creation_destruction(zip_path).folder_creation()

        result = request.session.get('result')
        compressed_files = result

        for i in compressed_files:
            shutil.copy(i, zip_path)
            os.remove(i)

        '''
        might directly move it to output folder
        '''

        # out_put_folder = os.path.join(BASE_DIR , "main\\Website\\output_files")

        out_put_folder = os.path.join(output_file_directory, folder_name)
        folder_cleaner(out_put_folder).file_path_make()


        shutil.make_archive(os.path.join(out_put_folder , "{}".format(zip_output)), "zip", zip_path)
        folder_creation_destruction(zip_path).folder_destruction()
        entry = os.path.join(out_put_folder, zip_output + ".zip")
        zip_file = open(entry, 'rb')

        return FileResponse(zip_file)

    except Exception:
        messages.success(request, "Your file should have already downloaded, if not please try processing again")
        return render(request, "main/PDF_compressor/PDF_downloads.html", {})