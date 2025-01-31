#for voice Recognition
import os
import time
import socket
import pyttsx3
import threading
import webbrowser

# importing libraries for speech recognition
from pocketsphinx import LiveSpeech, DefaultConfig, Decoder, get_model_path, get_data_path
import speech_recognition as sr
import re

#for ui
from tkinter import *
from tkinter import filedialog
from tkinter import font
from PIL import Image, ImageTk
from tkinter.filedialog import askopenfilename, asksaveasfilename


#importing libraries for audio processing
from pydub import AudioSegment
from pydub.silence import split_on_silence
from pydub.playback import play


# object creation
engine = pyttsx3.init()

# getting details of current speaking rate
rate = engine.getProperty('rate')
print("speaking rate: ", rate)

# setting up new voice rate
engine.setProperty('rate', 100)

#getting to know current volume level (min=0 and max=1)
volume = engine.getProperty('volume')
print("volume: ", volume)

# setting up volume level  between 0 and 1
engine.setProperty('volume',1.0)

#getting details of current voice
voices = engine.getProperty('voices')

#changing index, changes voices. o for male
#engine.setProperty('voice', voices[0].id)

#changing index, changes voices. 1 for female
engine.setProperty('voice', voices[22].id)


# setting up custom configuration
config = DefaultConfig()
config.set_string('-hmm', os.path.join('./', 'hindi'))
config.set_string('-lm', os.path.join('./', 'hindi_en.lm.bin'))
config.set_string('-dict', os.path.join('./', 'hindi_en.dic'))
decoder = Decoder(config)

# Decoding streaming data
buf = bytearray(4096)

root = Tk()
root.title("Sarthi AMA's Virtual Assistant")
root.geometry('900x500')


# set variable for open filename
global open_status_name
open_status_name = False

# initial audio curser position after breaking up sound, on occurance of silance
global slice_position
slice_position = 0

# transcription
global transcriptions
transcriptions = []

# create new file function
def new_file():
    #delete previus text
    transcipted_text.delete("1.0", END)
    global open_status_name
    open_status_name = False

def open_file():
    #delete previus text
    transcipted_text.delete("1.0", END)

    #grab filename
    text_file = filedialog.askopenfilename(initialdir='', title="Open File", filetypes=(("Text Files", "*.txt"), ("HTML Files", "*.html"), ("Python Files", "*.y"), ("All Files", "*.*")))

    #check if file is selected i.e. not null
    if text_file:
        #make filename global so we can access it later
        global open_status_name
        open_status_name = text_file

    #open fileids
    text_file = open(text_file, 'r')
    stuff = text_file.read()
    #add file to text file
    transcipted_text.insert(END, stuff)
    #close the text file
    text_file.close()

def save_as_file():

    global text_file
    text_file = asksaveasfilename(filetypes=(("Text Files", "*.txt"), ("HTML Files", ".html"), ("Python Files", "*.py"), ("All Files", "*.*")))
    print("text_file: ", text_file)

    open_status_name = text_file
    f = open(text_file, 'w')
    f.write(transcipted_text.get(1.0, END))
    f.close()

#save file
def save_file():
    global open_status_name
    # open_status_name = text_file
    if open_status_name:

        f = open(open_status_name, 'w')
        f.write(transcipted_text.get(1.0, END))

        #close the file
        f.close()
    else:
        save_as_file()

#sarthi's functions
class Sarthi(object):
    # def __init__(self):
        # self.sarthi
    def sarthi_tts(self, transcipted_text):
        engine.say(transcipted_text)
        engine.runAndWait()
        engine.stop()

    def test_connection(self):
       try:
           socket.create_connection(('google.com',80))
           return True

       except socket.timeout:
           return False
       except OSError:
           return False



    def sarthi_stt(self):
        r = sr.Recognizer()

        if self.test_connection()==True:
        # if False:
            print("get set speak")
            with sr.Microphone() as source:
                r.adjust_for_ambient_noise(source)
                self.sarthi_tts("Google A S R activated")

		# use the default microphone as the audio source
                self.sarthi_tts("you can speek now)

		# listen for the first phrase and extract it into audio data
                audio = r.listen(source)

            try:
                sarthi_tts("processing your voice..")
                self.x=r.recognize_google(audio)
                print("by google command: ", self.x)

		# recognize speech using Google Speech Recognition
                return self.x

	    # speech is unintelligible
            except Exception:
		sarthi_tts("Could not understand audio")
                print("Could not understand audio")
                return 0
        else:
            print("no  internet connection ")
            print("Offline so result maybe inaccurate")
            print("now speek")
            self.sarthi_tts("pocket sphinx activated")
            self.sarthi_tts("you can speek now")
            self.model_path = get_model_path()
            speech = LiveSpeech(
            verbose=False,
            sampling_rate=16000,
            buffer_size=2048,
            no_search=False,
            full_utt=False,
	    hmm=os.path.join(self.model_path, 'hindi'),
            lm=os.path.join(self.model_path, 'hindi_en.lm.bin'),
            dic=os.path.join(self.model_path, 'hindi_en.dic')
            )
            self.x=''
            count = 0
            for phrase in speech:
                self.x=self.x+str(phrase)
                count = count + 1
                if(count == 2):
                    break
            print("you speak by phonix: ", self.x)
            return (self.x)

    def sarthi_openatom(self):
        # self.command = "atom"
        self.sarthi_tts("opening atom")
        os.system(f"atom")
    def sarthi_chrome(self):
        # self.command = "google-chrome"
        self.sarthi_tts("opening google chrome")
        os.system(f"google-chrome")

    def sarthi_youtube(self):
        self.sarthi_tts("opening youtube")
        self.url = 'https://www.youtube.com/'
        webbrowser.open(self.url, new=2)

    def sarthi_facebook(self):
        self.sarthi_tts("opening facebook")
        self.url = 'https://www.facebook.com/'
        webbrowser.open(self.url, new=2)

    def sarthi_gmail(self):
        self.sarthi_tts("opening gmail")
        self.url = 'https://gmail.com/'
        webbrowser.open(self.url, new=2)


    def sarthi_pwd(self):
        self.cwd=os.getcwd()
        print(str(self.cwd))
        self.sarthi_tts("PRESENT WORKING DIRECTORY is "+str(self.cwd))


    # def sarthi_websearch(keyword):
    def sarthi_websearch(self):
        # If new is 0, the url is opened in the same browser window if possible.
        # If new is 1, a new browser window is opened if possible.
        # If new is 2, a new browser page (“tab”) is opened if possible
        self.url = 'https://www.google.com'
        webbrowser.open('https://www.google.com', new=2)

    #main_function
    def sarthi(self):
        self.application_key = 0
        self.command_key = 0
        # self.sarthi_tts("please speek")

        self.x= self.sarthi_stt()
        return self.x

        # =========================only transcribing not performing actions thats why commented======================================
        # if(self.x==0):
        #     self.x = ""
        #     self.sarthi_tts('can not hear you click and please speak again')
        #     return self.x

        # self.x = self.x.lower()
        # if(self.x == "open google chrome"):
        #     self.x = "open google_chrome"

        # print(self.x, " :you says")
        #     # self.sarthi()

        # self.sarthi_dic={
        #     'folder':{
        #         'current':self.sarthi_pwd
        #     },
        #     'web':{
        #         'search':self.sarthi_websearch
        #     },
        #     'open':{
        #         'item':self.sarthi_openatom,
		# 'atom':self.sarthi_openatom,
        #         'google_chrome': self.sarthi_chrome,
        #         'youtube': self.sarthi_youtube,
        #         'facebook': self.sarthi_facebook,
        #         'gmail': self.sarthi_gmail,
        #         # https://pypi.org/project/update-check/
        #         # https://www.w3resource.com/python-exercises/python-basic-exercise-2.php
        #
        #     }
        # }

        # self.words_list=self.x.split(" ")
        # for i in self.words_list:
        #     if i in self.sarthi_dic.keys():
        #         self.application_key=i
        #         self.application_flag=1
        #         break
        #     else:
        #         self.application_flag=0
        #

        # if(self.application_flag != 0):
        #     self.command_flag = 0
        #     self.command_key = 0
        #     print("here")
        #     for i in self.words_list:
        #         if i in self.sarthi_dic[self.application_key].keys():
        #             self.command_flag=1
        #             self.command_key=i
        #             break
        #         else:
        #             self.command_flag=0
        #     if(self.command_flag != 0):
        #         if(self.command_flag ==1 and self.application_flag==1):
        #             print("executing command: ____", self.sarthi_dic[self.application_key][self.command_key])
        #             self.sarthi_dic[self.application_key][self.command_key]()
        #     else:
        #         self.user_info="sorry as of now, we are not providing this service"
        #         # self.sarthi_tts(self.user_info)
        #         print(self.user_info)
        #         self.x = self.user_info + ": " + self.x
        #         # return self.x
        # else:
        #     self.sarthi_tts("cant recognize what you said please click and start again")
        #     print('cant recognize please click and start again')
        #     self.sarthi()

        # print("returning comband from sarthi: ", self.x)
        # return self.x


def give_intro():
    time.sleep(1)
    engine.say('Hi I am your Sarthi please click button to start live transcription')
    engine.runAndWait()
    engine.stop()


global call_sarthi_flag
call_sarthi_flag = 0
def call_sarthi():

    global call_sarthi_flag
    global transcipted_text
    browse_text.set("listening...")
    command = Sarthi()

    give_command = command.sarthi()
    give_command = str(give_command)
    engine.say(give_command)
    engine.runAndWait()
    engine.stop()

    print("given command: ", give_command)
    print("call_sarthi_flag", call_sarthi_flag, "\n\n")

    text_box_texts = transcipted_text.get("1.0",'end-1c')
    print("----------------\n\n",text_box_texts, " in transcipted_text\n\n")

    if( "Transcription will be shown here" in text_box_texts):
        text_box_texts = text_box_texts.replace("Transcription will be shown here", ". ")
        transcipted_text.delete("1.0", END)
        print("scription will be shown here hai --------------------------------------------------------------------")
    text_box_texts = text_box_texts + give_command
    print("text_box_texts: ", text_box_texts)
    transcipted_text.insert(INSERT, text_box_texts)



global flag
flag = 1
global chunk_list
chunk_list = []
global total_chunk
total_chunk = 0
global file_path_name
file_path_name = ""
global chunks
chunks = 0
file_path_name = " "
global transciption_file_path
transciption_file_path = " "

def write_transcription():
    # global transcriptions
    global transciption_file_path
    print("\n\ntransciption_file_path-----------------------------------------------------------------------------------------------------------\n",transciption_file_path)
    global slice_position
    initian_transcription = transcipted_text.get("1.0",'end-1c')

    if(len(transcriptions) != 0):
        if("Transcription will be shown here" not in initian_transcription):
            # if(len(transcriptions) != 0):
                transcriptions[slice_position] ='<s>' + initian_transcription + '</s>'
        f = open(transciption_file_path, "w")
        for t in transcriptions:
            t = t + '\n'
            print(t)
            f.write(t)
        f.close()

def choose_file():
    global slice_position
    global file_path_name
    global total_chunk
    global chunk_list
    global chunks
    global transciption_file_path
    slice_position = 0
    file_path_name = askopenfilename(filetypes =[('Mp3 file', '.mp3'), ('Wav file', '.wav')])
    if(len(file_path_name) == 0):
        file_path_name = ' '
    print("\n\nfilename______: ", file_path_name,"\n\n\n")
    file_path['text'] =  "File: " + file_path_name

    # seperator = '/'
    breaked_file_path = re.split('/', file_path_name)
    print("breaked_file_path: ",breaked_file_path)
    print("breaked_file_path[-1]:  ",breaked_file_path[-1])
    file_extention = re.split('\.',breaked_file_path[-1])
    print("file_extention: ", file_extention)
    wav_file_path_name = ''
    if('wav' in file_extention):

        print("\n\n================= wav file selected =====================\n\n")
        wav_file_path_name = file_path_name
        engine.say('wave file selected   ')
        engine.runAndWait()
        engine.stop()

    else:

        file_extention[-1] = 'wav'
        breaked_file_path[-1] = '.'.join(file_extention)
        wav_file_path_name = '/'.join(breaked_file_path)


        sound =  AudioSegment.from_file(file_path_name, 'mp3')
        sound.export(wav_file_path_name, format="wav")
        print("\n\n================= mp3 file selected =====================\n\n")
        engine.say('mp3 file selected   ')
        engine.runAndWait()
        engine.stop()


    print("\n\n-----------------------------",wav_file_path_name,"\n\n")
    # file_dir =   "26.wav"

    sound = AudioSegment.from_file(wav_file_path_name, "wav")
    # play(sound)
    # root.withdraw()
    chunks = split_on_silence(sound,
        # must be silent for at 100 mili second
        min_silence_len=100,
        # consider it silent if quieter than -40 dBFS
        silence_thresh=-40
     )
    total_chunk = len(chunks)
    print("\n\ntotal no of chunks ", len(chunks), type(chunks))

    chunk_list = []
    for i, chunk in enumerate(chunks):
        print("==================================================================================================================================")
        chunk.export("files/chunk{0}.wav".format(i), format="wav")
        # play(chunk)
        # print("chunk ", i, ": ", len(chunk), "ms", " typw: ",type(chunk))
        chunk_list.append("files/chunk"+str(i)+".wav")
        print("==================================================================================================================================")
    print("\n\nchunk_list: ", chunk_list)
    print("\n\n")

    # play(AudioSegment.from_file('./files/choose_file_hindi.mp3', "mp3"))
    # engine.say("After choosing the files, it have break on each silences")
    # engine.runAndWait()
    # engine.stop()


    #transcribing and storing each chunks in a list
    # print("file_extention: ", file_extention)
    temp1 = re.split('.wav', wav_file_path_name)
    print("temp1: ", temp1)

    transciption_file_path = temp1[0] + '.txt'
    print("------------------------------------------------------------------------------------------------------------------")
    print("transciption_file_path", "\n\n",transciption_file_path)
    print("------------------------------------------------------------------------------------------------------------------")
    engine.say("            wait for next instructions     ")
    engine.runAndWait()
    engine.stop()

    if os.path.exists(transciption_file_path):
        global transcriptions

        #open and read the file after the appending:
        print("file already exists")
        f = open(transciption_file_path, "r")
        sentences = f.read()
        sentences = re.split('\n', sentences)
        print("\n\n-----------file read ----sentences: ", len(sentences), sentences, "---------------------\n\n\n")
        transcriptions = []
        for s in sentences:
            if(s != ''):
                transcriptions.append(s)
            else:
                pass
        print(transcriptions)
        f.close()
    else:
        for i in range(len(chunk_list)):
            prediction = ""
            engine.say("chunks " + str(i))
            engine.runAndWait()
            engine.stop()
            play(AudioSegment.from_file(chunk_list[i], "wav"))

            with open(chunk_list[i], 'rb') as f:
                decoder.start_utt()
                while f.readinto(buf):
                    decoder.process_raw(buf, False, False)
                decoder.end_utt()


            for segment in decoder.seg():
                prediction = prediction + " " + segment.word

            print("\n\nfinal prediction is: ", prediction, "\n")
            transcriptions.insert(i, prediction)
        write_transcription()

    # transcribe(filename)
    engine.say("now you can play each chunks")
    engine.runAndWait()
    engine.stop()
    print(transcriptions, "\n\n===================================================================\n\n\n\n")
    return 0

def play_and_do_transcribe():
    global slice_position
    global total_chunk
    global flag
    global chunks
    print("---------------------------slice_position: ", slice_position,"----------------------------------------")
    global file_path_name
    global chunk_list
    print("\n\n\n-------------------------chunk_list: ", chunk_list, " total_chunk: " ,total_chunk,"\n\n")
    if(slice_position >= total_chunk):
        slice_position = slice_position -1
        print("\ndo you want to  close playing then enter Y pr y else any Button")

        engine.say("End of the file cross")
        engine.runAndWait()
        engine.stop()
        flag = 0

    elif(slice_position < 0):
        flag = 0
        engine.say("it is already at beginning position")
        engine.runAndWait()
        engine.stop()
        print("\nsorry can't play because curser it at starting point itself: ", slice_position)
        slice_position = slice_position + 1

    if(flag == 1):
        # transcipted_text
        transcipted_text.delete("1.0", END)
        sentence = ''
        if(len(transcriptions)>0):
            sentence = re.split('<s>|</s>', transcriptions[slice_position])
        temp = []
        for s in sentence:
            if(s != ''):
                temp.append(s)
        # sentence = temp

        sentence = " "
        sentence = sentence.join(temp)
        transcipted_text.insert(INSERT, sentence)
        play(chunks[slice_position])


    return 0


def forward_slice():
    global flag
    flag = 1
    global slice_position
    initian_transcription = transcipted_text.get("1.0",'end-1c')
    if(initian_transcription != "Transcription will be shown here"):
        if(len(transcriptions) == 0):
            transcriptions[slice_position].append('<s>' + initian_transcription + '</s>')
        else:
            transcriptions[slice_position] ='<s>' + initian_transcription + '</s>'

    print("\n\n\ntranscipted_text: ",type(transcipted_text))
    print(transcipted_text.get("1.0",'end-1c'), "\n")
    print(" modifed values added : ", transcriptions, "\n\n\n")
    slice_position = slice_position + 1
    play_and_do_transcribe()
    return 0

def backward_slice():
    global flag
    flag = 1
    global slice_position
    initian_transcription = transcipted_text.get("1.0",'end-1c')
    if(initian_transcription != "Transcription will be shown here"):
        if(len(transcriptions) == 0):
            transcriptions[slice_position].append('<s>' + initian_transcription + '</s>')
        else:
            transcriptions[slice_position] ='<s>' + initian_transcription + '</s>'


    print("\n\n\ntranscipted_text: ",type(transcipted_text))
    print(transcipted_text.get("1.0",'end-1c'), "\n")
    print(" modifed values added : ", transcriptions, "\n\n\n")
    slice_position = slice_position - 1
    play_and_do_transcribe()
    return 0

def current_slice():
    global flag
    flag = 1
    global slice_position
    initian_transcription = transcipted_text.get("1.0",'end-1c')
    if(initian_transcription != "Transcription will be shown here"):
        if(len(transcriptions) == 0):
            transcriptions[slice_position].append('<s>' + initian_transcription + '</s>')
        else:
            transcriptions[slice_position] ='<s>' + initian_transcription + '</s>'

    print("\n\n\ntranscipted_text: ",type(transcipted_text))
    print(initian_transcription, "\n")

    print(" modifed values added : ", transcriptions, "\n\n\n")
    play_and_do_transcribe()
    return 0

def exiting_window():
    write_transcription()
    root.quit()

# global live_voice_status, audio_file_status
global live_button_state, mic_state, audio_button_state, choose_n_option_state
global live_voice_btn, audio_file_btn, mic_btn, choose_file_btn, backward_button, current_button, forward_button
live_button_state = "normal"
mic_state = "active"
audio_button_state = "normal"
choose_n_option_state = "normal"


def set_button_Status():
    # global live_button_state, mic_state, audio_button_state, choose_n_option_state
    # global live_voice_btn, audio_file_btn, mic_btn, choose_file_btn, backward_button, current_button, forward_button

    if(live_voice_btn['state'] == "active"):
        live_voice_btn['state'] = 'normal'
        audio_file_btn['state'] = 'normal'
        mic_btn['state'] = 'normal'
        choose_file_btn['state'] = 'disabled'
        backward_button['state'] = 'disabled'
        current_button['state'] = 'disabled'
        forward_button['state'] = 'disabled'
        # forward_button.state = choose_n_option_state
    elif(audio_file_btn['state'] == 'active'):
        live_voice_btn['state'] = 'normal'
        audio_file_btn['state'] = 'normal'
        mic_btn['state'] = 'disabled'
        choose_file_btn['state'] = 'normal'
        backward_button['state'] = 'normal'
        current_button['state'] = 'normal'
        forward_button['state'] = 'normal'
    else:
        print('\n\ndono normal hai--------------------------------\n\n')


#----------------logo and transcription control----------------------


logo_frame = Frame(root)
logo_frame.pack()

live_voice_btn = Button(
                    logo_frame,borderwidth=0, text="Live: " + live_button_state,  command=lambda:set_button_Status(),
                    bg="#0c23a0", fg="white", height=2, width=13,
                    state = live_button_state
                    )
live_voice_btn.grid(row=0, column=0, padx=10)

#----------------- for live audio ----------------------
logo = ImageTk.PhotoImage(Image.open('logo.png').resize((200, 200)))
logo_label = Label(logo_frame, image=logo)
# logo_label.image = logo
# logo_label.pack()
logo_label.grid(row=0, column=1, padx=10)


audio_file_btn = Button(
                    logo_frame,borderwidth=0, text="Audio: "+audio_button_state,  command=lambda:set_button_Status(),
                    bg="#0c23a0", fg="white", height=2, width=13,
                    state = audio_button_state
                    )
audio_file_btn.grid(row=0, column=2, padx=10)




#-------------------command wrapper-----------------------------------------
comand_frame = Frame(root)
comand_frame.pack()

#instructions
instructions = Label(comand_frame, text="click on the button to give a command")
# instructions.pack()
instructions.grid(row=0, column=0, padx=10)

#browse button
browse_text = StringVar()
mic_image = Image.open("_mic.png")
mic_image = mic_image.resize((35, 35), Image.ANTIALIAS)
reset_img = ImageTk.PhotoImage(mic_image)

mic_btn = Button(
                    comand_frame,borderwidth=0, textvariable=browse_text,
                    image=reset_img,  command=lambda:call_sarthi(),
                    bg="#d9d9d9", fg="white", height=45, width=50,
                    state = 'disabled'
                    )

mic_btn.grid(row=1, column=0, padx=10)


#------------------------For audio file ----------------------------------------------

# def open_transcription():
#     choose_file_btn.pack_forget() if choose_file_btn.winfo_manager() else choose_file_btn.pack(after=sent_control, anchor=W, padx=5, pady=10)

choose_img = Image.open("_choose_file.png")
choose_img = choose_img.resize((100, 40), Image.ANTIALIAS)
choose_img = ImageTk.PhotoImage(choose_img)
# , height=45, width=50

choose_file_btn = Button(
                     comand_frame,borderwidth=0, textvariable=browse_text, image=choose_img,
                     command=lambda:choose_file(), font="Raleway", bg="#d9d9d9", fg="white",
                     state = 'disabled'
                     )
choose_file_btn.grid(row=0, column=1, padx=10)

# transcipted_text = Text(my_frame, width = 97, height = 25, font=("Helvetica", 16), selectbackground="Yellow", selectforeground="black", undo=True, yscrollcommand=text_scroll.set, pady=5)
# file_path = Text(comand_frame,width=50,height = 2,  selectbackground="Yellow", selectforeground="black", undo=False, pady=5)
file_path = Label(comand_frame, text="file")
file_path.grid(row=1, column=1, padx=10, )
# file_path.insert(INSERT, "file path: ")
file_path['text'] = 'file path: '

sent_control = Frame(comand_frame)
sent_control.grid(row=2, column=1, padx=30)


backward = ImageTk.PhotoImage(Image.open('_skip-back.png').resize((35, 35)))
current = ImageTk.PhotoImage(Image.open('_play.png').resize((35, 35)))
forward = ImageTk.PhotoImage(Image.open('_skip-forward.png').resize((35, 35)))


# Create Volume Meter
backward_button = Button(
                        sent_control, image=backward, borderwidth=0, textvariable=browse_text,  command=lambda:backward_slice(),
                        font="Raleway", bg="#d9d9d9", fg="white", height=45, width=50,
                        state = 'disabled'
                        )
backward_button.grid(row=0, column=0, padx=0)
backward_button_label = Label(sent_control, text="previus")
backward_button_label.grid(row=1, column=0, padx=0)

current_button = Button(
                        sent_control, image=current, borderwidth=0, textvariable=browse_text,  command=lambda:current_slice(),
                        font="Raleway", bg="#d9d9d9", fg="white", height=45, width=50,
                        state = 'disabled'
                        )
current_button.grid(row=0, column=1, padx=0)
current_button_label = Label(sent_control, text="current")
current_button_label.grid(row=1, column=1, padx=0)

forward_button = Button(
                        sent_control, image=forward, borderwidth=0, textvariable=browse_text,  command=lambda:forward_slice(),
                        font="Raleway", bg="#d9d9d9", fg="white", height=45, width=50,
                        state = 'disabled'
                        )
forward_button.grid(row=0, column=2, padx=0)
forward_button_label = Label(sent_control, text="next")
forward_button_label.grid(row=1, column=2, padx=0)



#create main frame
my_frame = Frame(root)
my_frame.pack(pady = 5)

#create scrollbar for text Box
text_scroll = Scrollbar(my_frame)
text_scroll.pack(side=RIGHT, fill=Y)

#create Text Box
global transcipted_text
transcipted_text = Text(my_frame, width = 97, height = 25, font=("Helvetica", 16), selectbackground="Yellow", selectforeground="black", undo=True, yscrollcommand=text_scroll.set, pady=5)
transcipted_text.pack()
transcipted_text.insert(INSERT, "Transcription will be shown here")


#create menu
my_menu = Menu(root)
root.config(menu=my_menu)

#add file Menu
file_menu=Menu(my_menu, tearoff=False)
my_menu.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="New", command=new_file)
file_menu.add_command(label="Open", command=open_file)
file_menu.add_command(label="Save", command=save_file)
file_menu.add_command(label="Save As", command=save_as_file)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=exiting_window)

#add edit menu
edit_menu=Menu(my_menu, tearoff=False)
my_menu.add_cascade(label="Edit", menu=edit_menu)
edit_menu.add_command(label="Cut")
edit_menu.add_command(label="Copy")
edit_menu.add_command(label="Paste")
edit_menu.add_command(label="Undo")
edit_menu.add_command(label="Redo")


#configure scrollbar
text_scroll.config(command=transcipted_text.yview)


threading.Thread(target = give_intro).start()




#setting up voice command
print("----------------------\n\n",file_path_name,"\n\n")




root.mainloop()
