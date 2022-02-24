# Grabacion de un archivo de audio 'q' para terminar

import numpy as np         # arrays    
import sounddevice as sd   # modulo de conexión con portAudio
import soundfile as sf     # para lectura/escritura de wavs
import kbhit               # para lectura de teclas no bloqueante


CHUNK = 1024
CHANNELS = 1
SRATE = 44100
CHUNKS_DELAY = 100000

# abrimos stream de entrada (InpuStream)
inputStream = sd.InputStream(samplerate=SRATE, blocksize=CHUNK, dtype="float32", channels=1)
# arrancamos stream
inputStream.start()

# abrimos stream de salida
outputStream = sd.OutputStream(samplerate = SRATE, blocksize  = CHUNK, channels = 1)
# arrancamos stream
outputStream.start()

print("* grabando")
print("* pulsa q para termninar")

# buffer para acumular grabación.
# (0,1): con un canal (1), vacio (de tamaño 0)
buffer = np.empty((0, 1), dtype="float32")

# bucle de grabación
kb = kbhit.KBHit()
c = ' '

numBloqueMandado = 0
bloquesEspera = 0

while c != 'q': 
    bloque = inputStream.read(CHUNK)  # recogida de samples en array numpy 
    # read devuelve un par (samples,bool)
    buffer = np.append(buffer,bloque[0]) # en bloque[0] están los samples
    print(len(buffer))  
    if kb.kbhit(): c = kb.getch()
    print("a: ", len(buffer)*CHUNK)
    print("b: ", CHUNKS_DELAY*CHUNK)

    if(len(buffer)*CHUNK >= CHUNKS_DELAY*CHUNK ):
        sd.play(buffer[CHUNK*numBloqueMandado*2 : CHUNK*(numBloqueMandado + 2 )*2 ], SRATE)
        sd.wait()
        print("HOLIWI")
        numBloqueMandado +=2
outputStream.time
inputStream.stop() 
outputStream.stop()
print("* grabacion terminada")

kb.set_normal_term()