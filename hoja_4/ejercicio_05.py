import numpy as np         # arrays
import sounddevice as sd   # modulo de conexión con portAudio
import soundfile as sf     # para lectura/escritura de wavs
import kbhit               # para lectura de teclas no bloqueante

SRATE = 44100
CHUNK = 1024

class Nota :
    def __init__(self, freq, dur):
        self.freq = freq
        self.dur = dur
        self.samples=[]
        self.chunk=0
    def initNota(self) :
        self.samples=KarplusStrong(self.freq,self.dur)
        return 
    def getchunks(self) :
        self.chunk=self.chunk + 1
        return self.samples[CHUNK * (self.chunk-1): min(len(self.samples),CHUNK * self.chunk)]


def KarplusStrong(frec, dur):
    N = SRATE // int(frec) # la frecuencia determina el tamanio del buffer
    buf = np.random.rand(N) * 2 - 1 # buffer inicial: ruido
    nSamples = int(dur*SRATE)
    samples = np.empty(nSamples, dtype=float) # salida
    # generamos los nSamples haciendo recorrido circular por el buffer
    for i in range(nSamples):
        samples[i] = buf[i % N] # recorrido de buffer circular
    buf[i % N] = 0.5 * (buf[i % N] + buf[(1 + i) % N]) # filtrado
    return samples



notes = "C.D.EF.G.A.B"
freqs = [523.251*(2**(i/12)) for i in range(12)]

# abrimos stream de salida
stream = sd.OutputStream(
    samplerate = SRATE,            # frec muestreo 
    blocksize  = CHUNK,            # tamaño del bloque (muy recomendable unificarlo en todo el programa)
    channels   = 1)  # num de canales

# arrancamos stream
stream.start()

lista=[]
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
            vel = freqs[0]
        elif (c == 'x'):
            vel = freqs[2]
        elif (c == 'c'):
            vel = freqs[4]
        elif (c == 'v'):
            vel = freqs[5]
        elif (c == 'b'):
            vel = freqs[7]
        elif (c == 'n'):
            vel = freqs[9]
        elif (c == 'm'):
            vel = freqs[11]
        elif (c == 'a'):
            octava = max(1, octava-1) 
            continue
        elif (c == 'A'):
            octava = min(4, octava + 1)
            continue
        else: continue
        
        #una nota
        nota= Nota(vel,1)
        nota.initNota()
        lista.append(nota)
    
    son=np.zeros(CHUNK)
    for elem in lista :
        auxchunk=elem.getchunks()
        if len(auxchunk)!=CHUNK :
            lista.remove(elem)    
        son+= np.resize(auxchunk,CHUNK)
    
    stream.write(np.float32(son/max(1,len(lista))))
    
