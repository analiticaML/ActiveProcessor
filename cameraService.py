#Se improtan librerías
import cv2
import numpy as np

#Clase encargada de conectar con el dispositivo de streaming a través del protocolo
#RTSP. Obtiene el contorno de cada cuadro y lo compara con el cuadro anterior.
#Se evalúa si la diferencia de pixeles es mayor a un nivel umbral preestablecido.
#Si la diferencia es mayor se guarda la imagen en un directorio local preestablecido.
class CameraService:

    #Constructor
    def __init__(self):
        self.count=0


    #Configuración inicial de la recepción del streaming
    def openCamera(self,width, height, rtsp):
        #Variable con el streaming de video
        self.camera=cv2.VideoCapture(rtsp)
        
        print("Esperando conexión con la cámara")

        #Verificación de la conexión con la cámara
        if (self.camera.isOpened()):
            print("Video is captured")
        else:
            print("Video is not working")


        #Tamaño de la imagen transmitida
        width2 = self.camera.get(cv2.CAP_PROP_FRAME_WIDTH )
        height2 = self.camera.get(cv2.CAP_PROP_FRAME_HEIGHT)
        print(width2)
        print(height2)
        
        #Se ajusta tamaño de la recepción de acuerdo al tamaño de
        #la imagen del video transmitido.
        self.camera.set(3, width)
        self.camera.set(4, height)

        #Se espera 1 segundo mientras se establece la conexión con la cámara
        cv2.waitKey(1000)

    #Método para obtener un cuadro (frame) del streaming
    def getFrame(self):
       
        _, frame = self.camera.read()

        return frame

    #Método para cambiar el frame a escala de grises
    def getGrayScaleFrame(self,frame):
            
            greyScaleFrame=cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            greyScaleFrame = cv2.GaussianBlur(greyScaleFrame,(21, 21), 0)

            return greyScaleFrame

    #Método para obtener diferencia entre dos cuadros
    def getFramesDifference(self,frameGrayScale,newFrameGrayScale):
        framesDifference = cv2.absdiff(frameGrayScale, newFrameGrayScale)
        return framesDifference
    
    #Método para obetener los contornos de la imagen con la diferencia de lso dos cuadros
    def getContours(self,framesDifference):
        
        kernel = np.ones((5, 5), np.uint8)
        ret,threshold = cv2.threshold(framesDifference,  25, 255, cv2.THRESH_BINARY)
        threshold = cv2.dilate(src=threshold,kernel=kernel,anchor=(-1, -1) ,iterations= 2)
        countours,hierarchy = cv2.findContours(threshold,  cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        return countours
    
    #Método que establece si hubo movimiento 
    def detectMovement(self,frameGrayScale, newFrameGrayScale,limit):
        

        framesDifferenceContours=[]
        #Se obtiena la diferencia entre cuadros
        framesDifference = self.getFramesDifference(frameGrayScale, newFrameGrayScale)
        #Se obtiene el contorno de dicha diferencia
        framesDifferenceContours=self.getContours(framesDifference)

        #Para cada uno de los puntos encontrados en el contorno de la diferencia
        for framesDifferenceContour in framesDifferenceContours:
            
            #Se compara el área del contorno con el nivel umbral
            #Si es mayor se aumenta el contador
            print(cv2.contourArea(framesDifferenceContour))
            if cv2.contourArea(framesDifferenceContour) > limit:
                self.count=self.count+1
                print(self.count)

                return True 

        return False

