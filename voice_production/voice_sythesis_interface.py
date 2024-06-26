'''

Modified & original work Copyright (c) 2022 Hemanto Bairagi


This code is the sole property of Hemanto Bairagi. 
Any unauthorized replication and use of any code used 
in any form will be a violation of my exclusive Copyright. 

'''

import argparse
import os
from pathlib import Path
import sys
import librosa
import numpy as np
import soundfile as sf
import torch
from voice_production.encoder import inference as encoder
from voice_production.encoder.params_model import model_embedding_size as speaker_embedding_size
from voice_production.synthesizer.inference import Synthesizer
from voice_production.utils.argutils import print_args
from voice_production.utils.default_models import ensure_default_models
from voice_production.vocoder import inference as vocoder

from django.core.management.base import BaseCommand, CommandError

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


class audio_synthesis(BaseCommand):

    def __init__(self):
        pass

    def pre_req(self):

        parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)

        
        parser.add_argument("-e", "--enc_model_fpath", type=Path,
                            default="voice_production/saved_models/default/encoder.pt",
                            help="Path to a saved encoder")
        parser.add_argument("-s", "--syn_model_fpath", type=Path,
                            default="voice_production/saved_models/default/synthesizer.pt",
                            help="Path to a saved synthesizer")
        parser.add_argument("-v", "--voc_model_fpath", type=Path,
                            default="voice_production/saved_models/default/vocoder.pt",
                            help="Path to a saved vocoder")


        parser.add_argument("--cpu", action="store_true", help= \
            "If True, processing is done on CPU, even when a GPU is available.")
        parser.add_argument("--no_sound", action="store_true", help= \
            "If True, audio won't be played.")

        parser.add_argument("--seed", type=int, default=None, help= \
            "Optional random number seed value to make toolbox deterministic.")
        # parser.add_argument('-f')


        # args = parser.parse_args()

        args, unknown = parser.parse_known_args()


        arg_dict = vars(args)
        print_args(args, parser)

        if arg_dict.pop("cpu"):
            os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

        print("Running a test of your configuration...\n")

        if torch.cuda.is_available():
            device_id = torch.cuda.current_device()
            gpu_properties = torch.cuda.get_device_properties(device_id)
            ## Print some environment information (for debugging purposes)
            print("Found %d GPUs available. Using GPU %d (%s) of compute capability %d.%d with "
                  "%.1fGb total memory.\n" %
                  (torch.cuda.device_count(),
                   device_id,
                   gpu_properties.name,
                   gpu_properties.major,
                   gpu_properties.minor,
                   gpu_properties.total_memory / 1e9))
        else:
            print("Using CPU for inference.\n")

        ## Load the models one by one.
        print("Preparing the encoder, the synthesizer and the vocoder...")
        #ensure_default_models(Path("saved_models"))
        #ensure_default_models(Path("C:\\Users\\Owner\\Desktop\\voice_synthesis\\saved_models"))

        '''
        fix default models
        '''

        #ensure_default_models(Path("C:\\Users\\Owner\\Desktop\\webdevelopment\\vo_prod2\\saved_models"))

        # ensure_default_models(Path("C:\\Users\\Owner\\Desktop\\web_dev_11\\vo_prod2\\saved_models"))

        '''
        Model issues, create web_app_dev_4
        '''



        # ensure_default_models(Path(os.getcwd() + "\\voice_production\\saved_models"))

        # os.path.join(BASE_DIR, "sangenius_complete\\gs\\gs10.00.0\\bin\\gswin64c.exe")

        ensure_default_models(Path(os.path.join(BASE_DIR, "voice_production\\saved_models")))

        encoder.load_model(args.enc_model_fpath)
        synthesizer = Synthesizer(args.syn_model_fpath)
        vocoder.load_model(args.voc_model_fpath)


        ## Run a test
        print("Testing your configuration with small inputs.")
        print("\tTesting the encoder...")
        encoder.embed_utterance(np.zeros(encoder.sampling_rate))
        embed = np.random.rand(speaker_embedding_size)
        embed /= np.linalg.norm(embed)
        embeds = [embed, np.zeros(speaker_embedding_size)]
        texts = ["test 1", "test 2"]
        print("\tTesting the synthesizer... (loading the model will output a lot of text)")
        mels = synthesizer.synthesize_spectrograms(texts, embeds)
        mel = np.concatenate(mels, axis=1)


        no_action = lambda *args: None
        print("\tTesting the vocoder...")
        vocoder.infer_waveform(mel, target=200, overlap=50, progress_callback=no_action)

        print("All test passed! You can now synthesize speech.\n\n")

        return args, synthesizer


class voice_synthesis(object):

    def __init__(self, audio_file_path, filename, input_text):

        self.audio_file_path = audio_file_path
        self.filename = filename
        self.input_text = input_text

        '''
        Loads model
        '''

        self.args,self.synthesizer = audio_synthesis().pre_req()



    def voice_synthetic_text(self):

        synthesizer = self.synthesizer
        args = self.args
        in_fpath = self.audio_file_path

        print(in_fpath)
        preprocessed_wav = encoder.preprocess_wav(in_fpath)
        original_wav, sampling_rate = librosa.load(str(in_fpath))
        preprocessed_wav = encoder.preprocess_wav(original_wav, sampling_rate)
        print("Loaded file succesfully")
        embed = encoder.embed_utterance(preprocessed_wav)
        print("Created the embedding")
        text = self.input_text
        if args.seed is not None:
            torch.manual_seed(args.seed)
            synthesizer = Synthesizer(args.syn_model_fpath)
        texts = [text]
        embeds = [embed]
        specs = synthesizer.synthesize_spectrograms(texts, embeds)
        spec = specs[0]
        print("Created the mel spectrogram")
        print("Synthesizing the waveform:")
        if args.seed is not None:
            torch.manual_seed(args.seed)
            vocoder.load_model(args.voc_model_fpath)
        generated_wav = vocoder.infer_waveform(spec)
        generated_wav = np.pad(generated_wav, (0, synthesizer.sample_rate), mode="constant")
        generated_wav = encoder.preprocess_wav(generated_wav)

        '''sound argument'''

        print(args.no_sound)

        args.no_sound = True

        if not args.no_sound:
            import sounddevice as sd
            try:
                sd.stop()
                sd.play(generated_wav, synthesizer.sample_rate)
            except sd.PortAudioError as e:
                print("\nCaught exception: %s" % repr(e))
                print("Continuing without audio playback. Suppress this message with the \"--no_sound\" flag.\n")
            except:
                raise

        # print(generated_wav.dtype)
        sf.write(self.filename, generated_wav.astype(np.float32), synthesizer.sample_rate)
        return



