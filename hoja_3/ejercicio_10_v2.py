from tkinter import TRUE
from matplotlib.pyplot import axis
import numpy as np         
import sounddevice as sd   
import soundfile as sf     
import kbhit               

CHUNK = 1024
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

    #ESTO ESTA COPIADO TAL CUAL DEL EJEMPLO DE PLAYEAR UN CALLBACK Y 
    # ES PROBABLEMENTE LO QUE TENGAMOS QUE MODIFICAR PARA QUE FUNQUE EN CONDICIONES
    
    # vemos si podemos coger un CHUNK entero o lo que quede en 
    chunksize = min(len(buffer) - current_frame, frames)  
    
    # escribimos en outdata los samples correspondientes
    outdata[:chunksize] = buffer[current_frame:current_frame + chunksize]    
    # es una forma compacta de hacer:
    #for i in range(chunksize): outdata[i] = buffer[current_frame+i]

    # NO funcionaría hacer outdata = data[current_frame:current_frame + chunksize]
    # porque asignaría (compartiría) referencias (objetos array de numpy)
    # outdata tiene que ser un nuevo array para enviar al stream y que no se reescriba
    
    if chunksize < frames: # ha terminado?
        outdata[chunksize:] = 0
        raise sd.CallbackStop()

    # actualizamos current_frame con los frames procesados    
    current_frame += chunksize


# stream de entrada/salida con callBack
stream = sd.Stream(
    samplerate=SRATE, dtype="float32",
    channels=CHANNELS,
    blocksize=CHUNK, 
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