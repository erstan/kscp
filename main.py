from txt_proc import txt_proc
import os
import csv
import matplotlib.pyplot as plt
from math import ceil
import time
import webrtcvad

plain_transcripts_path = "./results/plain_transcripts"
line_durations_path = "./results/plots/line_durations"
line_wordlengths_path = "./results/plots/line_wordlengths"
line_charlengths_path = "./results/plots/line_charlengths"
durs_vs_lengths_path = "./results/plots/durs_vs_lengths"
time_domain_waveforms_path = "./results/plots/time_domain_waveforms"
silence_percentage_path = "./results/plots/silence_percentage"
amplitude_spectra_path = "./results/plots/freq_domain_waveforms/amplitude_spectra"
non_zero_pitch_values_path = "./results/plots/non_zero_pitch_values"
pitch_transitions_path = "./results/plots/pitch_transitions"
phase_spectra_path = "./results/plots/freq_domain_waveforms/phase_spectra"
unique_words_path = "./results/unique_words"
unique_word_lengths_vs_counts_path = "./results/plots/unique_word_lengths_vs_counts"
unique_chars_path = "./results/unique_chars"

datapath = "./dataset"
txt_datapath = "./dataset/txt"
aud_datapath = "./dataset/audio"
def writegraph(x, y, xlabel, ylabel, title, path, type):
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    if(type=='p'):
        plt.plot(x, y)
    elif(type=='b'):
        plt.bar(x,y)
    elif(type=='s'):
        plt.scatter(x,y)
    else:
        print("Unknown graph type : ", type)
    plt.savefig(path)
    plt.close()
    return
def fwritevar(filepath, variable):
    f = open(filepath, "w")
    f.write(variable)
    f.close()
def dicttocsv(csvfilepath, dictionary):
    f = open(csvfilepath, "w")
    for item, count in dictionary.items():
        csv.writer(f).writerow([item, count])
    f.close()
def keylen(k):
    return len(k[0])
def sortbykeylengths(d):
    l = list(d.items())
    l.sort(key=keylen)
    return {elem[0] : elem[1] for elem in l}
def counttransits(c):
    t = 0
    for i in range(0, len(c)-1):
        if(c[i]==0 and c[i+1]!=0) or (c[i]!=0 and c[i-1]==0):
            t = t + 1
    return t


tp = txt_proc(txt_datapath=txt_datapath)
text_files = tp.files
total_files = len(text_files)
i = 1
for filename in text_files:
    nameonly = os.path.splitext(filename)[0]
    print("Text[", i, "/", total_files, "]: ", tp.datapath+"/"+filename)
    i = i + 1

    # plain transcript generation
    plain_transcript = " - ".join(tp.plainlines(filename))
    plain_transcript_dest = plain_transcripts_path+"/"+nameonly+".txt"
    fwritevar(plain_transcript_dest, plain_transcript)

    # unique words & their counts
    unique_words = tp.uniquewords(filename)
    unique_words = sortbykeylengths(unique_words)
    unique_word_lengths = [len(k) for k in unique_words.keys()]
    unique_word_counts = [int(k) for k in unique_words.values()]
    unique_words_dest = unique_words_path+"/"+nameonly+".csv"
    dicttocsv(unique_words_dest, unique_words)

    # unique word lengths vs their counts
    unique_word_lengths_vs_counts_dest = unique_word_lengths_vs_counts_path+"/"+nameonly+".png"
    writegraph(x=unique_word_lengths[1:], y=unique_word_counts[1:], 
                xlabel="Word Lengths", ylabel="Word Frequencies", title=nameonly, 
                path=unique_word_lengths_vs_counts_dest, type='p')
    # unique characters & their counts
    unique_chars = tp.uniquechars(filename)
    unique_chars_dest = unique_chars_path+"/"+nameonly+".csv"
    dicttocsv(unique_chars_dest, unique_chars)

    # histogram which pictorially shows the wordlengths of all the lines
    line_wordlengths = tp.linewordcounts(filename)
    total_lines = len(line_wordlengths)
    line_wordlengths_dest = line_wordlengths_path+"/"+nameonly+".png"
    writegraph(x=list(range(1, total_lines + 1)), y=line_wordlengths,
                xlabel="Line Number", ylabel="Line Length (Number of Words)", title=nameonly, 
                path=line_wordlengths_dest, type='p')

    # histogram of charlengths of all the lines
    line_charlengths = tp.linecharcounts(filename)
    total_lines = len(line_charlengths)
    line_charlengths_dest = line_charlengths_path+"/"+nameonly+".png"
    writegraph(x=list(range(1, total_lines + 1)), y=line_charlengths,
                xlabel="Line Number", ylabel="Line Length (Number of Characters)", title=nameonly, 
                path=line_charlengths_dest, type='p')

    # histogram of the time durations covered by all the lines 
    line_durations = tp.linedurations(filename)
    total_lines = len(line_durations)
    plt.xlabel("Line Number")
    plt.ylabel("Line Duration")
    plt.title(nameonly)
    plt.bar(list(range(1, total_lines + 1)), line_durations)
    line_durations_dest = line_durations_path+"/"+nameonly+".png"
    plt.savefig(line_durations_dest)
    plt.close()
    writegraph(x=list(range(1, total_lines + 1)), y=line_durations,
                xlabel="Line Number", ylabel="Line Duration", title=nameonly, 
                path=line_durations_dest, type='p')

    # scatter plot of line lengths & line durations
    durs_vs_lengths_dest = durs_vs_lengths_path+"/"+nameonly+".png"
    writegraph(x=line_wordlengths, y=line_durations,
                xlabel="Line Length", ylabel="Line Duration", title=nameonly, 
                path=durs_vs_lengths_dest, type='p')


from aud_proc import *
from aud_proc import aud_proc
total_audio_len = 0
ap = aud_proc(aud_datapath)
audio_files = ap.files
total_files = len(audio_files)
i = 1
for filename in audio_files:
    nameonly = os.path.splitext(filename)[0]
    print("Audio[", i, "/", total_files, "]: ", ap.datapath+"/"+filename)
    i = i + 1
    wavedata = ap.getdata(filename)
    # time domain representation of the audio waveform
    y = wavedata["samples"]
    t = wavedata["time"]
    time_domain_waveforms_dest = time_domain_waveforms_path+"/"+nameonly+".png"
    writegraph(x=t, y=y,
                xlabel="Time (s)", ylabel="y(t)", title=nameonly, 
                path=time_domain_waveforms_dest, type='p')

    # amplitude spectrum of the audio waveform
    amplitude_spectrum = ap.amp_spectrum(wavedata)
    amplitude_spectra_dest = amplitude_spectra_path+"/"+nameonly+".png"
    writegraph(x=amplitude_spectrum[0][::2000], y=amplitude_spectrum[1][::2000],
                xlabel="Frequency (Hz)", ylabel="Amplitude", title=nameonly, 
                path=amplitude_spectra_dest, type='p')

    # phase spectrum of the audio waveform
    phase_spectrum = ap.ph_spectrum(wavedata)
    phase_spectra_dest = phase_spectra_path+"/"+nameonly+".png"
    writegraph(x=phase_spectrum[0][::2000], y=phase_spectrum[1][::2000],
                xlabel="Frequency (Hz)", ylabel="Phase Angle (rad.)", title=nameonly, 
                path=phase_spectra_dest, type='p')
    # linewise silence percentage
    rw = read_wave(ap.datapath+"/"+filename)
    pcm_data, sample_rate = rw[0], rw[1]
    vad = webrtcvad.Vad(3)
    frame_duration = 10
    frames = list(frame_generator(frame_duration, pcm_data, sample_rate))
    tfilename = nameonly+".txt"
    stamps = tp.linestamps(tfilename)
    percent_silence = []
    for linestamp in stamps:
        start = float(linestamp["beg"])
        end = float(linestamp["end"])
        total_frames = 0
        voiced_frames = 0
        silent_frames = 0
        for frame in frames:
            if frame.timestamp + frame_duration*0.001 > end:
                break
            elif frame.timestamp < start:
                continue
            else:
                total_frames = total_frames + 1
                if(vad.is_speech(frame.bytes, sample_rate)):
                    voiced_frames = voiced_frames + 1
                else:
                    silent_frames = silent_frames + 1
        percent_silence.append(float(silent_frames/total_frames * 100))
    silence_percentage_dest = silence_percentage_path+"/"+nameonly+".png"
    writegraph(x=list(range(1, len(percent_silence) + 1)), y=percent_silence,
                xlabel="Line Number", ylabel="Silence Percentage", title=nameonly, 
                path=silence_percentage_dest, type='p')
    
    # plotting non-zero pitch values
    csv_destination = "./results/pitchinfo/"+nameonly+".csv"
    ffs = ap.pitchinfo(filename, csv_destination)["fundamental_freq"].values()
    non_zero_pitches = []
    for p in ffs:
        if(float(p)):
            non_zero_pitches.append(float(p))
    non_zero_pitch_values_dest = non_zero_pitch_values_path + "/" + nameonly + ".png"
    writegraph(x=[x for x in range(1, len(non_zero_pitches)+1)], y=non_zero_pitches,
                xlabel="Audio Frames", ylabel="Pitch Values", title=nameonly, 
                path=non_zero_pitch_values_dest, type='p')

    # plotting pitch transitions per second
    transitions = []
    audio_len = float(wavedata["length"])
    pitch_values = [float(p) for p in ffs]
    total_pitch_values = float(len(pitch_values))
    pitch_values_per_second = ceil(total_pitch_values / audio_len)
    frame_chunks = [pitch_values[x:x+pitch_values_per_second] 
                            for x in range(0, len(pitch_values), pitch_values_per_second)]
    for chunk in frame_chunks:
        transitions.append(counttransits(chunk))
    pitch_transitions_dest = pitch_transitions_path + "/" + filename + ".png"
    writegraph(x=range(1, len(transitions)+1), y=transitions,
                xlabel="Time (s)", ylabel="Pitch Transition Rate", title=nameonly, 
                path=pitch_transitions_dest, type='p')

    total_audio_len = total_audio_len + audio_len

print("------------------------------------------")
print(f"Total data processed : {time.strftime('%H h:%M m:%Ss', time.gmtime(total_audio_len))}")
print("------------------------------------------")