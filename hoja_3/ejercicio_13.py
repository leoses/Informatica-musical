
import numpy as np         # arrays    
import sounddevice as sd   # modulo de conexión con portAudio
import soundfile as sf     # para lectura/escritura de wavs
import kbhit               # para lectura de teclas no bloqueante

SRATE = 44100
CHUNK = 1024
FREC = 10
last = 0 # ultimo frame generado

def oscChuck(frec,vol):
 global last # var global
 data = vol*np.sin(2*np.pi*(np.arange(CHUNK)+last)*frec/SRATE)
 last += CHUNK # actualizamos ultimo generado
 return data


# leemos wav en array numpy (data)
# por defecto lee float64, pero podemos hacer directamente la conversion a float32
data  = oscChuck(FREC, 10)#, SRATE = sf.read('piano.wav',dtype="float32")
# abrimos stream de salida
stream = sd.OutputStream(
    samplerate = SRATE,            # frec muestreo 
    blocksize  = CHUNK,            # tamaño del bloque (muy recomendable unificarlo en todo el programa)
    channels   = 1)  # num de canales


kb = kbhit.KBHit()
c= ' '

frame = 0 # frame count
prev = 0 # memoria/buffer del filtro (sample anterior)
while c!= 'q':
      if kb.kbhit():
        c = kb.getch()
      # sacamos bloque en curso
      bloque = data[frame*CHUNK:(frame+1)*CHUNK]
      # procesamos
      bloqueOut = np.zeros(CHUNK,dtype=data.dtype)
      bloqueOut[0] = prev + bloque[0]
      for i in range(1,CHUNK):
        bloqueOut[i] = bloque[i-1] + bloque[i] # 0.5* para normalizar amplitud
      prev = bloque[CHUNK-1] # actualizamos buffer
      # a la salida
      stream.write(bloqueOut.astype((data.dtype)).tobytes())
    

print('end')
stream.stop()