import pyaudio
import audioop
import wave
import sys
from Tkinter import *

layers = 1
state = "stop"
autoplayafterrec = True
mousecontrol = True
chunk = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 10
# WAVE_OUTPUT_FILENAME1 = "output1.wav"
# WAVE_OUTPUT_FILENAME2 = "output2.wav"

def record(event, layer):
    global data, state, layers
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
    print "* recording layer "+str(layer)
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
    # if layer == 1:
    #     WAVE_OUTPUT_FILENAME = WAVE_OUTPUT_FILENAME1
    # elif layer == 2:
    #     WAVE_OUTPUT_FILENAME = WAVE_OUTPUT_FILENAME2
    #     layers = layer

    if layer > layers:
        layers = layer

    data = ''.join(all)
    # wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf = wave.open("output"+str(layer)+".wav", 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(data)
    wf.close()

    state = "stop"
    if autoplayafterrec:
        play(event)

def play(event):
    global data, state, layers
    state = "play"
    while canPlay():
        print "playing"
        p = pyaudio.PyAudio()

        # wf = wave.open(WAVE_OUTPUT_FILENAME, 'rb')
        wf = wave.open("output1.wav", 'rb')
        if layers >= 2:
            wf2 = wave.open("output2.wav", 'rb')
            if layers >= 3:
                wf3 = wave.open("output3.wav", 'rb')
                if layers >= 4:
                    wf4 = wave.open("output4.wav", 'rb')

        # open stream for wav file playback
        stream = p.open(format =
                    p.get_format_from_width(wf.getsampwidth()),
                    channels = wf.getnchannels(),
                    rate = wf.getframerate(),
                    output = True)

        # read data from wav file
        data = wf.readframes(chunk)
        if layers >= 2:
            data2 = wf2.readframes(chunk)
            if layers >= 3:
                data3 = wf3.readframes(chunk)
                if layers >= 4:
                    data4 = wf4.readframes(chunk)

        # play stream from wav file
        while data != '' and canPlay():

            if layers >= 2:
                data = audioop.add(data, data2, CHANNELS)
                if layers >= 3:
                    data = audioop.add(data, data3, CHANNELS)
                    if layers >= 4:
                        data = audioop.add(data, data4, CHANNELS)

            stream.write(data)

            data = wf.readframes(chunk)
            if layers >= 2:
                data2 = wf2.readframes(chunk)
                if layers >= 3:
                    data3 = wf3.readframes(chunk)
                    if layers >= 4:
                        data4 = wf4.readframes(chunk)

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

def reset(event):
    global layers, state
    print "reset pressed"
    layers = 1
    state = "stop"

def quit(event):
    print "quitting"
    root.quit()

root = Tk()
frame = Frame(root, width=683, height=768, bg="black", padx=4, pady=4)
frame.bind("<space>", lambda event, arg=1: record(event, arg))
frame.bind("1", lambda event, arg=1: record(event, arg))
frame.bind("2", lambda event, arg=2: record(event, arg))
frame.bind("3", lambda event, arg=3: record(event, arg))
frame.bind("4", lambda event, arg=4: record(event, arg))
frame.bind("p", play)
frame.bind("s", stop)
frame.bind("r", reset)
frame.bind("q", quit)
frame.pack()
frame.focus_set()
# Label(frame, fg="white", bg="black", width=24, height=8, anchor=CENTER, font=("helvetica", 42), text="Loop Machine").pack()
# Label(frame, fg="white", bg="black", width=24, height=9, anchor=CENTER, font=("helvetica", 20), text="space, 1 - Record track 1\n2 - Record track 2\n3 - Record track 3\n4 - Record track 4\np - Play loop\ns - Stop\nr - Reset\nq - Quit").pack()
Label(frame, fg="white", bg="black", width=24, height=8, anchor=CENTER, font=("helvetica", 42), text="Loop Machine").grid(row=0, columnspan=4)
rec1b = Label(frame, fg="black", bg="cyan", width=12, height=3, anchor=CENTER, font=("helvetica", 20), text="space, 1\nRec track 1")
rec1b.grid(row=1, column=0, padx=4, pady=4)
rec2b = Label(frame, fg="black", bg="green", width=12, height=3, anchor=CENTER, font=("helvetica", 20), text="2\nRec track 2")
rec2b.grid(row=1, column=1, padx=4, pady=4)
rec3b = Label(frame, fg="black", bg="orange", width=12, height=3, anchor=CENTER, font=("helvetica", 20), text="3\nRec track 3")
rec3b.grid(row=1, column=2, padx=4, pady=4)
rec4b = Label(frame, fg="black", bg="red", width=12, height=3, anchor=CENTER, font=("helvetica", 20), text="4\nRec track 4")
rec4b.grid(row=1, column=3, padx=4, pady=4)
playb = Label(frame, fg="black", bg="dodgerblue", width=12, height=3, anchor=CENTER, font=("helvetica", 20), text="p\nPlay")
playb.grid(row=2, column=0, padx=4, pady=4)
stopb = Label(frame, fg="black", bg="darkgreen", width=12, height=3, anchor=CENTER, font=("helvetica", 20), text="s\nStop")
stopb.grid(row=2, column=1, padx=4, pady=4)
resetb = Label(frame, fg="black", bg="gold", width=12, height=3, anchor=CENTER, font=("helvetica", 20), text="r\nReset")
resetb.grid(row=2, column=2, padx=4, pady=4)
quitb = Label(frame, fg="black", bg="darkred", width=12, height=3, anchor=CENTER, font=("helvetica", 20), text="q\nQuit")
quitb.grid(row=2, column=3, padx=4, pady=4)

if mousecontrol:
    rec1b.bind("<Button-1>", lambda event, arg=1: record(event, arg))
    rec2b.bind("<Button-1>", lambda event, arg=2: record(event, arg))
    rec3b.bind("<Button-1>", lambda event, arg=3: record(event, arg))
    rec4b.bind("<Button-1>", lambda event, arg=4: record(event, arg))
    playb.bind("<Button-1>", play)
    stopb.bind("<Button-1>", stop)
    resetb.bind("<Button-1>", reset)
    quitb.bind("<Button-1>", quit)

root.mainloop()