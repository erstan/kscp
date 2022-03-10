import os
from collections import Counter
"""
class txt_proc(text_data_path):
    .datapath --> path to the text data
    .files --> list of all the files in the .datapath
    .getlines(filename) --> list of all the lines in a transcription file
    .plainlines(filename) --> list of all the lines without timestamps 
    .linestamps(filename) --> beg and end stamps of the lines in a transcription file
    .linedurations(filename) --> durations (in seconds) of the lines in a transcription file
    .linewords(filename) --> list of the "list of words" of each line of the transcription
    .linechars(filename) --> list of the "list of characters" in each line of the transcription
    .linewordcounts(filename) --> list of the wordcounts in each line of the transcription
    .linecharcounts(filename) --> list of the char counts in each line of the transcription
    .allwords(filename) --> single list of all the words in the text file
    .uniquewords(filename) --> list of dictionaries containing the unique words and their counts in the file
    .allchars(filename) --> single list of all the chars in the text file
    .uniquechars(filename) --> list of dictionaries containting the unique chars and their counts in the file
"""
class txt_proc:
    def __init__(self, txt_datapath):
        self.datapath = txt_datapath
        self.files = os.listdir(self.datapath)
    def tabsplit(self, line):
        assert len(line.split("\t")) == 3, \
            "Transcription file is not properly formatted at " + line + "\n" + \
            "Transcription Format: \
                [Timestamp] [Tab] [Timestamp] [Tab] [Transcription Line] [Newline]"
        return line.split("\t")
    def getlines(self, fname):
        filepath = self.datapath+"/"+fname
        with open(filepath) as f:
            lines = f.readlines()
        f.close()
        return [line.strip() for line in lines]
    def getplainline(self, line):
        return self.tabsplit(line)[2].strip()
    def plainlines(self, filename):
        lines_array = self.getlines(filename)
        return [self.getplainline(line) for line in lines_array]
    def linestamps(self, filename):
        lines_array = self.getlines(filename)
        stamps = []
        for line in lines_array:
            [beg, end, plain_line] = self.tabsplit(line)
            stamps.append({"beg": beg, "end": end})
        return stamps
    def linedurations(self, filename):
        stamps = self.linestamps(filename)
        return [float(stamp["end"])-float(stamp["beg"]) for stamp in stamps]
    def linewords(self, filename):
        lines = self.plainlines(filename)
        return [line.split(" ") for line in lines]
    def linechars(self, filename):
        lines = self.plainlines(filename)
        charstrings = ["".join(line.split(" ")) for line in lines]
        chars = []
        for str in charstrings:
            chars.append([char for char in str])
        return chars
    def linewordcounts(self, filename):
        words = self.linewords(filename)
        return [len(word_array) for word_array in words]
    def linecharcounts(self, filename):
        chars = self.linechars(filename)
        return [len(char_array) for char_array in chars]
    def allwords(self, filename):
        linewordlists = self.linewords(filename)
        all = []
        for wordlist in linewordlists:
            all.extend(wordlist)
        return all
    def uniquewords(self, filename):
        return dict(Counter(self.allwords(filename)))
    def allchars(self, filename):
        linecharlists = self.linechars(filename)
        all = []
        for charlist in linecharlists:
            all.extend(charlist)
        return all
    def uniquechars(self, filename):
        return dict(Counter(self.allchars(filename)))