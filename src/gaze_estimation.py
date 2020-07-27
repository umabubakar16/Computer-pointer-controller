import cv2
import numpy as np
import logging
import time
from helper import Helper
import math

class GazeEstimationModel(Helper):
    '''
    Class for the Gaze Estimation Model.
    '''
    def __init__(self, model, device='CPU', extensions=None):
        super().__init__(model,device,extensions)
        self.p_frame = None
        self.show = False
        l_e = 'left_eye_image'
        r_e = 'right_eye_image'
        self.input_shape_l=self.net.inputs[l_e].shape
        self.input_shape_r=self.net.inputs[r_e].shape
        self.output_names = [n for n in self.net.outputs.keys()]
        self.model_name = "Gaze Estimation"

    def load_model(self):
        '''
        TODO: You will need to complete this method.
        This method is for loading the model to the device specified by the user.
        If your model requires any Plugins, this is where you can load them.
        '''
        Helper.load_model(self)

    def predict(self, left_eye_image, right_eye_image, hpa):
        '''
        TODO: You will need to complete this method.
        This method is meant for running predictions on the input image.
        '''
        # process the input
        lt_rt_input_result = self.preprocess_input(left_eye_image, right_eye_image = right_eye_image)
        if lt_rt_input_result is None:
            return None, None
       
        le_img_processed, re_img_processed = lt_rt_input_result
        self.p_frame = lt_rt_input_result
        outputs = self.exec_net.infer({'head_pose_angles':hpa, 'left_eye_image':le_img_processed, 'right_eye_image':re_img_processed})
        new_mouse_coord, gaze_vector = self.preprocess_output(outputs,hpa)
        prid_res =  {'head_pose_angles':hpa,'left_eye_image':le_img_processed,'right_eye_image':re_img_processed}
        _input_dict = prid_res
        
        #get output results from input image
        result = self.req_get(req_type="sync", input_dict=_input_dict)
       
        outputs = self.preprocess_output(result, hpa)
        new_mouse_coord, gaze_vector  = outputs[0], outputs [1]
        return new_mouse_coord, gaze_vector

    def preprocess_output(self, outputs, hp_angle):
        '''
        Before feeding the output of this model to the next model,
        you might have to preprocess the output. This function is where you can do that.
        '''
        gaze_vector = list(outputs[self.output_names[0]])[0]
        #gaze_vector = list[self.output_name[0]][0]
        mouse_cord = (0, 0)
        try:
            cos_value = math.cos(hp_angle[2]*math.pi/180.0)
            sin_value = math.sin(hp_angle[2]*math.pi/180.0)
        
            cord_x = gaze_vector[0]*cos_value+gaze_vector[1]*sin_value
            cord_y = (-gaze_vector[0])*sin_value+gaze_vector[1]*cos_value
            mouse_cord = (cord_x, cord_y)
        except Exception as e:
            logger.error("Error preprocessing output result in Gaze Estimation Model" + str(e))
        return (cord_x,cord_y), gaze_vector

    def show_gaze(self, l_eye, r_eye, gaze_vector):
        x = int(gaze_vector[0]*15)
        y = int(gaze_vector[1]*15)
        w = 160
        points = (x-w, y-w), (x+w, y+w), (x-w, y+w), (x+w, y-w)
        l_eye = cv2.line(l_eye, points[0], points[1], (255,0,255), 2)
        cv2.line(l_eye, points[2], points[3], (0,200,255), 2)
        r_eye = cv2.line(r_eye, points[0], points[1], (255,0,255), 2)
        cv2.line(r_eye, points[2], points[3], (0,200,255), 2)
        return 

