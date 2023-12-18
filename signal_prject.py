import tkinter
from tkinter import *
import wave
import numpy as np
import sys
import matplotlib.pyplot as plt
from pydub import AudioSegment
import simpleaudio as sa

# start window
window1 = Tk()
window1.title("Signal Processing")
window1.configure(width=500, height=500)
window1.configure(background='#371B58')
t = Label(window1, text="Signal Processing", font=(
    "Bradley Hand ITC", 40, "bold"), fg="White", bg="#371B58")
t.place(x=35, y=30)
window1.resizable(0,0)

# icon1
window1.iconbitmap('icon.ico')

# photo1
aa = PhotoImage(file='photo.PNG')
img = Label(window1, image=aa)
img.place(x=120, y=110)
img.configure(background='#371B58')

def start():
    # program window
    window1.destroy()
    window = Tk()
    window.title("Signal Processing")
    window.configure(width=550, height=570)
    window.configure(bg="#4C3575")
    t = Label(window, text="Signal Processing", font=(
        "Bradley Hand ITC", 40, "bold"), fg="White", bg="#4C3575")
    t.place(x=55, y=30)
    window.resizable(0,0)
    # icon
    window.iconbitmap('icon.ico')

    # compres label
    a = Label(window, text="Enter The Time Scale Value", bg="#4C3575",
              font=('Bradley Hand ITC', 18, 'bold'), fg="white")
    a.place(x=30, y=190)
    # shift label
    a = Label(window, text="Enter The Shift Value", bg="#4C3575",
              font=('Bradley Hand ITC', 18, 'bold'), fg="white")
    a.place(x=30, y=130)
    # compres command

    def click():
        x = DoubleVar()
        if ce.get() == 0:
            x = 1
        else:
            x = (ce.get())
        comp_exp(x)

    # Oreginal Wave command
    def org():
        orgwave()

    # opening the wav file
    def open_audfile(name):
        wav = wave.open(name, "r")
        global raw, Time, time
        raw = wav.readframes(-1)
        raw = np.frombuffer(raw, dtype='int16')
        if wav.getnchannels() == 2:
            print("Can not run!")
            sys.exit(0)
        sampleRate = wav.getframerate()
        time = len(raw)/sampleRate
        Time = np.linspace(0, time, num=len(raw))

    # prepare the function axis
    def plotting(Time, raw):
        a = plt.subplot()
        plt.title("Waveform")
        a.set(xlabel='Time (sec)', ylabel='Amplitude')
        plt.plot(Time, raw, color="blue")
        plt.show()

    # original function
    def orgwave():
        open_audfile("signal.wav")
        plotting(Time, raw)

    # Time shifting function
    def shift(pn):
        shift = AudioSegment.from_file(file="signal.wav", format="wav")
        AudioSegment.converter = "ffmpeg.exe"
        AudioSegment.ffmpeg = "ffmpeg.exe"
        AudioSegment.ffprobe = "ffprobe.exe"
        if pn > 0:
            StartSec = pn
            open_audfile('signal.wav')
            EndSec = time
            StartTime = StartSec * 1000
            EndTime = EndSec * 1000
            shift = shift[StartTime: EndTime]
        else:
            pn = -pn
            shifting = AudioSegment.silent(duration=pn*1000)
            shift = shifting+shift
        shift.export('modified_signal.wav', format='wav')

    # Time scale function
    def comp_exp(ce):
        x = AudioSegment.from_file(file="modified_signal.wav", format="wav")
        x = x._spawn(x.raw_data, overrides={
                     "frame_rate": int(x.frame_rate * ce)})
        x.export(out_f="modified_signal.wav", format="wav")

    # Time reverse function
    def Revfun():
        Rev = AudioSegment.from_file(file="modified_signal.wav", format="wav")
        Rev = Rev.reverse()
        Rev.export(out_f="modified_signal.wav", format="wav")

    #play the audio
    def play():
        name1='signal.wav'
        wav = sa.WaveObject.from_wave_file(name1)
        wav.play()

    # compres entry
    ce = DoubleVar()
    e2 = Entry(window, font=25, width=15, textvariable=ce)
    e2.place(x=350, y=190)

    # shift entry
    pn = DoubleVar()
    e1 = Entry(window, font=25, width=15, textvariable=pn)
    e1.place(x=350, y=130)

    # reverse radio button
    module = StringVar()
    r1 = Radiobutton(window, text='ON', value='on', variable=module,
                     bg="#4C3575", font=('Bradley Hand ITC', 14, 'bold'))
    r1.place(x=350, y=250)
    r2 = Radiobutton(window, text='OFF', value='off', variable=module,
                     bg="#4C3575", font=('Bradley Hand ITC', 14, 'bold'))
    r2.place(x=420, y=250)
    a = Label(window, text="Reverse", bg="#4C3575", font=(
        'Bradley Hand ITC', 18, 'bold'), fg="white")
    a.place(x=30, y=250)

    # original button
    p1 = Button(window, text="Original Wave", command=org, bg="#5B4B8A", font=(
        'Bradley Hand ITC', 18, 'bold'), fg="white", width=13)
    p1.place(x=42, y=350)

    #original sound
    s = Button(window, text="Original Sound", command=play, bg="#5B4B8A", font=(
        'Bradley Hand ITC', 18, 'bold'), fg="white", width=13)
    s.place(x=42, y=420)

    # Modified wave command
    def select():
        if module.get() == 'on':
            shift(pn.get())
            click()
            Revfun()
        else:
            shift(pn.get())
            click()
        open_audfile("modified_signal.wav")
        plotting(Time, raw)

    def play1():
        name2='modified_signal.wav'
        wav2 = sa.WaveObject.from_wave_file(name2)
        wav2.play()

    # Modified Wave button
    p = Button(window, text="Modified Wave", command=select, bg="#5B4B8A", font=(
        'Bradley Hand ITC', 18, 'bold'), fg="white", width=13)
    p.place(x=300, y=350)

    # Modified sound button
    ms = Button(window, text="Modified Sound", command=play1, bg="#5B4B8A", font=(
        'Bradley Hand ITC', 18, 'bold'), fg="white", width=13)
    ms.place(x=300, y=420)

    # exit button
    a = Button(window, text="Exit Now", command=window.quit, bg="#5B4B8A", font=(
        'Bradley Hand ITC', 18, 'bold'), fg="white", width=15)
    a.place(x=157, y=490)

    window.mainloop()

# start button
a = Button(window1, text="Get Start", command=start, bg="#4C3575",
           font=('Bradley Hand ITC', 18, 'bold'), fg="white", width=15)
a.place(x=125, y=400)

window1.mainloop()