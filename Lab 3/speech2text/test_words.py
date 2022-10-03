#!/usr/bin/env python3

from vosk import Model, KaldiRecognizer
import sys
import os
import wave
import json

def getData():
    text = ""
    
    while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            data = json.loads(rec.Result())
            #print(rec.Result())
            #print("CONVERT DATA")
            text = data["text"]
        #else:
            #print(rec.PartialResult())

    #print(rec.FinalResult())
    #print(text)
    return(text.split())

def getVal(val):
        if val == "one":
            val = 1
        elif val == "two":
            val = 2
        elif val == "three":
            val = 3
        elif val == "four":
            val = 4
        elif val == "five":
            val = 5
        elif val == "six":
            val = 6
        elif val == "seven":
            val = 7
        elif val == "eight":
            val = 8
        elif val == "nine":
            val = 9
        elif val == "zero":
            val = 0
        return val

def parseData(data):
    num1 = num2 = 0.0
    op = ""

    # Read first number
    while data != []:
        val = data.pop(0)
        # Check for operator
        if val in ["plus", "minus", "times", "over"]:
            op = val
            break
        num1 *= 10
        num1 += getVal(val)

    # Read second number
    while data != []:
        val = data.pop(0)
        num2 *= 10
        num2 += getVal(val)
    
    # Perform operation
    if op == "plus":
        return num1 + num2
    elif op == "minus":
        return num1 - num2
    elif op == "times":
        return num1 * num2
    elif op == "over":
        return num1 / num2

if not os.path.exists("model"):
    print ("Please download the model from https://github.com/alphacep/vosk-api/blob/master/doc/models.md and unpack as 'model' in the current folder.")
    exit (1)

wf = wave.open(sys.argv[1], "rb")
if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getcomptype() != "NONE":
    print ("Audio file must be WAV format mono PCM.")
    exit (1)

model = Model("model")
# You can also specify the possible word list
rec = KaldiRecognizer(model, wf.getframerate(), "zero one two three four five six seven eight nine plus minus times over [unk]")

data = getData()
print(data)
out = parseData(data)

# Convert output to string form
if out < 0:
    out *= -1
    out = "negative" + str(out)
else:
    out = str(out)

print(out)
os.system("./my_demo.sh " + out)
