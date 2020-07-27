import cv2
import numpy as np
from helper import Helper
import time
class FacialLandmarksDetectionModel(Helper):
    '''
    Class for the Facial Landmarks Detection Model.
    '''
    def __init__(self, model, device='CPU', extensions=None):
        super().__init__(model,device,extensions)
        self.current_frame = None
        self.model_name = "Facial Landmarks Detection"       
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
        self.proc_img = self.preprocess_input(self.current_frame)
        _input_dict={self.input_name: self.proc_img}
        result = self.req_get(req_type="sync", input_dict=_input_dict, outputs=self.output_name)
       
        left_eye, right_eye = self.preprocess_output(result)
        return left_eye, right_eye

    def preprocess_output(self, outputs):
        '''
        Before feeding the output of this model to the next model,
        you might have to preprocess the output. This function is where you can do that.
        '''
        lt_eye_x = outputs[0][0].tolist()[0][0]
        lt_eye_y = outputs[0][1].tolist()[0][0]
        rt_eye_x = outputs[0][2].tolist()[0][0]
        rt_eye_y = outputs[0][3].tolist()[0][0]
        coords = [lt_eye_x,lt_eye_y,rt_eye_x,rt_eye_y]
        frame = self.current_frame
        h,w = frame.shape[0:2]
        coords = np.int32(coords * np.array([w, h, w, h]))
        
        le_xmin, le_ymin, re_xmin, re_ymin = map(lambda i : coords[i]-15, [0,1,2,3])
        le_xmax, le_ymax, re_xmax, re_ymax = map(lambda i : coords[i]+15, [0,1,2,3])
        
        left_eye =  frame[le_ymin:le_ymax, le_xmin:le_xmax]
        right_eye = frame[re_ymin:re_ymax, re_xmin:re_xmax]
        eye_coords = [[le_xmin,le_ymin,le_xmax,le_ymax], [re_xmin,re_ymin,re_xmax,re_ymax]]
        
        if self.show:
            cv2.rectangle(frame,(le_xmin,le_ymin),(le_xmax,le_ymax),(255,0,0),2)
            cv2.rectangle(frame,(re_xmin,re_ymin),(re_xmax,re_ymax),(255,0,0),2)
        
        return left_eye, right_eye
