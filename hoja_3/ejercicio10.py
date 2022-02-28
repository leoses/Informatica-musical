# Grabacion de un archivo de audio 'q' para terminar

import numpy as np         # arrays    
import sounddevice as sd   # modulo de conexión con portAudio
import soundfile as sf     # para lectura/escritura de wavs
import kbhit               # para lectura de teclas no bloqueante
import time


CHUNK = 1024
CHANNELS = 1
SRATE = 44100
DELAY = 1.0
HALF_CHUNK = int(CHUNK/2)

#frames = np.array([]).astype(np.float32)
lastTime = time.time()
currentTime = time.time()

bloque = np.zeros([CHUNK])
buffer = np.array([]).astype(np.float32)

def input_callback(indata, frame_count, time, status):
    global buffer
    buffer = np.append(buffer, np.frombuffer(indata))
    print(buffer.shape)


def output_Callback(out_data, frame_count, time_info, status):
    currentTime = time.time()
    if lastTime + DELAY < currentTime:
        global buffer
        global bloque
        bloque = buffer[HALF_CHUNK: HALF_CHUNK + HALF_CHUNK]
        buffer = np.delete(buffer, np.s_[HALF_CHUNK: HALF_CHUNK + HALF_CHUNK])
        out_data=bloque.astype(buffer.dtype).tobytes()

# abrimos stream de entrada (InpuStream)
inputStream = sd.InputStream(samplerate=SRATE, blocksize=CHUNK, dtype="float32", channels=1,callback=input_callback)
# arrancamos stream
inputStream.start()

# abrimos stream de salida
outputStream = sd.OutputStream(samplerate = SRATE, blocksize  = CHUNK, channels = 1,callback=output_Callback)
# arrancamos stream
outputStream.start()


# bucle de grabación
kb = kbhit.KBHit()
c = ' '

while c != 'q': 
    if kb.kbhit():
        c = kb.getch()
   

        
inputStream.stop() 
outputStream.stop()

print("* grabacion terminada")

kb.set_normal_term()