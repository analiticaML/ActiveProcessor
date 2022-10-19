#Se importan librerías
from faceDetector import FaceDetector
from cameraService import CameraService
from imageService import ImageService
from subprocess import call
import time
import json
import os
import datetime

#Clase donde se desarrolla el proceso de streaming, guardado de captura y notificación
# a servidor de mensajería 
class Recorder:

    #Cosntructor
    def __init__(self,path, mqHost, movementSensibility, millisecondsBetweenCaptures):
        self.path = path
        self.mqHost = mqHost
        self.movementSensibility =  movementSensibility
        self.millisecondsBetweenCaptures = millisecondsBetweenCaptures

    #Método para comenzar el streaming
    def start(self):

        #Se crea objeto tipo ImageService
        imageservice=ImageService()
        #Método para verificar existencia del directorio donde se guardan las capturas
        imageservice.setFolder(self.path)

        #Se crea objeto tipo CameraService
        cameraservice=CameraService()

        #Se establece conexión del streaming
        cameraservice.openCamera(800, 1080, "rtsp://192.168.1.16:554/live1s1.sdp")
   

        #Se obtiene la imagen actual en escala de grises
        previousGrayFrame = cameraservice.getGrayScaleFrame(cameraservice.getFrame())
     

        #Se esteblece un contador para disminuir el número de imágenes a las cuales
        #se les hace el análisis. 
        cuenta=0

        cuenta2 = 0

        facedetector = FaceDetector()

        banderaProcesor= 0

        #Ciclo infinito para la captura de cuadros
        while (True):
            try:
                #Nuevo cuadro
                newFrame = cameraservice.getFrame()
            
                cuenta = cuenta + 1

                #Se salta el análisis de 5 imágenes
                if (cuenta > 30):

                    #Cambia  a escala de grises el nuevo cuadro
                    newFrameGrayScale = cameraservice.getGrayScaleFrame(newFrame)
                    now = datetime.datetime.now()
                    date=str(now.year)+str(now.month)+str(now.day)+str(now.hour)+str(now.minute)+str(now.second)+str(now.microsecond)
                    #Se gurda la imagen el directorio local con nombre de la imagen como la fecha y hora de la captura
                    imageservice.saveImage(previousGrayFrame, "/home/analitica2/Documentos/previus"+ "/" + date + ".jpg")
                    imageservice.saveImage(newFrameGrayScale, "/home/analitica2/Documentos/newframe"+ "/" + date + ".jpg")
                    #Se llama a método para detectar movimiento
                    if (cameraservice.detectMovement(previousGrayFrame, newFrameGrayScale, 50000)):
                        print("Motion detected!!!")

                        #objetos= persondetector.detectObjects(path)
                        caras = facedetector.facedetector(newFrame)                      
                                
                        if (caras.size != 0 and banderaProcesor == 0):
                            cuenta2 = 0
                            now = datetime.datetime.now()
                            date=str(now.year)+str(now.month)+str(now.day)+str(now.hour)+str(now.minute)+str(now.second)+str(now.microsecond)
                            #Se gurda la imagen el directorio local con nombre de la imagen como la fecha y hora de la captura
                            imageservice.saveImage(newFrame, "/home/analitica2/Documentos/CapturesWithProcessor"+ "/" + date + ".jpg")
                            banderaProcesor = 1
                            print("Se detectó una cara y se enciende el procesor")
                            os.system('aws rekognition start-stream-processor --name my-rekognition-video-stream-processor --region us-east-1')
                            #call('aws rekognition start-stream-processor --name my-rekognition-video-stream-processor --region us-east-1', shell=True)
                            for i in range(0,450):
                                i+=1
                                newFrame = cameraservice.getFrame()  
                            

                        elif(caras.size != 0 and banderaProcesor == 1):
                            cuenta2 = 0
                            now = datetime.datetime.now()
                            date=str(now.year)+str(now.month)+str(now.day)+str(now.hour)+str(now.minute)+str(now.second)+str(now.microsecond)
                            #Se gurda la imagen el directorio local con nombre de la imagen como la fecha y hora de la captura
                            imageservice.saveImage(newFrame, "/home/analitica2/Documentos/CapturesWithProcessor"+ "/" + date + ".jpg")
                            print("el procesor sigue encendido")
                            for i in range(0,450):
                                i+=1
                                newFrame = cameraservice.getFrame()  
                        
                        elif(caras.size == 0 and banderaProcesor == 1):
                            cuenta2 = 0
                            banderaProcesor = 0
                            print("Se apaga el stream procesor")
                            os.system('aws rekognition stop-stream-processor --name my-rekognition-video-stream-processor --region us-east-1')
                            #call('aws rekognition stop-stream-processor --name my-rekognition-video-stream-processor --region us-east-1', shell=True)
                        
                        newFrameGrayScale = cameraservice.getGrayScaleFrame(newFrame)
                        previousGrayFrame = newFrameGrayScale
                    else:      
                        previousGrayFrame = newFrameGrayScale
                    
                    if (cuenta2 > 10 and banderaProcesor == 1):
                        cuenta2 = 0
                        banderaProcesor = 0
                        print("Se apaga el stream procesor sin movimiento")
                        os.system('aws rekognition stop-stream-processor --name my-rekognition-video-stream-processor --region us-east-1')
                        #call('aws rekognition stop-stream-processor --name my-rekognition-video-stream-processor --region us-east-1', shell=True)
                        
                    cuenta2+=1
                    cuenta=0
            except:
                cameraservice.openCamera(800, 1080, "rtsp://192.168.1.16:554/live1s1.sdp")
               