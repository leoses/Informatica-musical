import numpy as np         # arrays    
import sounddevice as sd   # modulo de conexión con portAudio
import soundfile as sf     # para lectura/escritura de wavs

SRATE = 44100
CHUNK = 1024
vol = 1.0

def osc(frec,dur,vol):
    print("Duracion: " + str(dur))
    nSamples = int(SRATE*float(dur))
    return vol * np.sin(2*np.pi*np.arange(nSamples)*frec/SRATE)


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

for note in song:
    print(note)
    hz = frequencies[note[0].upper()]
    if note[0] not in frequencies.keys():
        hz = hz*2

    samples = osc(hz,note[1],vol)
    stream.write(np.float32(samples))


print('end')
stream.stop()

