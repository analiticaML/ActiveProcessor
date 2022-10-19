#Se importan librerías
import cv2
import os

#Clase encargada del guardado de la imagen en el directorio local
class ImageService:

    #Constructor (Es vacío, pero como Python exige tener algo en el cuerpose pone a=1)
    def __init__(self):
        a=1

    #Método para establecer la existencia del directorio donde se van a guardar las capturas
    def setFolder(self,path):
        #dirCreated = os.mkdir(file)
        dirCreated = os.path.exists(path)
        print("\n Created directory: " + str(dirCreated))

    #Método para guardar la imagen
    def saveImage(self,imageMatrix, path):
        cv2.imwrite(path, imageMatrix)
