# reproductor con Chunks

import numpy as np         # arrays    
import sounddevice as sd   # modulo de conexión con portAudio
import soundfile as sf     # para lectura/escritura de wavs
import kbhit               # para lectura de teclas no bloqueante

SRATE = 44100
CHUNK = 1024

# returns a sinusoidal signal with frec, dur, vol
def osc(frec,dur,vol):
    print("Duracion: " + str(dur))
    # number of samples requiered according to SRATE
    nSamples = int(SRATE*float(dur))
    return vol * np.sin(2*np.pi*np.arange(nSamples)*frec/SRATE, dtype="float32")


song = [('G',0.5),('G',0.5),('A',1.0),('G',1.0),('c',1.0),('B',2.0),
('G',0.5),('G',0.5),('A',1.0),('G',1.0), ('d',1.0), ('c',2.0),
('G',0.5),('G',0.5), ('g', 1.0), ('e', 1.0), 
('c',1.0), ('B',1.0), ('A',1.0),
('f', 0.5), ('f', 0.5), ('e',1.0),('c',1.0),
('d',1.0), ('c', 2.0)]

frequencies =  {'C': 523.251, 'D': 587.33, 'E': 659.255, 'F': 698.456, 'G': 783.991, 'A': 880, 'B': 987.767}

# abrimos stream de salida
stream = sd.OutputStream(
    samplerate = SRATE,            # frec muestreo 
    blocksize  = CHUNK,            # tamaño del bloque (muy recomendable unificarlo en todo el programa)
    channels   = 1)  # num de canales

# arrancamos stream
stream.start()

# En data tenemos el wav completo, ahora procesamos por bloques (chunks)
# bloque = np.arange(CHUNK,dtype=data.dtype)
numBloque = 0
kb = kbhit.KBHit()
c= ' '

vol = 10.0
print('\n\nProcessing chunks: ',end='')

# termina con 'q' o cuando el último bloque ha quedado incompleto (menos de CHUNK samples)
for note in song:
    print(note)
    hz = frequencies[note[0].upper()]
    if note[0] not in frequencies.keys():
        hz = hz*2

    samples = osc(hz,note[1],vol)
    stream.write(samples)


print('end')
stream.stop()

