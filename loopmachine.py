import pyaudio
import wave
import sys
from Tkinter import *

state = "stop"
autoplayafterrec = True
chunk = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 10
WAVE_OUTPUT_FILENAME = "output.wav"

def record(event):
    global data, state
    p = pyaudio.PyAudio()
    print "record pressed"

    # # toggle record state
    # if state == "record":
    #     state = "stop"
    # else:
    #     state = "record"

    if state == "record":
        return
    else:
        state = "record"

    # start recording
    stream = p.open(format = FORMAT,
                    channels = CHANNELS,
                    rate = RATE,
                    input = True,
                    frames_per_buffer = chunk)
    print "* recording"
    all = []

    # for i in range(0, RATE / chunk * RECORD_SECONDS):
    #     data = stream.read(chunk)
    #     all.append(data)
    # print "* done recording"
    # stream.close()
    # p.terminate()

    for i in range(0, RATE / chunk * RECORD_SECONDS):
        data = stream.read(chunk)
        all.append(data)
        frame.update()
        if not(canRec()):
            break
    print "* done recording"   
    stream.stop_stream()
    stream.close()
    p.terminate()

    # write data to WAVE file
    data = ''.join(all)
    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(data)
    wf.close()
    if autoplayafterrec:
        play(event)

def play(event):
    global data, state
    state = "play"
    while canPlay():
        print "playing"
        p = pyaudio.PyAudio()
        wf = wave.open(WAVE_OUTPUT_FILENAME, 'rb')
        # open stream for wav file playback
        stream = p.open(format =
                    p.get_format_from_width(wf.getsampwidth()),
                    channels = wf.getnchannels(),
                    rate = wf.getframerate(),
                    output = True)
        # read data from wav file
        data = wf.readframes(chunk)
        # play stream from wav file
        while data != '' and canPlay():
            stream.write(data)
            data = wf.readframes(chunk)
            frame.update()
        stream.close()
        p.terminate()

def canRec():
    global state
    return state == "record"

def canPlay():
    global state
    return state == "play"
 
def stop(event):
    global state
    print "stop pressed"
    state = "stop"

def quit(event):
    print "quitting"
    root.quit()

root = Tk()
frame = Frame(root, width=683, height=768, bg="black")
frame.bind("<space>", record)
frame.bind("p", play)
frame.bind("s", stop)
frame.bind("q", quit)
frame.pack()
frame.focus_set()
Label(frame, fg="white", bg="black", width=24, height=8, anchor=CENTER, font=("monaco", 42), text="Loop Machine").pack()
Label(frame, fg="white", bg="black", width=24, height=8, anchor=CENTER, font=("monaco", 20), text="space - Record\np - Play loop\ns - Stop\nq - Quit").pack()
root.mainloop()