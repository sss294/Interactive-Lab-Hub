#from: https://elinux.org/RPi_Text_to_Speech_(Speech_Synthesis)#Festival_Text_to_Speech

#Record file
arecord -D hw:2,0 -f cd -c1 -r 44100 -d 5 -t wav recorded_mono.wav

#Analyze the recording
python3 proximity.py recorded_mono.wav

