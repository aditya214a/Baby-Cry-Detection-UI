import pyaudio, wave, threading

from predict import Predict
predict = Predict()

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "output.wav"
p = pyaudio.PyAudio()
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

class Record:
    # def __init__(self,stop):
    #     self.stop = 
    def record(self,window,stop):
        print("[LOG] Recording audio!")
        frames = []
        songname = "output"
        WAVE_OUTPUT_FILENAME = "output.wav"
        for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
            data = stream.read(CHUNK)
            frames.append(data)
            if stop():
                # print("returning")
                break
        else:
            wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(p.get_sample_size(FORMAT))
            wf.setframerate(RATE)
            wf.writeframes(b''.join(frames))
            # print("DONE RECORDING")
            t2 = threading.Thread(target=predict.predict, args=(songname,window))
            t2.start()

    def play(self):
        wf = wave.open('output.wav', 'rb')
        pa = pyaudio.PyAudio()
        stream_output = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=False,
                output=True,
                frames_per_buffer=CHUNK)
        data = wf.readframes(CHUNK)
        while data != '':
        # writing to the stream is what *actually* plays the sound.
            stream_output.write(data)
            data = wf.readframes(CHUNK)
            # if stop():
            #     # print("returning")
            #     break
        stream_output.stop_stream()
        stream_output.close()    
        pa.terminate()

    def close(self):
        """Close all open streams/files"""
        global stream, p#, wf
        stream.stop_stream()
        stream.close()
        p.terminate()
        # wf.close()