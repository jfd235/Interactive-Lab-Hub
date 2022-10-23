import pyaudio
import numpy as np
from scipy.fft import rfft, rfftfreq
from scipy.signal.windows import hann
from numpy_ringbuffer import RingBuffer

import queue
import time


## Please change the following number so that it matches to the microphone that you are using. 
DEVICE_INDEX = 2

## Compute the audio statistics every `UPDATE_INTERVAL` seconds.
UPDATE_INTERVAL = 1.0

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

    stream = pyaudio_instance.open(input=True,start=False,format=pyaudio.paFloat32,channels=CHANNELS,rate=SAMPLING_RATE,frames_per_buffer=int(SAMPLING_RATE/2),stream_callback=_callback,input_device_index=DEVICE_INDEX)
    
    
    # One essential way to keep track of variables overtime is with a ringbuffer. 
    # As an example the `AudioBuffer` it stores always the last second of audio data. 
    AudioBuffer = RingBuffer(capacity=SAMPLING_RATE*1, dtype=FORMAT) # 1 second long buffer.
    
    # Another example is the `VolumeHistory` ringbuffer. 
    VolumeHistory = RingBuffer(capacity=int(20/UPDATE_INTERVAL), dtype=FORMAT) ## This is how you can compute a history to record changes over time
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

                print(volume)
                if volume > thresh:
                    print("Threshold exceded!")
                
                nextTimeStamp = UPDATE_INTERVAL+time.time() # See `UPDATE_INTERVAL` above


if __name__ == '__main__':
    main()
    print("Something happend with the audio example. Stopping!") 


