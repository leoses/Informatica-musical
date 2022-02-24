import numpy as np         # arrays
import sounddevice as sd   # modulo de conexión con portAudio
import soundfile as sf     # para lectura/escritura de wavs
import kbhit               # para lectura de teclas no bloqueante

SRATE = 44100
CHUNK = 1024

# returns a sinusoidal signal with frec, dur, vol


def osc(frec, dur, vol):
    print("Duracion: " + str(dur))
    # number of samples requiered according to SRATE
    nSamples = int(SRATE*float(dur))
    return vol * np.sin(2*np.pi*np.arange(nSamples)*frec/SRATE, dtype="float32")


data, SRATE = sf.read('piano.wav')


frequencies = {'C': 1.0, 'D': 1.12, 'E': 1.19,
               'F': 1.33, 'G': 1.5, 'A': 1.59, 'B': 1.78}

# abrimos stream de salida
stream = sd.OutputStream(
    samplerate=SRATE,            # frec muestreo
    # tamaño del bloque (muy recomendable unificarlo en todo el programa)
    blocksize=CHUNK,
    channels=1)  # num de canales

# arrancamos stream
stream.start()

# En data tenemos el wav completo, ahora procesamos por bloques (chunks)
# bloque = np.arange(CHUNK,dtype=data.dtype)
numBloque = 0
kb = kbhit.KBHit()
c = ' '

vol = 10.0
print('\n\nProcessing chunks: ', end='')

vel = SRATE
while c != 'q':

    # modificación de volumen
    if kb.kbhit():
        c = kb.getch()
        if (c == 'z'):
            vel = frequencies['C']
        elif (c == 'x'):
            vel = frequencies['D']
        elif (c == 'c'):
            vel = frequencies['E']
        elif (c == 'v'):
            vel = frequencies['F']
        elif (c == 'b'):
            vel = frequencies['G']
        elif (c == 'n'):
            vel = frequencies['A']
        elif (c == 'm'):
            vel = frequencies['B']

        sd.write(data, SRATE*vel)


print('end')
stream.stop()
