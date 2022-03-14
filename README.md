# kscp (Kashmiri Speech Corpus Processing)
Text and audio processing of the Kashmiri language corpus. 
### Usage
* Place the audio (.wav) files in the `./dataset/audio` directory and the transcription files in the `./dataset/txt` directory. 
* Set up the directory structure 
```
make setup
```
* Compile `get_f0`
```
cd get_f0 && make && cd ..
```
Link to the original repo : <https://github.com/gareth-ferneyhough/get_f0>

Finally run the `main.py` for the extraction of the descriptive data from the dataset. The generated data will be stored in the `./results` folder. 

