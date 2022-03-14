setup: 
	-mkdir -p results
	-mkdir -p results/plain_transcripts
	-mkdir -p results/plots
	-mkdir -p results/plots/durs_vs_lengths
	-mkdir -p results/plots/line_charlengths
	-mkdir -p results/plots/line_wordlengths
	-mkdir -p results/plots/line_durations
	-mkdir -p results/plots/non_zero_pitch_values
	-mkdir -p results/plots/pitch_transitions
	-mkdir -p results/plots/silence_percentage
	-mkdir -p results/plots/time_domain_waveforms
	-mkdir -p results/plots/unique_word_lengths_vs_counts
	-mkdir -p results/plots/freq_domain_waveforms
	-mkdir -p results/plots/freq_domain_waveforms/amplitude_spectra
	-mkdir -p results/plots/freq_domain_waveforms/phase_spectra
	-mkdir -p results/pitchinfo
	-mkdir -p results/unique_chars
	-mkdir -p results/unique_words
	-mkdir -p dataset
	-mkdir -p dataset/audio
	-mkdir -p dataset/txt
clean: clean_plain_transcripts clean_plots clean_unique clean_pitchinfo
clean_plain_transcripts:
	-rm -f plain_transcripts/*
clean_plots: 
	-rm -f results/plots/durs_vs_lengths/*
	-rm -f results/plots/line_durations/*
	-rm -f results/plots/line_wordlengths/*
	-rm -f results/plots/line_charlengths/*
	-rm -f results/plots/time_domain_waveforms/*
	-rm -f results/plots/silence_percentage/*
	-rm -f results/plots/freq_domain_waveforms/amplitude_spectra/*
	-rm -f results/plots/freq_domain_waveforms/phase_spectra/*
	-rm -f results/plots/unique_word_lengths_vs_counts/*
	-rm -f results/plots/non_zero_pitch_values/*
	-rm -f results/plots/pitch_transitions/*
clean_unique: 
	-rm -f results/unique_chars/*
	-rm -f results/nique_words/*
clean_pitchinfo:
	-rm -f results/pitchinfo/*
