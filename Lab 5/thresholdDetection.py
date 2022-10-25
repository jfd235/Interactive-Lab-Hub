import pyaudio
import numpy as np
from scipy.fft import rfft, rfftfreq
from scipy.signal.windows import hann
from numpy_ringbuffer import RingBuffer
from PIL import Image, ImageDraw, ImageFont
import adafruit_rgb_display.st7789 as st7789

import queue
import time

# Config for display baudrate (default max is 24mhz):
BAUDRATE = 64000000

# Create the ST7789 display:
disp = st7789.ST7789(
    spi,
    cs=cs_pin,
    dc=dc_pin,
    rst=reset_pin,
    baudrate=BAUDRATE,
    width=135,
    height=240,
    x_offset=53,
    y_offset=40,
)

# Create blank image for drawing.
# Make sure to create image with mode 'RGB' for full color.
height = disp.width  # we swap height/width to rotate it to landscape!
width = disp.height
image = Image.new("RGB", (width, height))
rotation = 90

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

## Please change the following number so that it matches to the microphone that you are using. 
DEVICE_INDEX = 2

## Compute the audio statistics every `UPDATE_INTERVAL` seconds.
UPDATE_INTERVAL = 0.1

## Fixed volume threshold value
thresh = 100

### Things you probably don't need to change
FORMAT=np.float32
SAMPLING_RATE = 44100
CHANNELS=1


def main():
    ### Setting up all required software elements: 
    audioQueue = queue.Queue() #In this queue stores the incoming audio data before processing.
    pyaudio_instance = pyaudio.PyAudio() #This is the AudioDriver that connects to the microphone for us.

    def _callback(in_data, frame_count, time_info, status): # This "callbackfunction" stores the incoming audio data in the `audioQueue`
        audioQueue.put(in_data)
        return None, pyaudio.paContinue

    stream = pyaudio_instance.open(input=True,start=False,format=pyaudio.paFloat32,channels=CHANNELS,rate=SAMPLING_RATE,frames_per_buffer=int(SAMPLING_RATE/200),stream_callback=_callback,input_device_index=DEVICE_INDEX)
    
    
    # One essential way to keep track of variables overtime is with a ringbuffer. 
    # As an example the `AudioBuffer` it stores always the last second of audio data. 
    AudioBuffer = RingBuffer(capacity=int(SAMPLING_RATE*0.1), dtype=FORMAT) # 1 second long buffer.
    
    # Another example is the `VolumeHistory` ringbuffer. 
    VolumeHistory = RingBuffer(capacity=int(1/UPDATE_INTERVAL), dtype=FORMAT) ## This is how you can compute a history to record changes over time
    ### Here  is a good spot to extend other buffers  aswell that keeps track of varailbes over a certain period of time. 

    nextTimeStamp = time.time()
    stream.start_stream()
    if True:
        while True:
            frames = audioQueue.get() #Get DataFrom the audioDriver (see _callbackfunction how the data arrives)
            if not frames:
                continue

            framesData = np.frombuffer(frames, dtype=FORMAT) 
            AudioBuffer.extend(framesData[0::CHANNELS]) #Pick one audio channel and fill the ringbuffer. 
            
            if(AudioBuffer.is_full and  # Waiting for the ringbuffer to be full at the beginning.
                audioQueue.qsize()<2 and # Make sure there is not alot more new data that should be used. 
                time.time()>nextTimeStamp): # See `UPDATE_INTERVAL` above.

                buffer  = np.array(AudioBuffer) #Get the last second of audio. 


                volume = np.rint(np.sqrt(np.mean(buffer**2))*10000) # Compute the rms volume

                VolumeHistory.append(volume)
                maxVol = volume
                volumechange = 0.0
                if VolumeHistory.is_full:
                    #HalfLength = int(np.round(VolumeHistory.maxlen/2)) 
                    #vnew = np.array(VolumeHistory)[HalfLength:].mean()
                    #vold = np.array(VolumeHistory)[:VolumeHistory.maxlen-HalfLength].mean()
                    #volumechange =vnew-vold
                    #volumneSlow = np.array(VolumeHistory).mean()
                    #VolumeHistory = VolumeHistory[1:]
                    maxVol = max(VolumeHistory)

                print(VolumeHistory)
                if maxVol > thresh:
                    print("Threshold exceded!")
                    draw.rectangle((0, 0, width, height), outline=0, fill=(255, 0, 0))
                    disp.image(image, rotation)
                else:
                    draw.rectangle((0, 0, width, height), outline=0, fill=(0, 0, 0))
                    disp.image(image, rotation)
                
                nextTimeStamp = UPDATE_INTERVAL+time.time() # See `UPDATE_INTERVAL` above


if __name__ == '__main__':
    main()
    print("Something happend with the audio example. Stopping!") 


