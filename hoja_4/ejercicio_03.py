# creacion de una ventana de pygame
import pygame
from pygame.locals import *

import numpy as np         # arrays    
import sounddevice as sd   # modulo de conexión con portAudio


SRATE = 44100       # sampling rate, Hz, must be integer
CHUNK = 16

# [(fc,vol),(fm1,beta1),(fm2,beta2),...]
def oscFM(frecs,frame):
    # sin(2πfc+βsin(2πfm))  
    chunk = np.arange(CHUNK)+frame
    samples = np.zeros(CHUNK)+frame
    # recorremos en orden inverso
    
    for i in range(len(frecs)-1,-1,-1):
        samples = frecs[i][1] * np.sin(2*np.pi*frecs[i][0]*chunk/SRATE + samples)
    return samples


#Creamos stream
stream = sd.OutputStream(samplerate=SRATE,blocksize=CHUNK,channels=1)  
stream.start()

#inicializacion pygame
WIDTH = 64
HEIGHT = 480
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Theremin")
runnning= True


# [(fc,vol),(fm1,beta1),(fm2,beta2),...]
#frecs = [[220,0.8],[220,0.5],[110,0.3]]

fc, fm = 220, 220
rangeFreq = [100,10000]
frecs = [[fc,0.8],[fc+fm,0.5],[fc+2*fm,0.3],[fc+3*fm,0.2]]

frame = 0
isrunning = True
currentFreq = 1
currentVol = 0
frecs = [[fc,0.8],[fc+fm,0.5],[fc+2*fm,0.3],[fc+3*fm,0.2]]
print(type(frecs))

while isrunning:

    # obtencion de la posicion del raton
    for event in pygame.event.get():
        if event.type == pygame.MOUSEMOTION:
            mouseX, mouseY = event.pos
            currentFreq = rangeFreq[0] + int(float(mouseX/WIDTH)*(rangeFreq[1] - rangeFreq[0]))
            currentVol = float(mouseY/HEIGHT)

            print("FreqActual: " + str(currentFreq))
            print("volActual:" + str(currentVol))
            
            frecs = [[currentFreq,0.8],[currentFreq+fm,0.5],[currentFreq+2*fm,0.3],[currentFreq+3*fm,0.2]]
        elif event.type == pygame.QUIT:
            isrunning = False
            continue
    
    samples = oscFM(frecs,frame)   
    stream.write(np.float32(currentVol*samples)) 

    frame += CHUNK
            
      
stream.stop()
pygame.quit()