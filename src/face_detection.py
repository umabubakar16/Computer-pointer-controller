import cv2
import numpy as np
import logging
import time
from helper import Helper

class FaceDetectionModel(Helper):
    '''
    Class for the Face Detection Model.
    '''
    def __init__(self, model, device='CPU', extensions=None, threshold=0.60):
        super().__init__(model,device,extensions)
        self.threshold = threshold
        self.width, self.height = 0, 0
        self.model_name = "Face Detection"
        self.current_frame = None
        self.show = False
      
    def load_model(self):
        '''
        TODO: You will need to complete this method.
        This method is for loading the model to the device specified by the user.
        If your model requires any Plugins, this is where you can load them.
        '''
        Helper.load_model(self)
 

    def predict(self, image):
        '''
        TODO: You will need to complete this method.
        This method is meant for running predictions on the input image.
        '''
        self.current_frame = image
        # process frame
        frame = self.current_frame
        self.pr_frame = self.preprocess_input(frame)
        _input_dict={self.input_name: self.pr_frame}
        
        result = self.req_get(req_type="sync",input_dict=_input_dict,outputs=self.output_name)
       
        outputs = self.preprocess_output(result)
        if outputs is None:
            return None
        frame, cropped_face, coords = outputs
        return frame, cropped_face, coords


    def preprocess_output(self, outputs):
        '''
        Before feeding the output of this model to the next model,
        you might have to preprocess the output. This function is where you can do that.
        '''
        detections = []
        coords=list()
        for box in range (len(outputs[0][0])):
            boxes = outputs[0][0][box]
            confidence = boxes[2]
            if confidence > self.threshold:
                coords_list = [boxes[3],boxes[4],boxes[5], boxes[6]]
                coords.append(coords_list)
                xmin =  int(box*self.width)
                xmax =  boxes[3],boxes[5]
                ymin =  int(box*self.height)
                ymax =  boxes[4],boxes[6]
                detections.append([xmin, ymin, xmax, ymax])
                if self.show:
                    cv2.rectangle(self.current_frame,(xmin-15,ymin-15), (xmax+15,ymax+15), (125, 255, 125) , 2)
        if len(coords) == 0:
            return None
        else:
            if len(coords) > 1:
                logging.warning("Many faces faces detected!, only one face would be")
            coords = coords [0]
        h= self.current_frame.shape[0] 
        w = self.current_frame.shape[1]
        coords = np.int32(coords * np.array([w, h, w, h]))
        face_cord = self.current_frame[coords[1]:coords[3], coords[0]:coords[2]]
        return self.current_frame, face_cord, coords