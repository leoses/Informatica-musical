# reproductor con Chunks

import numpy as np         # arrays    
import sounddevice as sd   # modulo de conexión con portAudio
import soundfile as sf     # para lectura/escritura de wavs
import kbhit               # para lectura de teclas no bloqueante

# corregido
last = 0 # ultimo frame generado
CHUNK = 1024
SRATE = 44100
FREC = 10

def oscChuck(frec,vol):
    global last # var global
    data = vol*np.sin(2*np.pi*(np.arange(CHUNK)+last)*frec/SRATE, dtype="float32")
    last += CHUNK # actualizamos ultimo generado
    return data


# leemos wav en array numpy (data)
# por defecto lee float64, pero podemos hacer directamente la conversion a float32
data  = oscChuck(FREC, 10)#, SRATE = sf.read('piano.wav',dtype="float32")


# informacion de wav
print("\n\nInfo del wav ",SRATE)
print("  Sample rate ",SRATE)
print("  Sample format: ",data.dtype)
print("  Num channels: ",len(data.shape))
print("  Len: ",data.shape[0])


# abrimos stream de salida
stream = sd.OutputStream(
    samplerate = SRATE,            # frec muestreo 
    blocksize  = CHUNK,            # tamaño del bloque (muy recomendable unificarlo en todo el programa)
    channels   = len(data.shape))  # num de canales

# arrancamos stream
stream.start()

# En data tenemos el wav completo, ahora procesamos por bloques (chunks)
# bloque = np.arange(CHUNK,dtype=data.dtype)
numBloque = 0
kb = kbhit.KBHit()
c= ' '

vol = 10.0
nSamples = CHUNK 
freq = FREC
print('\n\nProcessing chunks: ',end='')

# termina con 'q' o cuando el último bloque ha quedado incompleto (menos de CHUNK samples)
while c!= 'q': 
    samples = oscChuck(freq,vol)
    stream.write(samples)

    # modificación de volumen 
    if kb.kbhit():
        c = kb.getch()
        if (c=='v'): vol= max(0,vol-0.05)
        elif (c=='V'): vol= min(1,vol+0.05)
        elif(c =="F"): freq = max(0.5, freq + 1)
        elif(c == "f"):  freq = max(0.5, freq - 1)
        print("Vol: ",vol)

    numBloque += 1
    print('.',end='')


print('end')
stream.stop()
