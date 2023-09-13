'''

Modified & original work Copyright (c) 2022 Hemanto Bairagi


This code is the sole property of Hemanto Bairagi. 
Any unauthorized replication and use of any code used 
in any form will be a violation of my exclusive Copyright. 

'''

from PDFNetPython3.PDFNetPython import PDFDoc, Optimizer, SDFDoc, PDFNet
import cv2
import pytesseract
import os
import os.path
import shutil
from pdf2image import convert_from_path
import soundfile as sf

import PyPDF2
from gtts import gTTS
from PyPDF2 import PdfFileWriter, PdfFileReader
import pyttsx3
from moviepy.editor import concatenate_audioclips, AudioFileClip

import subprocess
import os.path
import sys
import shutil

print(os.getcwd() + "\\Tesseract-OCR\\tesseract.exe")