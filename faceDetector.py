from facenet_pytorch import MTCNN
import numpy as np
import os
os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"

class FaceDetector: 

    def __init__(self):

        a=0
        #Detector MTCNN
        self.mtcnn = MTCNN(
                    select_largest = True,
                    min_face_size  = 30,
                    thresholds     = [0.8, 0.8, 0.8],
                    post_process   = False,
                    image_size     = 160
                )


    def facedetector(self,frame):

        #imagen= cv2.imread(imagePath)
        #imagen= cv2.cvtColor(imagen,cv2.COLOR_BGR2RGB)


        # # Detector MTCNN
        # mtcnn = MTCNN(
        #             select_largest = True,
        #             min_face_size  = 15,
        #             thresholds     = [0.6, 0.7, 0.7],
        #             post_process   = False,
        #             image_size     = 160
        #         )
      

        # Detección de bounding box y landmarks
        boxes, probs, landmarks = self.mtcnn.detect(frame, landmarks=True)
    
        
        try:
            for box, landmark in zip(boxes, landmarks):
            
                xy  = (box[0], box[1])
                width  = box[2] - box[0]
                height = box[3] - box[1]
    
            return boxes

        except:
            return np.array([])
