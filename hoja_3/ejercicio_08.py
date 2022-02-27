import numpy as np         # arrays
import sounddevice as sd   # modulo de conexión con portAudio
import soundfile as sf     # para lectura/escritura de wavs
import kbhit               # para lectura de teclas no bloqueante

SRATE = 44100
CHUNK = 1024

data, SRATE = sf.read('piano.wav')

frequencies = {'C': 1.0, 'D': 1.12, 'E': 1.25,'F': 1.33, 'G': 1.5, 'A': 1.68, 'B': 1.88}

# En data tenemos el wav completo, ahora procesamos por bloques (chunks)
# bloque = np.arange(CHUNK,dtype=data.dtype)
numBloque = 0
kb = kbhit.KBHit()
c = ' '

vol = 10.0
vel = SRATE
octava = 1
while c != 'q':

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
        elif (c == 'a'):
            octava = max(1, octava-1) 
            continue
        elif (c == 'A'):
            octava = min(4, octava + 1)
            continue
        else: continue
        
        sd.play(np.float32(data), SRATE*vel*octava, blocking=False)
