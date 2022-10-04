import qwiic
import time
from vosk import Model, KaldiRecognizer
import sys
import os
import wave
from subprocess import call

if not os.path.exists("model"):
    print ("Please download the model from https://github.com/alphacep/vosk-api/blob/master/doc/models.md and unpack as 'model' in the current folder.")
    exit (1)

wf = wave.open(sys.argv[1], "rb")
if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getcomptype() != "NONE":
    print ("Audio file must be WAV format mono PCM.")
    exit (1)
model = Model("model")
# You can also specify the possible word list
rec = KaldiRecognizer(model, wf.getframerate(), '["want need one to", "[unk]"]')

print("VL53L1X Qwiic Test\n")
ToF = qwiic.QwiicVL53L1X()
if (ToF.sensor_init() == None): # Begin returns 0 on a good init
    print("Sensor online!\n")


while True:
    try:
        ToF.start_ranging() # Write configuration bytes to initiate measurement
        time.sleep(1)
        distance = ToF.get_distance() # Get the result of the measurement from the sensor
        time.sleep(1)
        ToF.stop_ranging()
        data = wf.readframes(4000)
        distanceInches = distance / 25.4
        distanceFeet = distanceInches / 12.0

        print("Distance(mm): %s Distance(ft): %s" % (distance, distanceFeet))
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            test = rec.Result()
            if test == 'want' and distanceFeet > 0:
                print("Yay")
        else:
            print(rec.PartialResult())
            if distanceFeet < 2:
                call(["espeak", "-s140 -ven+18 -z", "I want to go outside"])
                break
    except Exception as e:
        print(e)
        
    