#@title <-- Just run the cell (config edge TTS)
edge_folder="."
import nltk
nltk.download('punkt')
from nltk.tokenize import sent_tokenize

from deep_translator import GoogleTranslator

from lang_data import languages,male_voice_list,female_voice_list

def translate_text(text, Language):
    # print("calling translate")
    target_language=languages[Language]
    if Language == "Chinese":
          target_language='zh-CN'
    translator = GoogleTranslator(target=target_language)
    translation = translator.translate(text.strip())
    t_text=str(translation)
    # print(f"{t_text}---{Language}----{target_language}")
    return t_text


def chunks_sentences(paragraph, join_limit=2):
    sentences = sent_tokenize(paragraph)
    # Initialize an empty list to store the new sentences
    new_sentences = []

    # Iterate through the list of sentences in steps of 'join_limit'
    for i in range(0, len(sentences), join_limit):
        # Join the sentences with a space between them
        new_sentence = ' '.join(sentences[i:i + join_limit])
        new_sentences.append(new_sentence)
    return new_sentences


def calculate_rate_string(input_value):
    rate = (input_value - 1) * 100
    sign = '+' if input_value >= 1 else '-'
    return f"{sign}{abs(int(rate))}"


def make_chunks(input_text, language):
    language="English"
    if language == "English":
      filtered_list=chunks_sentences(input_text, join_limit=2)
      # temp_list = input_text.strip().split(".")
      # filtered_list = [element.strip() + '.' for element in temp_list[:-1] if element.strip() and element.strip() != "'" and element.strip() != '"']
      # if temp_list[-1].strip():
      #     filtered_list.append(temp_list[-1].strip())
      return filtered_list




import re
import uuid
def tts_file_name(text):
    if text.endswith("."):
        text = text[:-1]
    text = text.lower()
    text = text.strip()
    text = text.replace(" ","_")
    truncated_text = text[:25] if len(text) > 25 else text if len(text) > 0 else "empty"
    random_string = uuid.uuid4().hex[:8].upper()
    file_name = f"{edge_folder}/edge_tts_voice/{truncated_text}_{random_string}.mp3"
    return file_name


from pydub import AudioSegment
import shutil
import os
def merge_audio_files(audio_paths, output_path):
    # Initialize an empty AudioSegment
    merged_audio = AudioSegment.silent(duration=0)

    # Iterate through each audio file path
    for audio_path in audio_paths:
        # Load the audio file using Pydub
        audio = AudioSegment.from_file(audio_path)

        # Append the current audio file to the merged_audio
        merged_audio += audio

    # Export the merged audio to the specified output path
    merged_audio.export(output_path, format="mp3")

def edge_free_tts(chunks_list,speed,voice_name,save_path,translate_text_flag,Language):
  # print(voice_name)
  # print(chunks_list)
  store_text=""
  if len(chunks_list)>1:
    chunk_audio_list=[]
    if os.path.exists(f"{edge_folder}/edge_tts_voice"):
      shutil.rmtree(f"{edge_folder}/edge_tts_voice")
    os.mkdir(f"{edge_folder}/edge_tts_voice")
    k=1
    for i in chunks_list:
      # print(i)
      if translate_text_flag:
        text=translate_text(i, Language)
      else:
        text=i
      store_text+=text+" "
      text=text.replace('"',"")
      edge_command=f'edge-tts  --rate={calculate_rate_string(speed)}% --voice {voice_name} --text "{text}" --write-media {edge_folder}/edge_tts_voice/{k}.mp3'
      var1=os.system(edge_command)
      if var1==0:
        pass
      else:
        print(f"Failed: {i}")
        print(edge_command)
      chunk_audio_list.append(f"{edge_folder}/edge_tts_voice/{k}.mp3")
      k+=1
    # print(chunk_audio_list)
    merge_audio_files(chunk_audio_list, save_path)
  else:
    if translate_text_flag:
      text=translate_text(chunks_list[0], Language)
    else:
      text=chunks_list[0]
    text=text.replace('"',"")
    store_text+=text+" "
    edge_command=f'edge-tts  --rate={calculate_rate_string(speed)}% --voice {voice_name} --text "{text}" --write-media {save_path}'
    var2=os.system(edge_command)
    if var2==0:
      pass
    else:
      print(f"Failed: {chunks_list[0]}")
      print(edge_command)
  with open("./temp.txt", "w", encoding="utf-8") as text_file:
    text_file.write(store_text)
  return save_path


# speed = 1  # @param {type: "number"}
# translate_text_flag  = True # @param {type:"boolean"}
# long_sentence = True # @param {type:"boolean"}








# from IPython.display import clear_output
# from IPython.display import Audio
if not os.path.exists(f"{edge_folder}/audio"):
    os.mkdir(f"{edge_folder}/audio")
import uuid
def random_audio_name_generate():
  random_uuid = uuid.uuid4()
  audio_extension = ".mp3"
  random_audio_name = str(random_uuid)[:8] + audio_extension
  return random_audio_name
def edge_tts_pipeline(input_text,Language='English',voice_name=None,Gender='Male',translate_text_flag=True,no_silence=False,speed=1,tts_save_path="",long_sentence=True):
  # print("calling gradio_talk")
  # global long_sentence,translate_text_flag,Language,speed,voice_name,Gender
  global male_voice_list,female_voice_list
  # long_sentence=True
  # translate_text_flag=True
  # speed=1
  if long_sentence==False:
    if len(input_text)>500:
      long_sentence=True
  if voice_name==None:
    if Gender=="Male":
      voice_name=male_voice_list[Language]
    if Gender=="Female":
      voice_name=female_voice_list[Language]
  if long_sentence==True and translate_text_flag==True:
    chunks_list=make_chunks(input_text,Language)
  elif long_sentence==True and translate_text_flag==False:
    chunks_list=make_chunks(input_text,"English")
  else:
    chunks_list=[input_text]
  temp_save_path=f"{edge_folder}/audio/"+random_audio_name_generate()
  save_path=temp_save_path.lower().replace(".mp3",".wav")
  # print(chunks_list,speed,voice_name,save_path,translate_text_flag,Language)
  edge_save_path=edge_free_tts(chunks_list,speed,voice_name,temp_save_path,translate_text_flag,Language)
  mp3_to_wav(edge_save_path, save_path)
  audio_return_path=save_path
  if no_silence:
    clean_path=f"{edge_folder}/audio/"+random_audio_name_generate().replace(".mp3",".wav")
    remove_silence(save_path,clean_path)
    audio_return_path=clean_path
    # return clean_path
  if tts_save_path=="":
    return audio_return_path
  else:
    shutil.copyfile(audio_return_path,tts_save_path)
    return audio_return_path



def talk(input_text):
  # global long_sentence,translate_text_flag,Language,speed,voice_name,Gender
  global Language, Gender,male_voice_list,female_voice_list
  global no_silence
  long_sentence=True
  translate_text_flag=False
  speed=1

  if Gender=="Male":
    voice_name=male_voice_list[Language]
  if Gender=="Female":
    voice_name=female_voice_list[Language]
  if long_sentence==True and translate_text_flag==True:
    chunks_list=make_chunks(input_text,Language)
  elif long_sentence==True and translate_text_flag==False:
    chunks_list=make_chunks(input_text,"English")
  else:
    chunks_list=[input_text]
  
  temp_save_path=f"{edge_folder}/audio/"+random_audio_name_generate()
  # print(f"temp_save_path: {temp_save_path}")
  save_path=temp_save_path.replace(".mp3",".wav")
  # print(f"save_path: {save_path}")
  edge_save_path=edge_free_tts(chunks_list,speed,voice_name,temp_save_path,translate_text_flag,Language)
  
  mp3_to_wav(edge_save_path, save_path)
  if no_silence:
    clean_path=f"{edge_folder}/audio/"+random_audio_name_generate().replace(".mp3",".wav")
    remove_silence(save_path,clean_path)
    return clean_path
  return save_path

from pydub import AudioSegment
from pydub.silence import split_on_silence
import os
 
def remove_silence(file_path,output_path):
    # Extract file name and format from the provided path
    file_name = os.path.basename(file_path)
    audio_format = "wav"

    # Reading and splitting the audio file into chunks
    sound = AudioSegment.from_file(file_path, format=audio_format)
    audio_chunks = split_on_silence(sound,
                                    min_silence_len=100,
                                    silence_thresh=-45,
                                    keep_silence=50)

    # Putting the file back together
    combined = AudioSegment.empty()
    for chunk in audio_chunks:
        combined += chunk


    combined.export(output_path, format=audio_format)
    print(f"Remove silence successfully: {output_path}")

    return output_path


from pydub import AudioSegment

def mp3_to_wav(mp3_file, wav_file):
    # Load the MP3 file
    # print("calling mp3_to_wav")
    # print(mp3_file,wav_file)
    audio = AudioSegment.from_mp3(mp3_file)

    # Export the audio to WAV format
    audio.export(wav_file, format="wav")


###use case

# from microsoft_tts import edge_tts_pipeline
# def tts(text, Language='English',voice_name=None, tts_save_path='', Gender='Male', translate_text_flag=False, no_silence=True, speed=1.0, long_sentence=True):          
#     edge_save_path = edge_tts_pipeline(text, Language,voice_name, Gender, translate_text_flag=translate_text_flag, 
#                                         no_silence=no_silence, speed=speed, tts_save_path=tts_save_path, 
#                                         long_sentence=long_sentence)
#     return edge_save_path

# text="Machine learning is the study of computer algorithms that improve automatically through experience. It is seen as a subset of artificial intelligence. Machine learning algorithms build a model based on sample data, known as training data, in order to make predictions or decisions without being explicitly programmed to do so. Machine learning algorithms are used in a wide variety of applications, such as email filtering and computer vision, where it is difficult or infeasible to develop conventional algorithms to perform the needed tasks."
# save_path = tts(text, Language='English',Gender="Male")
# print(save_path)
# import simpleaudio as sa
# def play_sound(filename):
#     wave_obj = sa.WaveObject.from_wave_file(filename)
#     play_obj = wave_obj.play()
#     play_obj.wait_done()
# play_sound(save_path)



























# edge_save_path=talk(text)
# print(f"Audio File Save at: {edge_save_path}")

# text = "a quick brown fox jumps over the lazy dog and the dog barks loudly"
# Language = "English" # @param ['English','Hindi','Bengali','Afrikaans', 'Amharic', 'Arabic', 'Azerbaijani', 'Bulgarian', 'Bosnian', 'Catalan', 'Czech', 'Welsh', 'Danish', 'German', 'Greek', 'Spanish', 'French', 'Irish', 'Galician', 'Gujarati', 'Hebrew', 'Croatian', 'Hungarian', 'Indonesian', 'Icelandic', 'Italian', 'Japanese', 'Javanese', 'Georgian', 'Kazakh', 'Khmer', 'Kannada', 'Korean', 'Lao', 'Lithuanian', 'Latvian', 'Macedonian', 'Malayalam', 'Mongolian', 'Marathi', 'Malay', 'Maltese', 'Burmese', 'Norwegian Bokmål', 'Nepali', 'Dutch', 'Polish', 'Pashto', 'Portuguese', 'Romanian', 'Russian', 'Sinhala', 'Slovak', 'Slovenian', 'Somali', 'Albanian', 'Serbian', 'Sundanese', 'Swedish', 'Swahili', 'Tamil', 'Telugu', 'Thai', 'Turkish', 'Ukrainian', 'Urdu', 'Uzbek', 'Vietnamese', 'Chinese', 'Zulu']
# no_silence = False
# Gender = "Male"# @param ['Male', 'Female']
# translate_text_flag=True
# no_silence=True
# speed=1
# tts_save_path='temp.wav'
# edge_save_path=edge_tts_pipeline(text,Language,Gender,translate_text_flag=translate_text_flag,no_silence=no_silence,speed=speed,tts_save_path=tts_save_path)
# print(f"Audio File Save at: {edge_save_path}")

# from microsoft_tts import edge_tts_pipeline
# def tts(text,tts_save_path=''):
#     # text = "a quick brown fox jumps over the lazy dog and the dog barks loudly"
#     Language = "English" # @param ['English','Hindi','Bengali','Afrikaans', 'Amharic', 'Arabic', 'Azerbaijani', 'Bulgarian', 'Bosnian', 'Catalan', 'Czech', 'Welsh', 'Danish', 'German', 'Greek', 'Spanish', 'French', 'Irish', 'Galician', 'Gujarati', 'Hebrew', 'Croatian', 'Hungarian', 'Indonesian', 'Icelandic', 'Italian', 'Japanese', 'Javanese', 'Georgian', 'Kazakh', 'Khmer', 'Kannada', 'Korean', 'Lao', 'Lithuanian', 'Latvian', 'Macedonian', 'Malayalam', 'Mongolian', 'Marathi', 'Malay', 'Maltese', 'Burmese', 'Norwegian Bokmål', 'Nepali', 'Dutch', 'Polish', 'Pashto', 'Portuguese', 'Romanian', 'Russian', 'Sinhala', 'Slovak', 'Slovenian', 'Somali', 'Albanian', 'Serbian', 'Sundanese', 'Swedish', 'Swahili', 'Tamil', 'Telugu', 'Thai', 'Turkish', 'Ukrainian', 'Urdu', 'Uzbek', 'Vietnamese', 'Chinese', 'Zulu']
#     no_silence = False
#     Gender = "Male"# @param ['Male', 'Female']
#     translate_text_flag=True
#     no_silence=True
#     speed=1
#     # tts_save_path='temp.wav'
#     long_sentence=True
#     edge_save_path=edge_tts_pipeline(text,Language,Gender,translate_text_flag=translate_text_flag,no_silence=no_silence,speed=speed,tts_save_path=tts_save_path,long_sentence=long_sentence)
#     print(f"Audio File Save at: {edge_save_path}")
#     return edge_save_path
