'''
Software para detectar movimiento.
Captura cuadros (frames) de video de streaming (eviados a través de protocolo RTSP).
Cada frame es procesado y comparado con el frame anterior para encontrar la diferencia 
de pixeles. Si dicha diferencia es mayor a un nivel umbral preestablecido se guarda la
imagen en un directorio del servidor local y  se envía un mensaje a través del servidor
de mensajería MQRabbit confirmando la captura. 
'''

#Se importan las librerías
import os
import asyncio
from recorder import Recorder

#Función de inicialización
async def main():

    #Se crea objeto tipo Recorder 
    recorder=Recorder(capturesFolder,mq_host, int(movementSensibility), int(millisecondBetweenCaptures))
    #Se comienza el streaming a través del método de la clase Recorder
    recorder.start()

if __name__ == "__main__":

    #Se establecen variables con base en variables de entorno del sistema
    capturesFolder = os.environ['CAPTURES_FOLDER'] #Folder donde se van a guardar las imagenes
    mq_host = os.environ.get('MQ_HOST') #Host de donde se envían los mensajes para MQRabbit (localhost)
    movementSensibility = os.environ.get('MOVEMENT_SENSIBILITY') #Nivel umbral para diferencia de pixeles
    millisecondBetweenCaptures = os.environ.get('MILLISECONDS_BETWEEN_CAPTURES') #Milisegundos entre capturas
    captures_folder = os.environ.get('CAPTURES_FOLDER') #Folder donde se van a guardar las imagenes

    asyncio.run(main())
    



