import os
from scipy.io import wavfile
from scipy.fft import rfft, rfftfreq
import numpy as np 
import contextlib
import wave
import pandas as pd
"""
class aud_proc(audio_data_path):
    .datapath --> path to the audio data
    .files --> list of all the files in the .datapath
    .getdata(filename) --> get the audio waveform data
    .getlength(filename) --> get the length of the audio file in seconds
    .getsamplerate(filename) --> get the sample rate at which the audio file has been recorded
    .getwaveform(filename) --> returns the linearly spaced sampling time values & the sampled values
    .spectrum(wavedata) --> gives all the frequency components and their complex number amplitudes
    .amp_spectrum(wavedata) --> frequencies & their amplitudes
    .ph_spectrum(wavedata) --> frequencies & their phase angles
"""
def read_wave(path):
    with contextlib.closing(wave.open(path, 'rb')) as wf:
        num_channels = wf.getnchannels()
        sample_width = wf.getsampwidth()
        sample_rate = wf.getframerate()
        pcm_data = wf.readframes(wf.getnframes())
        length = wf.getnframes() / sample_rate
        return pcm_data, sample_rate, length
class Frame(object):
    def __init__(self, bytes, timestamp, duration):
        self.bytes = bytes
        self.timestamp = timestamp
        self.duration = duration
def frame_generator(frame_duration_ms, audio, sample_rate):
    n = int(sample_rate * (frame_duration_ms / 1000.0) * 2)
    offset = 0
    timestamp = 0.0
    duration = (float(n) / sample_rate) / 2.0
    while offset + n < len(audio):
        yield Frame(audio[offset:offset + n], timestamp, duration)
        timestamp += duration
        offset += n
def csvtodict(csvfilepath):
    df = pd.read_csv(csvfilepath)
    return df.to_dict()

class aud_proc:
    def __init__(self, aud_datapath):
        self.datapath = aud_datapath
        self.files = os.listdir(self.datapath)
    def getdata(self, filename):
        [sample_rate, samples] = wavfile.read(self.datapath+"/"+filename)
        time = np.linspace(0, len(samples)/sample_rate, len(samples))
        return {
                "sample_rate": sample_rate, 
                "time": time, 
                "samples": samples, 
                "pcm_data": [read_wave(self.datapath+"/"+filename)[0], read_wave(self.datapath+"/"+filename)[1]],
                "length" : read_wave(self.datapath+"/"+filename)[2]
        }
    def getlength(self, filename):
        return self.getdata(filename)["length"]
    def getsamplerate(self, filename):
        return self.getdata(filename)["sample_rate"]
    def getwaveform(self, filename):
        data = self.getdata(filename)
        return [data["time"], data["samples"]]
    def spectrum(self, wavedata):
        y = wavedata["samples"]
        sr = wavedata["sample_rate"]
        n = len(y)
        y_f = rfft(y)
        x_f = rfftfreq(n, 1/sr)
        return [x_f, y_f]
    def amp_spectrum(self, wavedata):
        [x_f, y_f] = self.spectrum(wavedata)
        return [x_f, np.abs(y_f)]
    def ph_spectrum(self, wavedata):
        [x_f, y_f] = self.spectrum(wavedata)
        return [x_f, np.angle(y_f)]
    def pitchinfo(self, filename, destination_filepath):
        os.system("f0_test "+self.datapath+"/"+filename+" > "+destination_filepath)
        return csvtodict(destination_filepath)
    
