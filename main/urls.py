'''

Modified & original work Copyright (c) 2022 Hemanto Bairagi


This code is the sole property of Hemanto Bairagi. 
Any unauthorized replication and use of any code used 
in any form will be a violation of my exclusive Copyright. 

'''


"""celeraydummy URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include,re_path
from . import views, pdf_comp,conv_audio, aud_merger,syn_voice
# from .Website import conv_audio,aud_merger,pdf_comp,syn_voice
# from .Website import aud_merger,syn_voice
from main.tasks import *



urlpatterns = [

path("", views.home, name = "home"),
# path("Regression/", views.Reg_page, name = "Regs"),
# path("Regression/Processing/", views.Regression_processor, name = "Processing"),
# path("Regression/DQ/", views.Dq_processor, name = "DQ Async Test"),
# path("Regression/Landing/", views.Finish, name = "Landing Page"),
# path('loading/',views.Regression_processor ,name="loading"),
path("django-rq/", include("django_rq.urls")),


path("ConventionalAudiobook/", conv_audio.Conventinal_audio, name = "Conventional Audio"),
path("ConventionalAudiobook/ConventionalAudiobook_upload/Default/<str:page_id>/", conv_audio.upload_default, name = "Default Audio"),
path("ConventionalAudiobook/ConventionalAudiobook_upload/Default/<str:page_id>/Default_Processing/<str:enc_id>/", conv_audio.default_processing,
     name = "Default Processing"),

path("ConventionalAudiobook/ConventionalAudiobook_upload/Default/<str:page_id>/Default_Processing/<str:enc_id>/Async/", conv_audio.async_default_load,
     name = "Default Processing"),
path("Process/", conv_audio.conventional_processing, name = "Default Processing"),
path("ConventionalAudiobook/ConventionalAudiobook_upload/Default/<str:page_id>/Default_Processing/<str:enc_id>/Async/Downloads/",
     conv_audio.default_downloads, name = "Default Processing"),


path("ConventionalAudiobook/ConventionalAudiobook_upload/Custom/<str:page_id>/", conv_audio.upload_custom, name = "Custom Audio"),
path("ConventionalAudiobook/ConventionalAudiobook_upload/Custom/<str:page_id>/Custom_Setting/<str:enc_id>/", conv_audio.custom_setting,
     name = "Custom Settings"),
path("ConventionalAudiobook/ConventionalAudiobook_upload/Custom/<str:page_id>/Custom_Setting/<str:enc_id>/Custom_processing/<str:sec_id>/",
     conv_audio.custom_code_processing, name = "Custom Processor"),

path("CQ/", conv_audio.custom_ajax_processing, name = "Custom Downloads"),
path("ConventionalAudiobook/ConventionalAudiobook_upload/Custom/<str:page_id>/Custom_Setting/<str:enc_id>/Custom_processing/<str:sec_id>/Downloads/",
     conv_audio.downloads_custom, name = "Custom Processor"),




path("AudioMerge/", aud_merger.upload_file, name = "MP3 Merger"),
path("AudioMerge/Merge/<str:page_id>/", aud_merger.audio_processing, name = "MP3 Merger"),

path("AudioMerge/Merge/<str:page_id>/Large_files/<str:enc_id>/", aud_merger.large_file_processing, name = "MP3 Merger"),
path("AudioMerge/Merge/<str:page_id>/Large_files/<str:enc_id>/Large_Async/", aud_merger.large_async, name = "MP3 Merger"),
path("ALP/", aud_merger.large_file_asyncronous, name = "MP3 Merger"),
path("AudioMerge/Merge/<str:page_id>/Large_files/<str:enc_id>/Large_Async/Downloads/", aud_merger.large_file_downloads, name = "MP3 Merger"),



path("AudioMerge/Merge/<str:page_id>/Mid_files/<str:enc_id>/", aud_merger.mid_file_processing, name = "MP3 Merger"),
path("AudioMerge/Merge/<str:page_id>/Mid_files/<str:enc_id>/Processing/", aud_merger.mid_file_calculation, name = "MP3 Merger"),
path("AudioMerge/Merge/<str:page_id>/Mid_files/<str:enc_id>/Processing/Mid_Async/", aud_merger.mid_async, name = "MP3 Merger"),
path("AMP/", aud_merger.mid_file_asyncronous, name = "MP3 Merger"),
path("AudioMerge/Merge/<str:page_id>/Mid_files/<str:enc_id>/Processing/Mid_Async/Downloads/", aud_merger.mid_downloads, name = "MP3 Merger"),


path("AudioMerge/Merge/<str:page_id>/Small_files/<str:enc_id>/", aud_merger.small_file_processing, name = "MP3 Merger"),
path("AudioMerge/Merge/<str:page_id>/Small_files/<str:enc_id>/Small_Async/", aud_merger.small_async, name = "MP3 Merger"),
path("ASP/", aud_merger.small_file_asyncronous, name = "MP3 Merger"),
path("AudioMerge/Merge/<str:page_id>/Small_files/<str:enc_id>/Small_Async/Downloads/", aud_merger.small_file_downloads, name = "MP3 Merger"),



path("PDF-compression/", pdf_comp.upload_file, name = "PDF Compression"),
path("PDF-compression/Compression/<str:page_id>/", pdf_comp.PDF_compression, name = "PDF Compression"),
path("PDF-compression/Compression/<str:page_id>/Compression_module/<str:enc_id>/",
     pdf_comp.pdf_compressor_mod, name = "PDF compression module"),
path("PQ/", pdf_comp.pdf_loader,name = "PDF Loading"),
path("PDF-compression/Compression/<str:page_id>/Compression_module/<str:enc_id>/Downloads/",
     pdf_comp.pdf_downloads, name = "PDF Downloads"),




#
# path("VoiceSynthesis/", syn_voice.upload_file_pdf, name = "Voice Synthesis PDF"),
# path("VoiceSynthesis/Audio/", syn_voice.upload_file_audio, name = "Voice Audio"),
# path("VoiceSynthesis/Audio/Synthesis/", syn_voice.synthesis, name = "Voice Synthesis"),
# path("VoiceSynthesis/Audio/Synthesis/Processing/", syn_voice.synthetic_processor, name = "Voice Processing"),
# path("Synth_processing/", syn_voice.synthetic_processing_unit, name = "Synthetic processing"),
# path("VoiceSynthesis/Audio/Synthesis/Processing/Downloads/", syn_voice.synthetic_downloads, name = "Voice Downloads"),


path("VoiceSynthesis/", syn_voice.upload_file_pdf, name = "Voice Synthesis PDF"),
path("VoiceSynthesis/Audio/<str:page_id>/", syn_voice.upload_file_audio, name = "Voice Audio"),
path("VoiceSynthesis/Audio/<str:page_id>/Synthesis/<str:enc_id>/", syn_voice.synthesis, name = "Voice Synthesis"),
path("VoiceSynthesis/Audio/<str:page_id>/Synthesis/<str:enc_id>/Processing/", syn_voice.synthetic_processor, name = "Voice Processing"),
path("Synth_processing/", syn_voice.synthetic_processing_unit, name = "Synthetic processing"),
path("VoiceSynthesis/Audio/<str:page_id>/Synthesis/<str:enc_id>/Processing/Downloads/",
     syn_voice.synthetic_downloads, name = "Voice Downloads"),



]


"""

url: "/Regression/DQ/",
data: {"taskid": TaskID},
method: "GET",
dataType: "json",
success: function(data){  }
"""

"""
if (data["state"] == "started"){console.log('Task is started')},

if (data["state"] == "finished"){console.log('Task is finished')}

"""
