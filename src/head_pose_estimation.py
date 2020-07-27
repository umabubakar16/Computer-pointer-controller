import cv2
import numpy as np
from helper import Helper
import time

class HeadPoseEstimationModel(Helper):
    '''
    Class for the Head Pose Estimation Model.
    '''
    def __init__(self, model, device='CPU', extensions=None):
        super().__init__(model,device,extensions)
        self.image_frame = None
        self.show = False
        self.model_name = "Head Pose Estimation"

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
        self.image_frame = image
        # process the image frame
        inputs = self.preprocess_input(self.image_frame)
        self.p_frame = inputs
        input_dict={self.input_name: self.p_frame}

        # get output results from the input image
        result = self.req_get(req_type="sync", input_dict=input_dict)
        return self.preprocess_output(result)
         

    def preprocess_output(self, outputs):
        '''
        Before feeding the output of this model to the next model,
        you might have to preprocess the output. This function is where you can do that.
        '''
        # head_pose_detection results
        pose_angles = ["angle_y_fc","angle_p_fc","angle_r_fc"]
        #angle_names = []
        output_result = map(lambda b : outputs[b][0][0], pose_angles)
        yaw,pitch,roll = output_result

        return [yaw,pitch,roll]

    def show_hp(self, frame, hpa):
        if frame.shape[0]>1000:
            message = "Pose Angles (y|p|r): {:.2f} | {:.2f} | {:.2f}".format(hpa[0],hpa[1],hpa[2])
            cv2.putText(frame, message, (45, 45), cv2.FONT_HERSHEY_COMPLEX, 1.4, (0, 0, 0), 1, cv2.LINE_AA, False)
        return frame