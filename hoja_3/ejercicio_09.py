import numpy as np         # arrays    
import sounddevice as sd   # modulo de conexión con portAudio
import soundfile as sf     # para lectura/escritura de wavs

data, SRATE = sf.read('piano.wav',dtype="float32")

last = 0 # ultimo frame generado
CHUNK = 1024
VOL = 1.0

class Delay:
    def __init__(self, sound, delay):
        self.sound = sound
        self.delay = delay
    
    def applyDelay(self):
        #print("Longitud de la muestra antes de aplicar el retardo: " + str(len(self.sound)))
        nSamples = int(SRATE*float(self.delay))
        #añadimos al principio del fragmento una zona en silencio de nSamples
        #para generar asi el delay
        delayedSound = np.append(np.float32(np.zeros(nSamples)),self.sound)
        #print("Longitud de la muestra despues de aplicar el retardo: " + str(len(delayedSound)))
        return delayedSound


retardo = Delay(data, 0.2)
dataRetarded = retardo.applyDelay()

# informacion de wav
print("\n\nInfo del wav ",SRATE)
print("  Sample rate ",SRATE)
print("  Sample format: ",data.dtype)
print("  Num channels: ",len(data.shape))

# abrimos stream de salida
stream = sd.OutputStream(
    samplerate = SRATE,            # frec muestreo 
    blocksize  = CHUNK,            # tamaño del bloque (muy recomendable unificarlo en todo el programa)
    channels   = len(data.shape))  # num de canales

# arrancamos stream
stream.start()
nSamples = CHUNK 
numBloque = 0

diff = len(dataRetarded) - len(data)
data = np.append(data, np.float32(np.zeros(diff)))
data += dataRetarded

# termina cuando el último bloque ha quedado incompleto (menos de CHUNK samples)
while nSamples == CHUNK: 
    # numero de samples a procesar: CHUNK si quedan sufucientes y si no, los que queden
    nSamples = min(CHUNK,data.shape[0] - (numBloque+1)*CHUNK)

    # nuevo bloque
    bloque = data[numBloque*CHUNK : numBloque*CHUNK+nSamples ]

    # lo pasamos al stream
    stream.write(bloque) # escribimos al stream

    #Pasamos a procesar el siguiente bloque
    numBloque +=1
    print('.',end='')


print('end')
stream.stop()

