import pyaudio
from scipy.io import wavfile # para manipulación de wavs
import numpy as np # arrays

# Conversion del tipo de datos NumPy a numero de bytes por muestra
def getWidthData(data):
    if data.dtype.name == 'int16': 
        return 2
    elif data.dtype.name in ['int32','float32']: 
        return 4
    elif data.dtype.name == 'uint8': 
        return 1
    else: 
        raise Exception('Not supported')

SRATE, data = wavfile.read('piano.wav') # Obtenemos SRATE y muestras (en data)
# información de wav (opcional)
print("SRATE: {} Format: {} Channels: {} Len: {}".
format(SRATE, data.dtype, len(data.shape), data.shape[0]))
p = pyaudio.PyAudio() # arrancamos pyAudio

# Abrimos un stream de PyAudio para enviar ahí los datos
stream = p.open(format=p.get_format_from_width(getWidthData(data)),
    channels=len(data.shape), # num canales (shape de data)
    rate=SRATE, # frecuencia de muestreo
    frames_per_buffer=1024, # num frames por buffer (elegir)
    output=True) # es stream de salida ()

# escribimos en el stream -> suena!
stream.write(data.astype(data.dtype).tobytes())

# liberamos recursos
stream.stop_stream()
stream.close()
p.terminate()
