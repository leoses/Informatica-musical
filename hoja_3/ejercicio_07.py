# reproductor con Chunks

import numpy as np         # arrays    
import sounddevice as sd   # modulo de conexión con portAudio
import soundfile as sf     # para lectura/escritura de wavs
import kbhit               # para lectura de teclas no bloqueante

SRATE = 44100

# returns a sinusoidal signal with frec, dur, vol
def osc(frec,dur,vol):
    # number of samples requiered according to SRATE
    nSamples = int(SRATE*dur)
    return vol * np.sin(2*np.pi*np.arange(nSamples)*frec/SRATE, dtype="float32")