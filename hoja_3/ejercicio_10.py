import numpy as np         
import sounddevice as sd   
import soundfile as sf     
import kbhit               

CHANNELS = 1
SRATE = 44100
TIME_RETARDO = 0.5

# buffer para acumular grabación.
# (0,1): con un canal (1), vacio (de tamaño 0)
buffer = np.empty((int(SRATE*TIME_RETARDO), 1), dtype="float32")
# contador de frames
current_frame = 0

def input_callback(indata,outdata, frames, time, status):
    global buffer
    global current_frame
    buffer = np.append(buffer,indata, axis=0)

    chunksize = min(len(buffer) - current_frame, frames)  
    outdata[:chunksize] = buffer[current_frame:current_frame + chunksize]    
    
    if chunksize < frames: # ha terminado?
        outdata[chunksize:] = 0
        raise sd.CallbackStop()
 
    current_frame += chunksize


# stream de entrada/salida con callBack
stream = sd.Stream(
    samplerate=SRATE, dtype="float32",
    channels=CHANNELS,
    blocksize= int(SRATE*TIME_RETARDO), 
    callback=input_callback)


# arrancamos stream entrada/salida
stream.start()
 
kb = kbhit.KBHit()
c = ' '
while c != 'q': 
    if kb.kbhit(): 
        c = kb.getch()
        print(c)

stream.stop() 
kb.set_normal_term()