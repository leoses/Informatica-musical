import numpy as np         # arrays    
import sounddevice as sd   # modulo de conexión con portAudio
import soundfile as sf     # para lectura/escritura de wavs
import kbhit 

data, SRATE = sf.read('piano.wav',dtype="float32")
# corregido
last = 0 # ultimo frame generado
CHUNK = 4096
VOL = 1.0


def oscChuck(frec,vol):
    global last # var global
    data = vol*np.sin(2*np.pi*(np.arange(CHUNK)+last)*frec/SRATE, dtype="float32")
    last += CHUNK # actualizamos ultimo generado
    return data

class Delay:
    def __init__(self, sound, delay):
        self.sound = sound
        self.delay = delay
    
    def applyDelay(self):
        #print("Longitud de la muestra antes de aplicar el retardo: " + str(len(self.sound)))
        nSamples = int(SRATE*float(self.delay))
        #añadimos al principio del fragmento una zona en silencio de nSamples
        #para generar asi el delay
        delayedSound = np.append( np.sin((np.arange(nSamples))*0/SRATE, dtype="float32"),self.sound)
        #print("Longitud de la muestra despues de aplicar el retardo: " + str(len(delayedSound)))
        return delayedSound

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
nSamples = CHUNK 
numBloque = 0
c= ' '
kb = kbhit.KBHit()

# termina con 'q' o cuando el último bloque ha quedado incompleto (menos de CHUNK samples)
while c!= 'q' and nSamples == CHUNK: 
    # numero de samples a procesar: CHUNK si quedan sufucientes y si no, los que queden
    nSamples = min(CHUNK,data.shape[0] - (numBloque+1)*CHUNK)

    # nuevo bloque
    bloque = data[numBloque*CHUNK : numBloque*CHUNK+nSamples ]
    bloque *= VOL

    # lo pasamos al stream
    stream.write(bloque) # escribimos al stream


    # modificación de volumen 
    if kb.kbhit():
        c = kb.getch()
        if (c=='v'): VOL= max(0,VOL-0.05)
        elif (c=='V'): VOL= min(1,VOL+0.05)
        elif(c =="S"):
            print("Retardo añadido")
            retardo = Delay(data, 1.0)
            data = retardo.applyDelay()


    print('.',end='')


print('end')
stream.stop()

