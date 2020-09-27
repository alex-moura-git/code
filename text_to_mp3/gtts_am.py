#!/usr/bin/env python
# coding: utf-8


""" the code has explanations and tells what is going on
    under the hood. Documented Parts # and quotation marks are ignored by the program
    If you need help let me know
            
    Have fun!! Love you"""

import os


"""Import modules. Packages are essencially code that other people wrote."""

"""This file gtts_am.py is an example of a module.
I separated the code to make it simpler to run what we want wihout risking mess to mess up
the rest of the code. 
it is like this file creates a bunch of recipes that will be implemented elsewhere"""


import os 
"""-os is one of the core modules of python does thing like creating,
deleting, moving and obtaining information of files and direcotries"""



"""-pandas is one of the most used modules of python for data analysis."""
import pandas as pd #again used a nickname



"""This is the core function that connections to Google Cloud Services for 
#and exports a file to the target folder.

# it takes 4 arguments:
# - msg: the text or the ssml to be synthesized (REQUIRED)
# - out_file_name: name of the output mp3 file (REQUIRED)
# - mode: text or sslm - In reality it only checks if it is sslm, if not defauls to text
#       - it is being initialized with None, so it is optional, if not provided it defaults to
#       -which then defaults to text.
# - out_file_path: detaults to None which then will put the file in the same directory of the
#       code you are running"""

def synthesize_text_or_ssml(msg, out_file_name,mode=None,out_file_path=None):
    """Synthesizes speech from the input string of text. 
    Comes straign from the google API.. aka code written by Google
    Since it worked I did not go into details. 
    It should have an explaination in the google documentation"""
    from google.cloud import texttospeech 

    client = texttospeech.TextToSpeechClient()
    out_file_name=out_file_path+'/'+out_file_name+".mp3"
    print(out_file_path)
    
    
    """here I did a if to join the two sets of code into one so
    we could select between text and ssml from the excel file"""
    
    if mode=='ssml':
        input_text = texttospeech.SynthesisInput(ssml=msg)
    else:
        input_text = texttospeech.SynthesisInput(text=msg)

    # Note: the voice can also be specified by name.
    # Names of voices can be retrieved with client.list_voices().
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        name="en-US-Wavenet-F",
        ssml_gender=texttospeech.SsmlVoiceGender.FEMALE,
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        request={"input": input_text, "voice": voice, "audio_config": audio_config}
    )

    # The response's audio_content is binary.
    with open(out_file_name, "wb") as out:
        out.write(response.audio_content)
        print('Audio content written to file '+out_file_name)



def synthesize_from_excel(excel_file_full_path):
    
    out_file_path=os.path.split(excel_file_full_path)[0]    
    input_df=pd.read_excel(excel_file_full_path)
    for i in range(len(input_df)) :
        msg=input_df.loc[i]['msg']
        out_file_name = input_df.loc[i]['out_file_name']
        mode = input_df.loc[i]['mode']
        synthesize_text_or_ssml(msg, out_file_name,mode,out_file_path)
    

"""I kept this fucntion in the modele to allow you to call it directly
  from your code. Just import this module (import gtts_am) and
        call the function directly list_voices()"""
        
        



def list_voices():
    """Lists the available voices."""
    from google.cloud import texttospeech

    client = texttospeech.TextToSpeechClient()

    # Performs the list voices request
    voices = client.list_voices()

    for voice in voices.voices:
        # Display the voice's name. Example: tpc-vocoded
        print(f"Name: {voice.name}")

        # Display the supported language codes for this voice. Example: "en-US"
        for language_code in voice.language_codes:
            print(f"Supported language: {language_code}")

        ssml_gender = texttospeech.SsmlVoiceGender(voice.ssml_gender)

        # Display the SSML Voice Gender
        print(f"SSML Voice Gender: {ssml_gender.name}")

        # Display the natural sample rate hertz for this voice. Example: 24000
        print(f"Natural Sample Rate Hertz: {voice.natural_sample_rate_hertz}\n")



